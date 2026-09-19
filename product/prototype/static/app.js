'use strict';
const $ = id => document.getElementById(id);
const escapeHTML = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const state = {token: '', factors: [], pack: null, report: null, comparison: null};
const examples = {
  notes: 'A voice-note app that turns spoken thoughts into searchable notes and action items, so useful ideas do not disappear before I act on them.',
  tasks: 'A personal planner that rearranges unfinished tasks around changing energy levels and available time, so people can recover when their day goes off plan.'
};
function notice(text = '', error = false) { $('notice').hidden = !text; $('notice').textContent = text; $('notice').dataset.error = error; }
function show(step) {
  for (const name of ['intake', 'brief', 'audiences', 'report']) {
    $(name).hidden = name !== step;
    $('nav-' + name).removeAttribute('aria-current');
  }
  $('nav-' + step).setAttribute('aria-current', 'step');
  notice(); window.scrollTo({top: 0, behavior: 'instant'});
  const heading = $(step).querySelector('h1'); heading.tabIndex = -1; heading.focus({preventScroll: true});
}
async function api(path, data) {
  const response = await fetch('/api/' + path, {method: 'POST', headers: {'Content-Type': 'application/json', 'X-Session-Token': state.token}, body: JSON.stringify(data)});
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || 'The request failed. Retry this step.');
  return body;
}
async function busy(form, message, action) {
  const buttons = [...document.querySelectorAll('button')];
  const disabled = buttons.map(b => b.disabled); buttons.forEach(b => b.disabled = true);
  form.setAttribute('aria-busy', 'true'); notice(message);
  try { await action(); } catch (error) { notice(error.message, true); $('notice').scrollIntoView({block:'nearest'}); }
  finally { buttons.forEach((b, i) => b.disabled = disabled[i]); form.removeAttribute('aria-busy'); }
}
function evidenceHTML(pack) {
  return `<p class="runline">${escapeHTML(pack.mode)} · ${pack.sources.length} unique sources · ${pack.elapsed_seconds}s · $0 API spend${pack.cached ? ' · baseline evidence reused' : ''}</p>` +
    pack.sources.map(s => `<article class="source" data-source="${escapeHTML(s.id)}"><h3><a href="${escapeHTML(s.url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(s.title)} ↗</a></h3><div class="meta mono">${escapeHTML(s.id)} · ${escapeHTML(s.provenance)} · ${escapeHTML(s.roles.join(', '))}</div><blockquote>${escapeHTML(s.observation)}</blockquote><p>${escapeHTML(s.supported_claim)}</p><p class="meta">${escapeHTML(s.limitation)}<br>Retrieved ${escapeHTML(s.retrieved_at)} · Publication date: ${escapeHTML(s.publication_date || 'unknown')}</p></article>`).join('') +
    (!pack.sources.length ? '<p class="empty">No evidence retrieved. All missing inputs remain unscored.</p>' : '') +
    '<h2>Research gaps</h2>' + pack.workers.map(w => `<p><strong>${escapeHTML(w.role)}</strong> · ${escapeHTML(w.gap)}</p>${w.failures.map(f => `<p class="meta">${escapeHTML(f.url)} · ${escapeHTML(f.reason)}</p>`).join('')}`).join('');
}
function renderAudiences() {
  const p = state.pack;
  $('research-summary').innerHTML = `<p class="runline">${p.sources.length} unique sources · Three concurrent source-review workers · ${p.elapsed_seconds}s<br>Suggestions below are rule-based hypotheses. No customer evidence has been inferred from vendor pages.</p>`;
  $('evidence-before').innerHTML = evidenceHTML(p);
  $('audience-fields').innerHTML = p.audiences.map((a, i) => `<div class="audience-edit"><div class="columns"><div><label for="audience-${i}-name">Need-based group ${i + 1}</label><input id="audience-${i}-name" maxlength="800" value="${escapeHTML(a.name)}"></div><div><label for="audience-${i}-need">What they need</label><textarea id="audience-${i}-need" rows="2" maxlength="800">${escapeHTML(a.need)}</textarea></div></div></div>`).join('');
  $('factor-fields').innerHTML = state.factors.map(f => `<div class="factor-entry"><span class="factor-name">${escapeHTML(f.label)}<br><span class="meta mono">weight ${f.weight.toFixed(2)}</span></span><div><label for="factor-${f.key}">Value 0–1</label><input id="factor-${f.key}" type="number" min="0" max="1" step="0.01" aria-label="${escapeHTML(f.label)} value"></div><div><label for="reason-${f.key}">Assumption and reason</label><input id="reason-${f.key}" maxlength="1000" placeholder="Leave blank when unknown" aria-label="${escapeHTML(f.label)} reason"></div></div>`).join('');
}
function citations(ids) {return ids.length ? `<p class="meta mono">Sources: ${ids.map(escapeHTML).join(', ')}</p>` : '';}
function renderReport() {
  const r = state.report, q = r.quant;
  $('report-proposition').textContent = r.brief.benefit;
  $('save-run').textContent = r.saved_at ? 'Saved locally' : 'Save run';
  $('report-overview').innerHTML = `<div class="overview"><div class="metric"><span class="meta">Commercial outlook</span><strong>${escapeHTML(q.outlook[0].toUpperCase() + q.outlook.slice(1))}</strong><span class="meta">Heuristic assessment, unvalidated</span></div><div class="metric"><span class="meta">Evidence coverage</span><strong class="mono">${q.evidence_backed} / ${q.total}</strong><span class="meta">Factors supported by cited evidence</span></div><div class="metric"><span class="meta">Model index</span><strong class="mono">${q.index === null ? 'Unscored' : q.index.toFixed(3)}</strong><span class="meta">${q.supplied} / ${q.total} inputs supplied${q.index !== null ? ' · not a probability' : ''}</span></div></div>`;
  $('panel-outlook').innerHTML = `<h2>Priority audiences to test</h2><p class="meta">Founder-confirmed hypotheses, in your chosen order.</p>${r.audiences.map((a, i) => `<p><strong>${i+1}. ${escapeHTML(a.name)}</strong><br>${escapeHTML(a.need)}</p>`).join('')}<div class="report-grid">${r.sections.map(s => `<article><h3>${escapeHTML(s.title)}</h3><p>${escapeHTML(s.text)}</p>${citations(s.evidence_ids)}</article>`).join('')}</div><h2>Quant factors</h2><p class="meta">Unknown is not zero. Missing factors suppress the aggregate; weights are not redistributed.</p><div class="table-wrap"><table><thead><tr><th>Factor</th><th>Weight</th><th>Value</th><th>Provenance / reason</th></tr></thead><tbody>${q.factors.map(f => `<tr><td>${escapeHTML(f.label)}</td><td class="mono">${f.weight.toFixed(2)}</td><td class="mono">${f.value === null ? '—' : f.value.toFixed(2)}</td><td>${escapeHTML(f.provenance)}${f.reason ? '<br>' + escapeHTML(f.reason) : ''}${citations(f.evidence_ids)}</td></tr>`).join('')}</tbody></table></div><details><summary>Assessment rubric & assumptions</summary><p>${escapeHTML(q.rubric)}</p><ul>${r.assumptions.map(a => `<li>${escapeHTML(a)}</li>`).join('')}</ul><p>No historical launch-outcome dataset is available. Predictive accuracy has not been measured.</p></details><h2>What to do next</h2><ol class="steps">${r.next_tests.map(t => `<li><strong>${escapeHTML(t.title)}</strong><p>${escapeHTML(t.action)}</p></li>`).join('')}</ol>`;
  $('panel-evidence').innerHTML = evidenceHTML(r.evidence);
  const sim = r.simulation;
  $('panel-reactions').innerHTML = `<h2>Six ways to challenge the proposition.</h2><p>${escapeHTML(sim.limitation)}</p><p id="simulation-status" class="runline">Rule-based fallback · MiroFish not connected<br>${sim.agent_count} LLM agents · ${sim.reaction_count} stress-test passes · ${sim.rounds} round · independent<br>${sim.elapsed_seconds}s · $${sim.api_cost_usd} API spend · ${sim.saved_run ? 'Saved run from ' + escapeHTML(r.saved_at || 'earlier in this session') : 'Fresh local run; not saved to disk'}</p>${sim.reactions.map((x, i) => `<article class="reaction"><div><span class="mono">PASS ${String(i+1).padStart(2,'0')}</span><h3>${escapeHTML(x.lens)}</h3><span class="meta">${escapeHTML(x.audience)}</span></div><div><p><strong>Challenge:</strong> ${escapeHTML(x.objection)}</p><p><strong>Test:</strong> ${escapeHTML(x.next_test)}</p><p class="meta">Quant tool called · ${escapeHTML(x.scenario.factor)} · No proposed value without evidence.<br>Model index: ${x.quant_tool.index === null ? 'suppressed; incomplete inputs' : x.quant_tool.index.toFixed(3)}</p></div></article>`).join('')}`;
  $('scenario-benefit').value = r.brief.benefit;
  $('scenario-factor').innerHTML = '<option value="">Compare the proposition only</option>' + state.factors.filter(f => f.key !== 'price_fit').map(f => `<option value="${f.key}">${escapeHTML(f.label)}</option>`).join('');
  $('scenario-value').value = ''; $('scenario-value').disabled = true; $('scenario-value').required = false;
  $('scenario-reason').value = ''; $('scenario-reason').required = false;
  $('comparison').innerHTML = ''; selectTab('outlook');
}
function selectTab(name) {
  document.querySelectorAll('[data-tab]').forEach(b => {const active = b.dataset.tab === name; b.setAttribute('aria-selected', active); b.tabIndex = active ? 0 : -1;});
  for (const tab of ['outlook','evidence','reactions','scenario']) $('panel-' + tab).hidden = name !== tab;
}
$('example-notes').onclick = () => {$('description').value = examples.notes; $('description').focus();};
$('example-tasks').onclick = () => {$('description').value = examples.tasks; $('description').focus();};
$('back-intake').onclick = () => show('intake');
$('back-brief').onclick = () => show('brief');
$('new-assessment').onclick = () => {state.comparison = null; refreshSaved(); show('intake');};
$('intake-form').onsubmit = event => {
  event.preventDefault(); busy(event.target, 'Preparing your editable brief…', async () => {
    const draft = await api('draft', {description: $('description').value});
    for (const key of ['description','problem','benefit','geography','alternatives','channel']) $('brief-' + key).value = draft[key];
    show('brief');
  });
};
$('brief-form').onsubmit = event => {
  event.preventDefault(); busy(event.target, $('offline').checked ? 'Preparing an offline assessment…' : 'Inspecting official product pages with three concurrent source-review workers…', async () => {
    const brief = Object.fromEntries(['description','problem','benefit','geography','alternatives','channel'].map(key => [key, $('brief-' + key).value]));
    state.pack = await api('research', {brief, confirmed:true, offline:$('offline').checked});
    state.report = null; state.comparison = null; renderAudiences(); show('audiences');
  });
};
$('audience-form').onsubmit = event => {
  event.preventDefault(); busy(event.target, 'Checking quant inputs and running six independent stress tests…', async () => {
    const audiences = state.pack.audiences.map((_, i) => ({name:$(`audience-${i}-name`).value.trim(), need:$(`audience-${i}-need`).value.trim()})).filter(a => a.name || a.need);
    const factors = {};
    for (const factor of state.factors) {
      const value = $('factor-' + factor.key).value;
      if (value !== '') factors[factor.key] = {value:Number(value), provenance:'assumed', evidence_ids:[], reason:$('reason-' + factor.key).value};
    }
    state.report = await api('report', {pack_id:state.pack.version, audiences, audiences_confirmed:true, factors});
    state.comparison = null; renderReport(); show('report');
  });
};
document.querySelectorAll('[data-tab]').forEach(button => {
  button.onclick = () => selectTab(button.dataset.tab);
  button.onkeydown = event => {
    const tabs = [...document.querySelectorAll('[data-tab]')]; const current = tabs.indexOf(button);
    let next;
    if (event.key === 'ArrowRight') next = (current+1)%tabs.length;
    else if (event.key === 'ArrowLeft') next = (current+tabs.length-1)%tabs.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = tabs.length-1;
    else return;
    event.preventDefault(); selectTab(tabs[next].dataset.tab); tabs[next].focus();
  };
});
$('scenario-factor').onchange = () => {const selected = Boolean($('scenario-factor').value); $('scenario-value').disabled = !selected; $('scenario-value').required = selected; $('scenario-reason').required = selected;};
$('scenario-form').onsubmit = event => {
  event.preventDefault(); busy(event.target, 'Comparing the changed proposition with the preserved baseline…', async () => {
    const result = await api('compare', {baseline_id:state.report.id, proposition:$('scenario-benefit').value, factor:$('scenario-factor').value, value:$('scenario-value').value === '' ? null : Number($('scenario-value').value), reason:$('scenario-reason').value});
    state.comparison = result;
    const before = state.report, after = result.revised;
    $('comparison').innerHTML = `<div class="comparison">${[[before,'Baseline'],[after,'Alternative assumption']].map(([r, label]) => `<div><h3>${label}</h3><p>${escapeHTML(r.brief.benefit)}</p><p class="mono">Index: ${r.quant.index === null ? 'unscored' : r.quant.index.toFixed(3)}</p><p class="meta">${escapeHTML(r.quant.outlook)} · ${r.quant.evidence_backed}/${r.quant.total} evidence-backed factors</p></div>`).join('')}</div><p>${result.delta === null ? 'No numerical delta: at least one run has missing inputs.' : 'Heuristic index change: ' + (result.delta >= 0 ? '+' : '') + result.delta.toFixed(3) + '. Not a change in success probability.'}</p><p class="meta">${escapeHTML(result.limitation)}</p><p><strong>Next test:</strong> Put both propositions in front of people with the confirmed need. Ask which better solves their last real problem and why.</p>`;
    notice(); $('comparison').scrollIntoView({block:'nearest'});
  });
};
async function refreshSaved() {
  const response = await fetch('/api/saved');
  if (!response.ok) return;
  const runs = await response.json();
  $('saved-runs').hidden = !runs.length;
  $('saved-list').innerHTML = runs.map(r => `<button class="saved-item" data-run="${escapeHTML(r.id)}">${escapeHTML(r.benefit)}<span class="meta">Saved ${escapeHTML(r.saved_at)} · Replay cached run →</span></button>`).join('');
  document.querySelectorAll('[data-run]').forEach(button => button.onclick = () => busy($('saved-runs'), 'Loading a saved assessment; no research is being run…', async () => {
    state.report = await api('replay', {run_id: button.dataset.run}); state.comparison = null;
    renderReport(); show('report'); notice('Saved run replay. Sources and stress tests retain their original dates.');
  }));
}
$('save-run').onclick = () => busy($('report'), 'Saving this baseline locally…', async () => {
  const saved = await api('save', {report_id: state.report.id});
  state.report.saved_at = saved.saved_at; state.report.simulation.saved_run = true;
  $('save-run').textContent = 'Saved locally';
  $('simulation-status').textContent = `Rule-based fallback · 0 LLM agents · 6 independent stress-test passes · 1 round · $0 API spend · Saved locally at ${saved.saved_at}`;
  notice('Baseline saved locally. Use Saved assessments on the start screen to replay it. Export JSON to retain the comparison too.');
});
$('export').onclick = () => {
  const blob = new Blob([JSON.stringify({baseline:state.report, comparison:state.comparison, exported_at:new Date().toISOString()}, null, 2)], {type:'application/json'});
  const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `launch-assessment-${state.report.id}.json`; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
};
(async () => {
  try {const response = await fetch('/api/status'); if (!response.ok) throw new Error(); const status = await response.json(); state.token = status.token; state.factors = status.factors; $('connection').textContent = 'Local · No paid APIs'; await refreshSaved();}
  catch {notice('Cannot connect to the local server. Start server.py and reload this page.', true); $('connection').textContent = 'Disconnected'; document.querySelectorAll('button').forEach(b => b.disabled = true);}
})();
