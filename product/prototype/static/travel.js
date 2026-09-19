'use strict';
const $ = id => document.getElementById(id);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels = {consider_paying:'Conditional interest · no price tested',free_only:'Would use free only',decline:'Would decline'};
let token, config, current, baseline, polling = false, busy = false, responsePage = 0, displayedGraph = null;
function error(message='') { $('error').textContent=message; $('error').hidden=!message; }
function jump(id) { $(id).scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'}); }
async function api(path, data) {
  const response=await fetch('/api/travel/'+path,{method:'POST',headers:{'Content-Type':'application/json','X-Session-Token':token},body:JSON.stringify(data)});
  const result=await response.json(); if(!response.ok) throw new Error(result.error||'Request failed'); return result;
}
function buttons() {
  $('run').disabled=busy||!config?.configured||!$('confirm').checked;
  $('revise').disabled=busy||!config?.configured||!current?.completed||!['completed','partial'].includes(current?.status);
  $('replay').disabled=busy||!config?.replay_available;
  $('replay-revision').disabled=busy||!config?.revision_replay_available;
  $('export').disabled=!current;
  $('next').disabled=!current?.completed;
}
function graphStudy() {
  if(!config.graph)return config.study;
  return {...config.study,profiles:config.graph.profiles,sources:config.graph.sources.map(s=>({...s,observation:s.text,limit:'Aggregate research, not person-level data or evidence of paid demand.'}))};
}
function contextHTML(study) {
  const grounded=study.profiles.some(p=>p.graph_node_ids);
  $('population-method').textContent=grounded?'Attitude seeds come from MiroFish’s graph-based profile generator. Travel circumstances use a documented scenario design; no profile represents an identified real person.':'Legacy authored profiles. This earlier recording did not use the knowledge graph.';
  $('offer-text').textContent=study.offer;
  $('sources').innerHTML=study.sources.map(s=>`<details class="source"><summary><span class="eyebrow">${esc(s.id)}</span> · ${esc(s.title)}</summary><p>${esc(s.observation)}</p><p class="subtle">${esc(s.limit)}</p><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">Inspect source ↗</a><p class="subtle">Recorded research · checked ${esc(s.checked)} · no live retrieval in this run</p></details>`).join('');
  $('population-title').textContent=`${study.profiles.length.toLocaleString()} traveller scenarios · showing the first ${Math.min(10,study.profiles.length)}`;
  $('profiles').innerHTML=study.profiles.slice(0,10).map(p=>`<article class="profile"><h4><span class="eyebrow">${esc(p.id)}</span> ${esc(p.label)}</h4><p>${esc(p.persona)}</p><p class="subtle">Context: ${esc(p.sources.join(', '))}. ${esc(p.assumption)}</p></article>`).join('');
  $('feedback-profile').innerHTML=study.profiles.map(p=>`<option value="${esc(p.id)}">${esc(p.id)} · ${esc(p.label)}</option>`).join('');
}
function render(run) {
  current=run; $('knowledge-graph').hidden=!run.knowledge_graph; if(run.knowledge_graph)renderGraph(run.knowledge_graph);
  const running=['starting','running'].includes(run.status);
  labels.consider_paying = run.price_gbp_per_trip ? `Hypothetical paid choice · £${run.price_gbp_per_trip}/trip` : 'Conditional interest · no price tested';
  $('offer-text').textContent = run.offer;
  $('price-note').textContent = run.price_gbp_per_trip ? `Test assumption: £${run.price_gbp_per_trip} per trip. No actual purchases or validated demand.` : 'No price was tested in this historical run.';
  const counts=run.counts||Object.fromEntries(Object.keys(labels).map(k=>[k,run.responses.filter(r=>r.answer.decision===k).length]));
  $('status').textContent=`${run.replay?'Recorded replay · ':''}${running?'Local interviews in progress':run.status==='completed'?'Study complete':run.status==='partial'?'Study partially complete':'Study failed'} · ${run.completed}/${run.requested} structured responses${run.active_profile?' · interviewing '+run.active_profile:''}`;
  $('progress').hidden=!running;$('progress').value=run.completed;$('progress').max=run.requested;
  $('pinned-run').textContent=`Audience v${run.audience_version} · ${run.completed}/${run.requested} completed`;
  const unanimous = run.completed >= 10 && Object.values(counts).some(n => n === run.completed);
  $('demand-warning').hidden = !unanimous;
  $('demand-warning').textContent = 'Demand assessment unreliable: every synthetic response chose the same answer. These are model outputs, not paying customers. No real purchase was tested. Inspect the offer and prompt; shared model bias may explain the result.';
  $('metrics').innerHTML=Object.entries(labels).map(([key,label])=>`<div class="metric"><strong>${counts[key]}</strong><span>${label}</span></div>`).join('');
  $('run-meta').textContent=`${run.elapsed_seconds}s${run.not_attempted?' · '+run.not_attempted+' not attempted':''} · ${run.failed.length} failed · ${run.excluded.length} excluded · ${run.model||config.model} · ${run.usage?.calls||0} model calls · ${run.usage?run.usage.prompt_tokens+run.usage.completion_tokens:0} tokens · $0 paid API spend. Synthetic counts, not conversion rates.`;
  renderResponses(run);
  $('run-errors').innerHTML=[...(run.error?[run.error]:[]),...run.failed.map(f=>`${f.profile_id}: ${f.error}`),...run.excluded.map(f=>`${f.profile_id}: excluded — ${f.error}`),...(run.halt_reason?[run.halt_reason]:[])].map(e=>`<p class="boundary">${esc(e)}</p>`).join('');
  $('technical').textContent=JSON.stringify({id:run.id,created_at:run.created_at,engine:run.engine,scope:run.scope,model:run.model,model_config:run.model_config,usage:run.usage,audience_version:run.audience_version,parent_id:run.parent_id,input_sha256:run.input_sha256,runner_sha256:run.runner_sha256,mirofish_source_sha256:run.mirofish_source_sha256,system_prompts:run.system_prompts,prompt:run.prompt,changes:run.changes,scope_amendment:run.scope_amendment},null,2);
  $('recommendations').innerHTML=run.completed?`${Object.values(counts).some(n=>n===run.completed)?'<div class="boundary"><strong>All valid responses chose the same category.</strong><p>This may reflect shared model bias or broad wording. It is a reason to challenge the study, not evidence of universal demand.</p></div>':''}<p class="eyebrow">DIRECTION FOR A REAL TEST</p><h3>Investigate the conditions, not just the yeses.</h3><p>${counts.consider_paying} of ${run.completed} valid synthetic responses would consider paying. ${run.price_gbp_per_trip ? `The hypothetical price was £${run.price_gbp_per_trip} per trip.` : 'No price was tested.'} Ask real travellers to compare this offer with their existing tools before drawing a commercial conclusion.</p><ul>${run.responses.slice(0,3).map(r=>`<li><strong>${esc(r.profile_id)}</strong> · ${esc(r.answer.next_test)}</li>`).join('')}</ul><p class="subtle">Rule-based summary of this run. Sample composition, a shared model and authored profiles can produce correlated answers.</p>`:'';
  if(run.parent_id && baseline) renderComparison(baseline,run);
  buttons();
}
function renderResponses(run) {
  const filter=$('response-filter').value.toLowerCase();
  const matches=run.responses.filter(r=>`${r.profile_id} ${r.label} ${r.answer.decision}`.toLowerCase().includes(filter));
  const pages=Math.max(1,Math.ceil(matches.length/12)); responsePage=Math.min(responsePage,pages-1);
  const visible=matches.slice(responsePage*12,responsePage*12+12);
  $('response-controls').hidden=!run.responses.length;
  $('response-page').textContent=`${responsePage+1} / ${pages} · ${matches.length} matching`;
  $('response-prev').disabled=responsePage===0; $('response-next').disabled=responsePage>=pages-1;
  $('responses').innerHTML=visible.map(r=>{
    const a=r.answer,s=a.scenario,c=r.calculation;
    return `<article class="response"><span class="decision">${esc(r.profile_id)} / ${esc(labels[a.decision])}</span><h3>${esc(r.label)}</h3><blockquote>“${esc(a.reason)}”</blockquote><dl><dt>Potential value</dt><dd>${esc(a.valuable_feature)}</dd><dt>Objection</dt><dd>${esc(a.objection)}</dd><dt>Test with people</dt><dd>${esc(a.next_test)}</dd></dl><details><summary>Inspect the proposed scenario and calculation</summary><div class="calculation"><p class="eyebrow">MODEL ASSUMPTIONS → PYTHON ARITHMETIC</p><p class="mono">${s.hours_saved_per_trip}h × ${s.trips_per_year} trips × £${s.value_per_hour_gbp}/h = £${c.annual_time_value_gbp}/year</p><p>${esc(s.rationale)}</p><p class="subtle">Illustrative time value only. Not a price, revenue estimate or willingness to pay. Numerical consistency and realism still need human review.</p></div></details><details><summary>Raw engine response</summary><pre>${esc(r.raw)}</pre></details></article>`;
  }).join('');
  const decisions=new Map(run.responses.map(r=>[r.profile_id,r.answer.decision]));
  const failures=new Set([...run.failed,...run.excluded].map(r=>r.profile_id));
  $('population-map').innerHTML=run.profiles.map(p=>`<span class="respondent ${decisions.get(p.id)|| (failures.has(p.id)?'failed':'pending')}" title="${esc(p.id)}: ${esc(decisions.get(p.id)|| (failures.has(p.id)?'failed/excluded':'pending'))}"></span>`).join('');
}
$('response-filter').oninput=()=>{responsePage=0;if(current)renderResponses(current);};
$('response-prev').onclick=()=>{responsePage--;renderResponses(current);};
$('response-next').onclick=()=>{responsePage++;renderResponses(current);};
function renderGraph(graph) {
  if(!graph)return;
  if(displayedGraph===graph.graph_id)return;
  displayedGraph=graph.graph_id;
  $('graph-status').textContent=`${graph.node_count||graph.nodes.length} entities · ${graph.edge_count||graph.edges.length} relationships · recorded MiroFish-local extraction. Select an entity to inspect its source and links.`;
  $('allocation').textContent=graph.allocation;
  const columns=[[],[],[]];
  graph.nodes.forEach(n=>columns[n.labels.includes('ResearchSource')?0:n.labels.includes('AudienceCohort')?1:2].push(n));
  const positions=new Map(); const height=Math.max(...columns.map(c=>c.length))*70+50;
  columns.forEach((col,i)=>col.forEach((n,j)=>positions.set(n.uuid,{x:60+i*290,y:40+j*70})));
  $('graph-canvas').innerHTML=`<svg viewBox="0 0 900 ${height}" role="group" aria-label="MiroFish research knowledge graph">${graph.edges.map(e=>{const a=positions.get(e.source_node_uuid),b=positions.get(e.target_node_uuid);if(!a||!b)return '';return `<path d="M${a.x},${a.y} C${(a.x+b.x)/2},${a.y} ${(a.x+b.x)/2},${b.y} ${b.x},${b.y}"/>`;}).join('')}${graph.nodes.map(n=>{const p=positions.get(n.uuid);return `<g data-node="${esc(n.uuid)}" role="button" tabindex="0" aria-label="${esc(n.name)}"><circle cx="${p.x}" cy="${p.y}" r="7"/><text x="${p.x+13}" y="${p.y+5}">${esc(n.name.length>27?n.name.slice(0,24)+'…':n.name)}</text></g>`;}).join('')}</svg>`;
  function select(id){const n=graph.nodes.find(n=>n.uuid===id);const edges=graph.edges.filter(e=>e.source_node_uuid===id||e.target_node_uuid===id);$('graph-detail').innerHTML=`<h4>${esc(n.name)}</h4><p>${esc(n.summary)}</p><p class="subtle">Source ${esc(n.attributes.source_id)} · Supporting text: ${esc(n.attributes.evidence_quote)}</p><ul>${edges.map(e=>`<li>${esc(e.fact)} <span class="subtle">(${esc(e.attributes.source_id)})</span></li>`).join('')}</ul>`;}
  $('graph-canvas').querySelectorAll('[data-node]').forEach(el=>{el.onclick=()=>select(el.dataset.node);el.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(el.dataset.node);}};});
  select(graph.nodes.find(n=>n.labels.includes('AudienceCohort'))?.uuid||graph.nodes[0].uuid);
}
function renderComparison(before,after) {
  const feedback=after.feedback?.at(-1);
  if(!feedback)return;
  const old=before.responses.find(r=>r.profile_id===feedback.profile_id), fresh=after.responses.find(r=>r.profile_id===feedback.profile_id);
  $('feedback-comparison').innerHTML=`<h3>Audience v${before.audience_version} → v${after.audience_version}</h3><p class="eyebrow">${esc(feedback.kind)} / ${esc(feedback.profile_id)}</p><div class="comparison-row"><strong>Frozen prediction</strong><p>${esc(old?labels[old.answer.decision]:'No valid baseline response')}</p></div><div class="comparison-row"><strong>Supplied feedback</strong><p>${esc(labels[feedback.decision])}: ${esc(feedback.observation)}</p><p class="subtle">${esc(feedback.provenance)} · ${esc(feedback.recruitment)} · ${esc(feedback.collected_at)}</p></div><p class="boundary">${old?.answer.decision===feedback.decision?'Baseline category matches the supplied response.':'Mismatch: the baseline category differs from the supplied response.'} ${fresh?(fresh.answer.decision===feedback.decision?'The revised category matches, but this feedback was used in the revision.':'The mismatch remains after revision.'):''}</p><details><summary>Inspect the exact audience change</summary><pre>${esc(JSON.stringify(after.changes?.at(-1),null,2))}</pre></details><div class="comparison-row"><strong>Revised response</strong><p>${esc(fresh?labels[fresh.answer.decision]:'Awaiting a valid response')}</p><p>${esc(fresh?.answer.reason||'')}</p></div><p class="subtle">One purposively matched workflow; no population inference. Response changes can also reflect model variability. Baseline ${esc(before.id)} is preserved. Independent validation remains pending.</p>`;
}
async function watch(id) {
  polling=true;
  try {
    while(polling) {
      const result=await api('result',{id});render(result);
      if(!['starting','running'].includes(result.status)){polling=false;break;}
      await new Promise(resolve=>setTimeout(resolve,5000));
    }
  } catch(e){error(e.message+' Reload to recover the saved job.');}
  finally{busy=false;buttons();await history();}
}
async function start(data) {
  error();busy=true;buttons();
  try { const run=await api('run',data);render(run);jump('simulation');await watch(run.id); }
  catch(e){error(e.message);busy=false;buttons();}
}
async function history() {
  try {config=await (await fetch('/api/travel')).json();
    $('history').replaceChildren();
    for(const run of config.runs){const b=document.createElement('button');b.textContent=`${run.id} · v${run.audience_version} · ${run.completed}/${run.requested} · ${run.status}`;b.disabled=busy;b.onclick=()=>load(run.id);$('history').append(b);}
  } catch(e){error('Could not refresh saved runs: '+e.message);}
}
async function load(id) {
  error(); $('feedback-comparison').replaceChildren();try{const run=await api('result',{id});baseline=run.parent_id?await api('result',{id:run.parent_id}):null;contextHTML(run);render(run);jump('simulation');if(['starting','running'].includes(run.status)){busy=true;buttons();await watch(run.id);}}catch(e){error(e.message);}
}
$('explore').onclick=()=>jump('evidence');$('next').onclick=()=>jump('learning');$('confirm').onchange=buttons;
$('run').onclick=()=>{baseline=null;$('feedback-comparison').replaceChildren();contextHTML(graphStudy());start({count:Number($('run-count').value),price_gbp_per_trip:Number($('pilot-price').value)});};
$('replay').onclick=()=>load('recorded');
$('replay-revision').onclick=async()=>{await load('recorded-revision');jump('learning');};
$('example-feedback').onclick=()=>{
  $('feedback-profile').value=current?.profiles.find(p=>p.scenario?.companions==='with friends')?.id||current?.profiles[0]?.id||'T01';$('feedback-kind').value='illustrative';$('feedback-decision').value='free_only';
  const date=new Date(); $('feedback-date').value=`${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
  $('recruitment').value='Authored teaching example, one imagined traveller; no customer recruitment.';
  $('observation').value='The organiser already has an itinerary. Most delays come from friends not replying or committing to dates. Everyone prefers staying in their existing group chat, and nobody wants another account.';
  $('same-offer').checked=true;
};
$('feedback-form').onsubmit=async e=>{e.preventDefault();if(!current)return;baseline=structuredClone(current);await start({parent_id:current.id,feedback:{profile_id:$('feedback-profile').value,kind:$('feedback-kind').value,decision:$('feedback-decision').value,collected_at:$('feedback-date').value,recruitment:$('recruitment').value,observation:$('observation').value,offer_tested:current.offer}});};
$('export').onclick=()=>{const url=URL.createObjectURL(new Blob([JSON.stringify(current,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`hindsight-${current.id}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
const observer=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting){document.querySelectorAll('nav a').forEach(a=>a.classList.toggle('active',a.hash==='#'+e.target.id));}},{rootMargin:'-15% 0px -55% 0px'});document.querySelectorAll('main section').forEach(s=>observer.observe(s));
(async()=>{try{const [status,initial]=await Promise.all([fetch('/api/status').then(r=>r.json()),fetch('/api/travel').then(r=>r.json())]);token=status.token;config=initial;contextHTML(graphStudy());renderGraph(config.graph);$('engine-state').textContent=config.configured?'Local MiroFish · configured':'Recorded demo · engine not installed';$('setup-note').textContent=config.configured?'Live runs use the installed local engine. Model availability is checked when the run starts.':'Install the engine using product/prototype/RUN-MIROFISH.md to generate fresh responses. Replay remains available.';buttons();await history();if(config.active_run){busy=true;buttons();await watch(config.active_run);}}catch(e){error('Could not load the local demo: '+e.message);}})();

document.querySelectorAll('nav a').forEach(link=>link.addEventListener('click',()=>{document.querySelectorAll('nav a').forEach(a=>a.classList.toggle('active',a===link));}));

$('pilot-price').onchange=()=>{$('price-note').textContent=`Test assumption: £${$('pilot-price').value} per trip. Synthetic choices are not purchases.`;};

$('pilot-10').onclick=()=>load('pilot-10');
$('pilot-30').onclick=()=>load('pilot-30');
