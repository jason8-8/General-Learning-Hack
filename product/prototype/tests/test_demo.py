import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server
from research import classify
from quant_adapter import WEIGHTS

class DemoTests(unittest.TestCase):
    def make_report(self):
        demo = json.loads((server.ROOT / 'demo.json').read_text())
        pack = server.dispatch('/api/research', {'brief':demo['brief'], 'confirmed':True, 'demo':True})
        factors = {k: {'value':.5,'provenance':'assumed','reason':'Illustrative demo input'} for k in WEIGHTS}
        report = server.dispatch('/api/report', {'pack_id':pack['version'], 'audiences':pack['audiences'], 'audiences_confirmed':True,'factors':factors})
        return pack,report
    def test_guided_demo_uses_recorded_sources_without_network(self):
        with patch('research.urlopen', side_effect=AssertionError('No network in demo')):
            pack,report = self.make_report()
        self.assertTrue(pack['cached'])
        self.assertTrue(pack['demo'])
        self.assertEqual(len(pack['sources']), 2)
        self.assertEqual(report['quant']['index'], .5)
        self.assertEqual(report['quant']['evidence_backed'], 0)
        self.assertEqual(report['quant']['outlook'], 'insufficient evidence')
    def test_save_and_replay_restores_comparison_after_memory_loss(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(server,'RUNS',Path(directory)):
            pack,report=self.make_report()
            comparison=server.dispatch('/api/compare',{'baseline_id':report['id'],'proposition':'Import existing notes','factor':'switching_ease','value':.9,'reason':'Illustrative assumption'})
            server.dispatch('/api/save',{'report_id':report['id'],'comparison_id':comparison['revised']['id']})
            for collection in server.STATE.values(): collection.clear()
            replay=server.dispatch('/api/replay',{'run_id':report['id']})
            self.assertEqual(replay['quant']['index'],.5)
            self.assertEqual(replay['comparison']['revised']['quant']['index'],.54)
            self.assertEqual(replay['comparison']['delta'],.04)
            self.assertTrue(replay['comparison']['revised']['simulation']['saved_run'])
            self.assertEqual(replay['evidence']['sources'],pack['sources'])
            server.dispatch('/api/save',{'report_id':report['id'],'comparison_id':comparison['revised']['id']})
    def test_unsupported_idea_rejected_before_generic_report(self):
        with self.assertRaisesRegex(ValueError,'currently supports'):
            server.dispatch('/api/research',{'brief':{'description':'AI sports coaching','problem':'Coaching is expensive','benefit':'Help athletes improve'},'confirmed':True})
    def test_substrings_are_not_categories(self):
        for description in ['An invoice tool', 'A product already used by teams', 'A planet viewer']:
            self.assertIsNone(classify({'description':description,'benefit':''}))
        self.assertEqual(classify({'description':'A planner for tasks already missed','benefit':''}),'tasks')
        self.assertEqual(classify({'description':'Searchable voice notes','benefit':''}),'notes')

if __name__ == '__main__': unittest.main()
