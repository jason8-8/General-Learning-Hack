'use strict';
const assert = require('node:assert/strict');
const {snapshot, compare} = require('../static/study-math.js');
const study = require('../travel/showcase-fixture.json');
const baseline = snapshot(study, 'All travellers', 'readiness', 10);
assert.equal(baseline.paid_choices, 159);
const basic = snapshot(study, 'All travellers', 'basic', 10);
assert.equal(basic.paid_choices, 31);
assert.equal(compare(baseline, basic).status, 'one_change');
assert.equal(compare(baseline, snapshot(study, 'All travellers', 'basic', 15)).status, 'multiple_changes');
assert.equal(compare(baseline, {...basic, study_id:'other'}).status, 'different_study');
assert.equal(compare(baseline, baseline).status, 'unchanged');
assert.equal(compare(null, baseline).status, 'no_baseline');
for (const segment of ['All travellers', ...study.segments.map(s => s.name)]) {
  for (const concept of ['basic', 'readiness']) {
    let last = Infinity;
    for (const price of [5, 10, 15, 20, 25, 30]) {
      const result = snapshot(study, segment, concept, price);
      assert.ok(result.paid_choices <= last);
      assert.equal(result.sample_size, segment === 'All travellers' ? 1000 : 200);
      last = result.paid_choices;
    }
  }
}
assert.equal(baseline.paid_choices, 159); // Later selections did not mutate the baseline.
assert.throws(() => snapshot(study, 'missing audience', 'basic', 10));
assert.throws(() => snapshot(study, 'All travellers', 'unknown', 10));
assert.throws(() => snapshot(study, 'All travellers', 'basic', NaN));
console.log('Scenario checks passed: baseline, one-change attribution, concept, audience, monotonicity and invalid inputs.');
