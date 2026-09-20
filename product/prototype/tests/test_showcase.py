import collections
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / 'quant'))
import showcase_service
from score_engine import price_fit


class ShowcaseEvidence(unittest.TestCase):
    def test_pilot_cards_reconcile_with_recorded_answers(self):
        data = showcase_service.study()
        for card, filename in zip(data['recorded_pilots'], ('pilot-10.json', 'pilot-30.json')):
            run = json.loads((ROOT / 'travel' / filename).read_text())
            counts = collections.Counter(r['answer']['decision'] for r in run['responses'])
            self.assertEqual(card['completed'], len(run['responses']))
            for choice, value in card['counts'].items():
                self.assertEqual(value, counts[choice])
            self.assertEqual(card['completed'] + card['failed'] + card['excluded'], card['requested'])
        self.assertIn('Authored', data['retrieval']['generation'])

    def test_retrieved_passages_have_real_saved_source_lineage(self):
        sources = {s['id']: s for s in json.loads((ROOT/'travel/market-sources.json').read_text())}
        passages = showcase_service.retrieve('free itinerary planning')
        self.assertTrue(passages)
        for passage in passages:
            source = sources[passage['source_id']]
            self.assertIn(passage['text'], source['text'])
            self.assertEqual(passage['url'], source['url'])
        self.assertEqual(showcase_service.retrieve('zzzznoresult'), [])

    def test_legacy_price_fit_does_not_rise_at_twice_wtp(self):
        prices = [1.9, 1.96, 1.99, 2, 2.01, 3]
        values = [price_fit(p, 1) for p in prices]
        self.assertEqual(values, sorted(values, reverse=True))
        for invalid in (float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                price_fit(invalid, 1)


if __name__ == '__main__':
    unittest.main()
