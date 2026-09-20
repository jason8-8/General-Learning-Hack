'use strict';
// Pure calculations shared by the UI and offline regression checks.
const StudyMath = (() => {
  function snapshot(study, segment, concept, price) {
    const rows = study.respondents.filter(p => segment === 'All travellers' || p.segment === segment);
    if (!rows.length || !['basic', 'readiness'].includes(concept) || !Number.isFinite(price) || price <= 0) {
      throw new Error('Invalid scenario selection');
    }
    const field = concept === 'basic' ? 'basic_max_gbp_per_trip' : 'max_gbp_per_trip';
    const paid = rows.filter(p => p[field] >= price).length;
    return {study_id: study.id, segment, concept, price_gbp_per_trip: price,
      paid_choices: paid, sample_size: rows.length, share: paid / rows.length,
      provenance: 'Authored sensitivity scenario; not observed or model-generated demand'};
  }
  function compare(baseline, current) {
    if (!baseline) return {status: 'no_baseline', changes: []};
    const changes = ['segment', 'concept', 'price_gbp_per_trip'].filter(k => baseline[k] !== current[k]);
    const sameStudy = baseline.study_id === current.study_id;
    return {status: !sameStudy ? 'different_study' : changes.length > 1 ? 'multiple_changes' : changes.length === 0 ? 'unchanged' : 'one_change',
      changes, delta_percentage_points: sameStudy ? (current.share - baseline.share) * 100 : null};
  }
  return {snapshot, compare};
})();
if (typeof module !== 'undefined') module.exports = StudyMath;
