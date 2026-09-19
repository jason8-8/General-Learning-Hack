'use strict';
const $ = id => document.getElementById(id);
const escapeHTML = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const state = {token: '', factors: [], pack: null, report: null, comparison: null, demo: false};
const examples = {
  notes: 'A voice-note app that turns spoken thoughts into searchable notes and action items, so useful ideas do not disappear before I act on them.',
  tasks: 'A personal planner that rearranges unfinished tasks around changing energy levels and available time, so people can recover when their day goes off plan.'
};
function notice(text = '', error = false) { $('notice').hidden = !text; $('notice').textContent = text; $('notice').dataset.error = error; }
const stages = ['intake', 'brief', 'audiences', 'report'];
const available = {intake: true, brief: false, audiences: false, report: false};
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const context = {
  intake: ['Start with the change.', 'What gets better for the person using your product? Keep that promise in view as you test it.'],
  brief: ['A promise, made concrete.', 'You control the brief. Research starts only after you confirm the problem and the benefit.'],
  audiences: ['Separate claims from evidence.', 'Read what was actually retrieved. Then choose whose need to investigate. Audience suggestions remain hypotheses.'],
  report: ['A decision you can inspect.', 'Follow the inputs into the result. Challenge the proposition, then compare one deliberate change.']
};
let activeStage = 'intake';
function setContext(stage) {
  activeStage = stage;
  document.querySelectorAll('.chapter').forEach(el => el.classList.toggle('is-active', el.id === stage));
  for (const name of stages) {
    $('nav-' + name).removeAttribute('aria-current');
    $('nav-' + name).classList.toggle('is-unlocked', available[name]);
  }
  $('nav-' + stage).setAttribute('aria-current', 'step');
  $('context-title').textContent = context[stage][0];
  $('context-copy').textContent = context[stage][1];
  $('map-progress').style.transform = `scaleX(${stages.indexOf(stage) / 3})`;
  document.querySelector('.journey-map').dataset.step = String(stages.indexOf(stage));
}
function syncContext() {
  const idea = available.brief ? $('brief-benefit').value || $('brief-description').value : $('description').value;
  $('pinned-idea').textContent = idea || state.report?.brief.benefit || 'A thought worth testing.';
  $('context-facts').textContent = state.report ? `${state.report.evidence.sources.length} sources · ${state.report.quant.supplied}/8 inputs · ${state.report.simulation.agent_count} LLM agents` : state.pack ? `${state.pack.sources.length} sources · Audience review next` : state.demo ? 'Guided example · Recorded sources' : 'Local prototype · No paid calls';
  for (const name of stages.slice(1)) {
    $('body-' + name).hidden = !available[name];
    $('lock-' + name).hidden = available[name];
  }
  $('report-preview').hidden = available.report;
  setContext(activeStage);
}
function invalidateFrom(stage) {
  for (const name of stages.slice(stages.indexOf(stage))) available[name] = false;
  if (stages.indexOf(stage) <= 2) state.pack = null;
  state.report = null; state.comparison = null;
  syncContext();
}
function moveTo(id) {
  const target = $(id);
  target.scrollIntoView({behavior: reduceMotion.matches ? 'instant' : 'smooth', block: 'start'});
  const heading = target.querySelector('h1, h2') || target;
  heading.tabIndex = -1; heading.focus({preventScroll: true});
}
function show(step) {
  available[step] = true;
  updateGuide(step); syncContext(); setContext(step); notice();
  requestAnimationFrame(() => moveTo(step));
}
const chapterObserver = new IntersectionObserver(entries => {
  const entering = entries.filter(entry => entry.isIntersecting).sort((a,b) => a.boundingClientRect.top - b.boundingClientRect.top);
  if (entering.length) setContext(entering[0].target.dataset.stage);
}, {rootMargin: '-15% 0px -55% 0px', threshold: 0});
document.querySelectorAll('.chapter').forEach(section => chapterObserver.observe(section));
document.querySelectorAll('[data-jump]').forEach(button => button.onclick = () => moveTo(button.dataset.jump));
$('description').addEventListener('input', () => {invalidateFrom('brief');});
$('brief-form').addEventListener('input', () => {if (state.pack || state.report) invalidateFrom('audiences'); else syncContext();});
$('audience-form').addEventListener('input', () => {if (state.report) invalidateFrom('report');});
async function api(path, data) {
  const response = await fetch('/api/' + path, {method: 'POST', headers: {'Content-Type': 'application/json', 'X-Session-Token': state.token}, body: JSON.stringify(data)});
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || 'The request failed. Retry this step.');
  return body;
}
async function busy(form, message, action) {
  const buttons = [...document.querySelectorAll('button')];
  const disabled = buttons.map(b => b.disabled); buttons.forEach(b => b.disabled = true);
  form.prepend($('notice'));
  form.setAttribute('aria-busy', 'true'); notice(message);
  try { await action(); } catch (error) { notice(error.message, true); $('notice').scrollIntoView({block:'nearest', behavior: 'instant'}); }
  finally { buttons.forEach((b, i) => b.disabled = disabled[i]); form.removeAttribute('aria-busy'); }
}
function evidenceHTML(pack) {
  return `<p class="runline">${escapeHTML(pack.mode)} · ${pack.sources.length} unique sources · ${pack.elapsed_seconds}s · $0 API spend${pack.cached ? ' · recorded evidence' : ''}</p>` +
    pack.sources.map(s => `<article class="source" data-source="${escapeHTML(s.id)}"><h3><a href="${escapeHTML(s.url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(s.title)} ↗</a></h3><div class="meta mono">${escapeHTML(s.id)} · ${escapeHTML(s.provenance)} · ${escapeHTML(s.roles.join(', '))}</div><blockquote>${escapeHTML(s.observation)}</blockquote><p>${escapeHTML(s.supported_claim)}</p><p class="meta">${escapeHTML(s.limitation)}<br>Retrieved ${escapeHTML(s.retrieved_at)} · Publication date: ${escapeHTML(s.publication_date || 'unknown')}</p></article>`).join('') +
    (!pack.sources.length ? '<p class="empty">No evidence retrieved. All missing inputs remain unscored.</p>' : '') +
    '<h2>Research gaps</h2>' + pack.workers.map(w => `<p><strong>${escapeHTML(w.role)}</strong> · ${escapeHTML(w.gap)}</p>${w.failures.map(f => `<p class="meta">${escapeHTML(f.url)} · ${escapeHTML(f.reason)}</p>`).join('')}`).join('');
}
function updateGuide(step) {
  const guideHost = step === 'intake' ? $('intake') : $('body-' + step);
  guideHost.prepend($('demo-guide'));
  $('demo-guide').hidden = !state.demo || step === 'intake';
  $('offline').parentElement.hidden = state.demo;
  $('brief-mode-note').textContent = state.demo ? 'Prewritten example. Review and confirm it before continuing.' : 'No LLM connected. Your description is preserved below. Add the problem and refine the benefit.';
  $('research-mode-note').textContent = state.demo ? 'The unchanged example uses recorded Voicenotes and Obsidian excerpts. It does not make live research or model calls.' : 'Live mode checks a small catalogue of official product pages. Open-web search and independent customer research are not connected.';
  const steps = {
    brief: ['1 / 4 · Confirm the example', 'This is a prewritten demonstration brief, not LLM output. Check the problem and benefit, then confirm to inspect recorded vendor sources. Editing it switches research to the normal live catalogue.'],
    audiences: ['2 / 4 · Inspect the evidence and inputs', 'Open the source panel to see real recorded excerpts. Review the three audience hypotheses. To demonstrate the arithmetic, open Add explicit quant inputs and choose Use illustrative demo assumptions. Then confirm the audiences.'],
    report: ['Follow the inputs into the result', 'If you used all eight illustrative inputs at 0.50, the index is 0.500. Keep scrolling to inspect the sources, challenge the idea and compare a changed assumption. Sample assumptions are not evidence.']
  };
  if (steps[step]) { $('demo-step').textContent = steps[step][0]; $('demo-explanation').textContent = steps[step][1]; }
}
$('start-demo').onclick = () => busy($('intake'), 'Loading the guided example…', async () => {
  const response = await fetch('/api/demo');
  if (!response.ok) throw new Error('Could not load the demo. Restart the updated server and reload.');
  const demo = await response.json(); invalidateFrom('brief'); state.demo = true;
  $('description').value = demo.brief.description;
  for (const key of ['description','problem','benefit','geography','alternatives','channel']) $('brief-' + key).value = demo.brief[key];
  $('offline').checked = false; show('brief');
});
$('demo-assumptions').onclick = () => {
  if (state.report) invalidateFrom('report');
  for (const f of state.factors) { $('factor-' + f.key).value = '0.50'; $('reason-' + f.key).value = 'Illustrative demo assumption only; not supported by product evidence.'; }
  $('audience-form').prepend($('notice'));
  notice('All eight factors are now 0.50 for demonstration only. Review them before confirming.');
};
$('demo-scenario').onclick = () => {
  $('scenario-benefit').value = 'Turn voice notes into searchable actions, with one-step import from your existing notes.';
  $('scenario-factor').value = 'switching_ease'; $('scenario-factor').onchange();
  $('scenario-value').value = '0.90';
  $('scenario-reason').value = 'Illustrative assumption: one-step import makes switching easier. This has not been tested with users.';
};
function renderAudiences() {
  const p = state.pack;
  $('demo-assumptions').closest('details').open = state.demo;
  $('demo-assumptions').hidden = !state.demo; $('demo-assumption-note').hidden = !state.demo;
  $('research-summary').innerHTML = `<p class="runline">${p.sources.length} unique sources · ${p.demo ? 'Recorded demo pack; no new research' : 'Three concurrent source-review workers'} · ${p.elapsed_seconds}s<br>Suggestions below are rule-based hypotheses. No customer evidence has been inferred from vendor pages.</p>`;
  $('evidence-before').innerHTML = evidenceHTML(p);
  $('audience-fields').innerHTML = p.audiences.map((a, i) => `<div class="audience-edit"><div class="columns"><div><label for="audience-${i}-name">Need-based group ${i + 1}</label><input id="audience-${i}-name" maxlength="800" value="${escapeHTML(a.name)}"></div><div><label for="audience-${i}-need">What they need</label><textarea id="audience-${i}-need" rows="2" maxlength="800">${escapeHTML(a.need)}</textarea></div></div></div>`).join('');
  $('factor-fields').innerHTML = state.factors.map(f => `<div class="factor-entry"><span class="factor-name">${escapeHTML(f.label)}<br><span class="meta mono">weight ${f.weight.toFixed(2)}</span></span><div><label for="factor-${f.key}">Value 0–1</label><input id="factor-${f.key}" type="number" min="0" max="1" step="0.01" aria-label="${escapeHTML(f.label)} value"></div><div><label for="reason-${f.key}">Assumption and reason</label><input id="reason-${f.key}" maxlength="1000" placeholder="Leave blank when unknown" aria-label="${escapeHTML(f.label)} reason"></div></div>`).join('');
}
function citations(ids) {return ids.length ? `<p class="meta mono">Sources: ${ids.map(escapeHTML).join(', ')}</p>` : '';}
function renderReport() {
  const r = state.report, q = r.quant;
  $('demo-scenario').hidden = !state.demo;
  $('report-proposition').textContent = r.brief.benefit;
  $('save-run').textContent = r.saved_at ? 'Saved locally' : 'Save run';
  $('report-overview').innerHTML = `<div class="overview"><div class="metric"><span class="meta">Commercial outlook</span><strong>${escapeHTML(q.outlook[0].toUpperCase() + q.outlook.slice(1))}</strong><span class="meta">Heuristic assessment, unvalidated</span></div><div class="metric"><span class="meta">Evidence coverage</span><strong class="mono">${q.evidence_backed} / ${q.total}</strong><span class="meta">Factors supported by cited evidence</span></div><div class="metric"><span class="meta">Model index</span><strong class="mono">${q.index === null ? 'Unscored' : q.index.toFixed(3)}</strong><span class="meta">${q.supplied} / ${q.total} inputs supplied${q.index !== null ? ' · not a probability' : ''}</span></div></div>`;
  $('panel-outlook').innerHTML = `<h2>Priority audiences to test</h2><p class="meta">Founder-confirmed hypotheses, in your chosen order.</p>${r.audiences.map((a, i) => `<p><strong>${i+1}. ${escapeHTML(a.name)}</strong><br>${escapeHTML(a.need)}</p>`).join('')}<details class="report-details"><summary>Commercial outlook, unknowns and next research</summary><div class="report-grid">${r.sections.map(s => `<article><h3>${escapeHTML(s.title)}</h3><p>${escapeHTML(s.text)}</p>${citations(s.evidence_ids)}</article>`).join('')}</div></details><h2>Follow the calculation</h2><p class="meta">Unknown is not zero. Missing factors suppress the aggregate; weights are not redistributed.</p><div class="table-wrap"><table><thead><tr><th>Factor</th><th>Weight</th><th>Value</th><th>Provenance / reason</th></tr></thead><tbody>${q.factors.map(f => `<tr><td>${escapeHTML(f.label)}</td><td class="mono">${f.weight.toFixed(2)}</td><td class="mono">${f.value === null ? '—' : f.value.toFixed(2)}</td><td>${escapeHTML(f.provenance)}${f.reason ? '<br>' + escapeHTML(f.reason) : ''}${citations(f.evidence_ids)}</td></tr>`).join('')}</tbody></table></div><details><summary>Assessment rubric & assumptions</summary><p>${escapeHTML(q.rubric)}</p><ul>${r.assumptions.map(a => `<li>${escapeHTML(a)}</li>`).join('')}</ul><p>No historical launch-outcome dataset is available. Predictive accuracy has not been measured.</p></details><h2>What to do next</h2><ol class="steps">${r.next_tests.map(t => `<li><strong>${escapeHTML(t.title)}</strong><p>${escapeHTML(t.action)}</p></li>`).join('')}</ol>`;
  $('panel-evidence').innerHTML = '<div class="chapter-heading"><p class="chapter-kicker">Trace it back</p><h2>Every claim needs<br>somewhere to stand.</h2><p>Open the original page. Check the dates. See precisely what each source can and cannot support.</p></div>' + evidenceHTML(r.evidence);
  const sim = r.simulation;
  $('panel-reactions').innerHTML = `<div class="chapter-heading"><p class="chapter-kicker">Pressure, before conviction</p><h2>Give the idea<br>some resistance.</h2></div><p>${escapeHTML(sim.limitation)}</p><p id="simulation-status" class="runline">Rule-based fallback · MiroFish not connected<br>${sim.agent_count} LLM agents · ${sim.reaction_count} stress-test passes · ${sim.rounds} round · independent<br>${sim.elapsed_seconds}s · $${sim.api_cost_usd} API spend · ${sim.saved_run ? 'Saved run from ' + escapeHTML(r.saved_at || 'earlier in this session') : 'Fresh local run; not saved to disk'}</p>${sim.reactions.map((x, i) => `<article class="reaction"><div><span class="mono">PASS ${String(i+1).padStart(2,'0')}</span><h3>${escapeHTML(x.lens)}</h3><span class="meta">${escapeHTML(x.audience)}</span></div><div><p><strong>Challenge:</strong> ${escapeHTML(x.objection)}</p><p><strong>Test:</strong> ${escapeHTML(x.next_test)}</p><p class="meta">Quant tool called · ${escapeHTML(x.scenario.factor)} · No proposed value without evidence.<br>Model index: ${x.quant_tool.index === null ? 'suppressed; incomplete inputs' : x.quant_tool.index.toFixed(3)}</p></div></article>`).join('')}`;
  $('scenario-benefit').value = r.brief.benefit;
  $('scenario-factor').innerHTML = '<option value="">Compare the proposition only</option>' + state.factors.filter(f => f.key !== 'price_fit').map(f => `<option value="${f.key}">${escapeHTML(f.label)}</option>`).join('');
  $('scenario-value').value = ''; $('scenario-value').disabled = true; $('scenario-value').required = false;
  $('scenario-reason').value = ''; $('scenario-reason').required = false;
  $('comparison').innerHTML = '';
  for (const tab of ['outlook','evidence','reactions','scenario']) $('panel-' + tab).hidden = false;
}
function selectTab(name) {
  document.querySelectorAll('[data-tab]').forEach(button => button.toggleAttribute('data-current', button.dataset.tab === name));
  moveTo('panel-' + name);
}
$('example-notes').onclick = () => {$('description').value = examples.notes; $('description').focus();};
$('example-tasks').onclick = () => {$('description').value = examples.tasks; $('description').focus();};
$('back-intake').onclick = () => show('intake');
$('back-brief').onclick = () => show('brief');
$('new-assessment').onclick = () => {invalidateFrom('brief'); state.demo = false; refreshSaved().catch(() => notice('Saved runs could not be loaded. Reload to retry.', true)); show('intake');};
$('intake-form').onsubmit = event => {
  event.preventDefault(); busy(event.target, 'Preparing your editable brief…', async () => {
    invalidateFrom('brief'); state.demo = false;
    const draft = await api('draft', {description: $('description').value});
    for (const key of ['description','problem','benefit','geography','alternatives','channel']) $('brief-' + key).value = draft[key];
    show('brief');
  });
};
$('brief-form').onsubmit = event => {
  event.preventDefault(); busy(event.target, state.demo ? 'Loading the recorded demo sources…' : $('offline').checked ? 'Preparing an offline assessment…' : 'Inspecting official product pages with three concurrent source-review workers…', async () => {
    const brief = Object.fromEntries(['description','problem','benefit','geography','alternatives','channel'].map(key => [key, $('brief-' + key).value]));
    state.pack = await api('research', {brief, confirmed:true, offline:$('offline').checked, demo:state.demo});
    state.demo = Boolean(state.pack.demo);
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
document.querySelectorAll('[data-tab]').forEach(button => button.onclick = () => selectTab(button.dataset.tab));
$('scenario-factor').onchange = () => {const selected = Boolean($('scenario-factor').value); $('scenario-value').disabled = !selected; $('scenario-value').required = selected; $('scenario-reason').required = selected;};
$('scenario-form').onsubmit = event => {
  event.preventDefault(); busy(event.target, 'Comparing the changed proposition with the preserved baseline…', async () => {
    const result = await api('compare', {baseline_id:state.report.id, proposition:$('scenario-benefit').value, factor:$('scenario-factor').value, value:$('scenario-value').value === '' ? null : Number($('scenario-value').value), reason:$('scenario-reason').value});
    state.comparison = result;
    renderComparison(result); syncContext();
    $('save-run').textContent = 'Save comparison';
    notice(); $('comparison').scrollIntoView({block:'nearest'});
  });
};
function renderComparison(result) {
  $('scenario-benefit').value = result.revised.brief.benefit;
  $('scenario-factor').value = result.changed_factor || '';
  $('scenario-factor').onchange();
  const input = result.changed_factor ? result.revised.factor_inputs[result.changed_factor] : null;
  $('scenario-value').value = input?.value ?? '';
  $('scenario-reason').value = input?.reason || '';
  const before = state.report, after = result.revised;
  $('comparison').innerHTML = `<div class="comparison">${[[before,'Baseline'],[after,'Alternative assumption']].map(([r, label]) => `<div><h3>${label}</h3><p>${escapeHTML(r.brief.benefit)}</p><p class="mono">Index: ${r.quant.index === null ? 'unscored' : r.quant.index.toFixed(3)}</p><p class="meta">${escapeHTML(r.quant.outlook)} · ${r.quant.evidence_backed}/${r.quant.total} evidence-backed factors</p></div>`).join('')}</div><p>${result.delta === null ? 'No numerical delta: at least one run has missing inputs.' : 'Heuristic index change: ' + (result.delta >= 0 ? '+' : '') + result.delta.toFixed(3) + '. Not a change in success probability.'}</p><p class="meta">${escapeHTML(result.limitation)}</p><p><strong>Next test:</strong> Put both propositions in front of people with the confirmed need. Ask which better solves their last real problem and why.</p>`;
}
async function refreshSaved() {
  const response = await fetch('/api/saved');
  if (!response.ok) return;
  const runs = await response.json();
  $('saved-runs').hidden = !runs.length;
  $('saved-list').innerHTML = runs.map(r => `<button class="saved-item" data-run="${escapeHTML(r.id)}">${escapeHTML(r.benefit)}<span class="meta">Saved ${escapeHTML(r.saved_at)} · Replay cached run →</span></button>`).join('');
  document.querySelectorAll('[data-run]').forEach(button => button.onclick = () => busy($('saved-runs'), 'Loading a saved assessment; no research is being run…', async () => {
    invalidateFrom('brief');
    state.report = await api('replay', {run_id: button.dataset.run}); state.comparison = state.report.comparison || null; state.demo = Boolean(state.report.evidence.demo);
    delete state.report.comparison;
    for (const key of ['description','problem','benefit','geography','alternatives','channel']) $('brief-' + key).value = state.report.brief[key];
    $('description').value = state.report.brief.description; available.brief = true;
    renderReport(); if (state.comparison) renderComparison(state.comparison); show('report'); notice('Saved run replay. Sources and stress tests retain their original dates.');
  }));
}
$('save-run').onclick = () => busy($('body-report'), 'Saving this baseline locally…', async () => {
  const saved = await api('save', {report_id: state.report.id, comparison_id: state.comparison?.revised.id || null});
  state.report.saved_at = saved.saved_at; state.report.simulation.saved_run = true;
  $('save-run').textContent = 'Saved locally';
  $('simulation-status').textContent = `Rule-based fallback · 0 LLM agents · 6 independent stress-test passes · 1 round · $0 API spend · Saved locally at ${saved.saved_at}`;
  notice(state.comparison ? 'Baseline and comparison saved locally. Both will be restored when you replay this assessment.' : 'Baseline saved locally. Use Saved assessments on the start screen to replay it.');
});
$('export').onclick = () => {
  const blob = new Blob([JSON.stringify({baseline:state.report, comparison:state.comparison, exported_at:new Date().toISOString()}, null, 2)], {type:'application/json'});
  const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `launch-assessment-${state.report.id}.json`; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
};
(async () => {
  try {const response = await fetch('/api/status'); if (!response.ok) throw new Error(); const status = await response.json(); state.token = status.token; state.factors = status.factors; $('connection').textContent = 'Local · No paid APIs'; await refreshSaved(); syncContext();}
  catch {notice('Cannot connect to the local server. Start server.py and reload this page.', true); $('connection').textContent = 'Disconnected'; document.querySelectorAll('button').forEach(b => b.disabled = true);}
})();
