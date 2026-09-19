import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from tempfile import TemporaryDirectory
import travel_service
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from travel_runner import parse_answer
from travel_service import validate_feedback, read, DATA, get

class TravelContracts(unittest.TestCase):
    def answer(self):
        return {'decision':'free_only','reason':'Already use maps','valuable_feature':'Updates','objection':'Accuracy','next_test':'Observe a planning session','scenario':{'hours_saved_per_trip':2,'trips_per_year':3,'value_per_hour_gbp':10,'rationale':'Illustrative'}}
    def test_invalid_answers_excluded(self):
        for field,value in [('decision','definitely_buy'),('reason','')]:
            a=self.answer();a[field]=value
            with self.assertRaises(ValueError):parse_answer(json.dumps(a))
        a=self.answer();a['scenario']['hours_saved_per_trip']=float('nan')
        with self.assertRaises(ValueError):parse_answer(json.dumps(a))
    def test_valid_answer(self):
        self.assertEqual(parse_answer(json.dumps(self.answer()))['decision'],'free_only')
    def test_feedback_cannot_change_offer_or_profile(self):
        p=read(DATA/'study.json');p['id']='baseline'
        f={'profile_id':'T01','observation':'Planning happens in group chat','collected_at':'2026-09-20','recruitment':'Illustrative one case','offer_tested':p['offer'],'kind':'illustrative','decision':'free_only'}
        self.assertEqual(validate_feedback(f,p)['baseline_id'],'baseline')
        self.assertEqual(p['profiles'][0]['persona'],read(DATA/'study.json')['profiles'][0]['persona'])
        for key,value in [('offer_tested','Different offer'),('profile_id','T99'),('collected_at','2026-13-99')]:
            with self.assertRaises(ValueError):validate_feedback({**f,key:value},p)
    def test_shape_errors_rejected(self):
        for data in ([], {'decision':'free_only','reason':'x','valuable_feature':'x','objection':'x','next_test':'x','scenario':[]}):
            with self.assertRaises(ValueError):parse_answer(json.dumps(data))
    def test_worker_failure_accounts_for_each_unfinished_profile(self):
        with TemporaryDirectory() as folder:
            directory=Path(folder)
            initial={'profiles':[{'id':'T01'},{'id':'T02'}], 'responses':[], 'failed':[], 'excluded':[]}
            (directory/'result.json').write_text(json.dumps(initial))
            with patch('travel_service.subprocess.run',side_effect=RuntimeError('Engine unavailable')):
                travel_service.work(directory,{'python':'missing','repo':'missing','model':'test'})
            result=read(directory/'result.json')
            self.assertEqual(result['status'],'failed')
            self.assertEqual(len(result['failed']),2)
            self.assertIsNone(travel_service.ACTIVE)
    def test_recordings_are_complete_and_baseline_preserved(self):
        b=get('recorded');r=get('recorded-revision')
        self.assertEqual(r['parent_id'], b['id'])
        self.assertEqual(b['profiles'][1:],r['profiles'][1:])
        self.assertNotEqual(b['profiles'][0]['persona'],r['profiles'][0]['persona'])
        self.assertFalse(b.get('feedback'))
        for record in (b,r):
            self.assertEqual(record['completed'],6)
            self.assertEqual(record['usage']['calls'],6)
            for response in record['responses']:
                a=response['answer']['scenario']
                self.assertEqual(response['calculation']['annual_time_value_gbp'],round(a['hours_saved_per_trip']*a['trips_per_year']*a['value_per_hour_gbp'],2))
    def test_invalid_pilot_price_never_starts_job(self):
        with patch('travel_service.ACTIVE', None), patch('travel_service.threading.Thread') as thread:
            for price in (True, 0, -1, 999, '10'):
                with self.assertRaises(ValueError):
                    travel_service.launch({'count':20,'price_gbp_per_trip':price})
            thread.assert_not_called()

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError):get('../../server.py')

if __name__=='__main__':unittest.main()
