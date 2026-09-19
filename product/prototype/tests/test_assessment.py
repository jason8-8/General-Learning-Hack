import copy
import json
import math
from pathlib import Path
import sys
import threading
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contracts import brief_record, audiences_record, deduplicate
from quant_adapter import assess, WEIGHTS
from research import research
from assessment import build_report, compare
from server import dispatch, STATE

BRIEF = {'description': 'Voice notes into searchable actions', 'problem': 'Ideas and commitments are lost', 'benefit': 'Retrieve ideas and act on commitments'}

def full_inputs(value=.5):
    return {k: {'value': value, 'provenance': 'assumed', 'reason': 'Explicit sensitivity-test input', 'evidence_ids': []} for k in WEIGHTS}

class QuantTests(unittest.TestCase):
    def test_missing_is_not_zero_or_renormalised(self):
        q = assess({'icp_fit': {'value': 1, 'reason': 'Assumed ideal audience', 'provenance':'assumed'}})
        self.assertIsNone(q['index'])
        self.assertEqual(q['supplied'], 1)
        self.assertEqual(q['outlook'], 'insufficient evidence')
        self.assertEqual(q['factors'][1]['value'], None)
    def test_complete_assumptions_do_not_create_evidence(self):
        q = assess(full_inputs())
        self.assertAlmostEqual(q['index'], .5)
        self.assertEqual(q['evidence_backed'], 0)
        self.assertEqual(q['outlook'], 'insufficient evidence')
        self.assertNotIn('P_adopt', q)
        self.assertEqual(q, assess(full_inputs()))
    def test_invalid_numbers_and_sources_rejected(self):
        for value in [True, -1, 1.01, math.nan, math.inf, '0.5']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                assess({'icp_fit': {'value':value, 'reason':'test'}})
        with self.assertRaises(ValueError):
            assess({'icp_fit': {'value':.5, 'reason':'test','provenance':'observed'}})
        with self.assertRaises(ValueError):
            assess({'icp_fit': {'value':.5, 'reason':'test','provenance':'observed','evidence_ids':['fake']}})
    def test_rubric_boundaries(self):
        for value, label in [(.399,'weak'),(.4,'mixed'),(.699,'mixed'),(.7,'promising')]:
            rows = full_inputs(value)
            for k in list(WEIGHTS)[:4]:
                rows[k].update(provenance='inferred', evidence_ids=['real'])
            self.assertEqual(assess(rows, ['real'])['outlook'], label)
    def test_single_factor_has_expected_weighted_effect(self):
        rows = full_inputs()
        before = assess(rows)['index']
        rows['switching_ease']['value'] = .8
        self.assertAlmostEqual(assess(rows)['index'] - before, .3 * WEIGHTS['switching_ease'])

class FlowTests(unittest.TestCase):
    def setUp(self):
        self.brief = brief_record(BRIEF)
        self.pack = research(self.brief, offline=True)
        self.audiences = self.pack['audiences']
    def test_confirmation_gates(self):
        with self.assertRaises(ValueError): dispatch('/api/research', {'brief': BRIEF})
        with self.assertRaises(ValueError): dispatch('/api/report', {'pack_id':'anything'})
    def test_geography_unknown(self):
        self.assertEqual(self.brief['geography'], '')
        self.assertEqual(self.brief['language'], 'English')
    def test_baseline_immutable_and_price_disabled(self):
        baseline = build_report(self.brief, self.pack, self.audiences, full_inputs())
        snapshot = copy.deepcopy(baseline)
        change = compare(baseline, 'Retrieve and act entirely offline', 'switching_ease', .9, 'Assume migration is easier')
        self.assertEqual(baseline, snapshot)
        self.assertAlmostEqual(change['delta'], .04)
        self.assertNotEqual(change['revised']['id'], baseline['id'])
        self.assertTrue(change['revised']['evidence']['cached'])
        self.assertEqual(change['revised']['evidence']['sources'], baseline['evidence']['sources'])
        with self.assertRaises(ValueError): compare(baseline, 'Cheaper', 'price_fit', .9, 'test')
        with self.assertRaises(ValueError): compare(baseline, 'Change', 'made_up', .9, 'test')
    def test_synthetic_results_cannot_add_evidence(self):
        r = build_report(self.brief, self.pack, self.audiences, {})
        self.assertEqual(r['simulation']['agent_count'], 0)
        self.assertEqual(len(r['simulation']['reactions']), 6)
        self.assertEqual(r['quant']['supplied'], 0)
        self.assertEqual(r['evidence']['sources'], [])
        self.assertFalse(r['simulation']['mirofish'])
    def test_second_idea_without_preset(self):
        brief = brief_record({'description':'A habit coach that rebuilds routines after a missed day', 'problem':'One missed day ends the routine', 'benefit':'Restart with a smaller action'})
        pack = research(brief, offline=True)
        self.assertNotEqual(pack['audiences'], self.audiences)
        report = build_report(brief, pack, pack['audiences'], {})
        self.assertIn('habit coach', report['brief']['description'])
        self.assertNotEqual(pack['version'], self.pack['version'])
    def test_unknown_domain_no_demo_evidence(self):
        brief = brief_record({'description':'A gardening sensor', 'problem':'Dry soil', 'benefit':'Know when to water'})
        pack = research(brief)
        self.assertEqual(pack['sources'], [])
        self.assertEqual(len(pack['audiences']), 1)
    def test_sources_fetched_once_deduped_roles_and_failure_visible(self):
        calls = []
        def fetch(entry):
            title, url = entry
            calls.append(url)
            return {'title':title, 'url':url, 'roles':[], 'observation':'A real fixture, not live evidence'}
        pack = research(self.brief, fetcher=fetch)
        self.assertEqual(len(calls), 2)
        self.assertEqual(len(pack['sources']), 2)
        self.assertEqual(pack['sources'][0]['roles'], ['competitor','customer','market'])
        def fail(entry): raise OSError('Secret diagnostic must not leak')
        broken = research(self.brief, fetcher=fail)
        self.assertEqual(broken['sources'], [])
        self.assertEqual(len(broken['workers'][0]['failures']), 2)
        self.assertNotIn('Secret diagnostic', json.dumps(broken))
    def test_bad_audiences(self):
        for a in [[], [{}], [{'name':'test','need':''}]]:
            with self.assertRaises(ValueError): audiences_record(a)
    def test_dispatch_end_to_end(self):
        pack = dispatch('/api/research', {'brief':BRIEF, 'confirmed':True, 'offline':True})
        report = dispatch('/api/report', {'pack_id':pack['version'], 'audiences':pack['audiences'], 'audiences_confirmed':True})
        comparison = dispatch('/api/compare', {'baseline_id':report['id'], 'proposition':'Feature changed', 'factor':''})
        self.assertEqual(comparison['baseline_id'], report['id'])
        self.assertIsNone(comparison['delta'])

if __name__ == '__main__': unittest.main()
