import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server
from research import TextParser

class SavedRunTests(unittest.TestCase):
    def test_save_replay_keeps_original_dates_and_labels_cache(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(server, 'RUNS', Path(directory)):
            pack = server.dispatch('/api/research', {'brief': {'description':'Voice notes', 'problem':'Lost ideas', 'benefit':'Find ideas'},'confirmed':True,'offline':True})
            report = server.dispatch('/api/report', {'pack_id':pack['version'],'audiences':pack['audiences'],'audiences_confirmed':True})
            saved = server.dispatch('/api/save', {'report_id':report['id']})
            replay = server.dispatch('/api/replay', {'run_id':saved['id']})
            self.assertTrue(replay['evidence']['cached'])
            self.assertTrue(replay['simulation']['saved_run'])
            self.assertEqual(replay['evidence']['version'], report['evidence']['version'])
            self.assertEqual(replay['simulation']['reactions'], report['simulation']['reactions'])
            self.assertEqual(replay['saved_at'], saved['saved_at'])
            self.assertFalse(report['evidence']['cached'])
            self.assertFalse(report['simulation']['saved_run'])
            with self.assertRaises(ValueError): server.dispatch('/api/replay', {'run_id':'../../secrets'})
    def test_description_and_scripts(self):
        parser = TextParser()
        parser.feed('<meta name="description" content="Keep your notes private."><script>hidden</script><p>Visible</p>')
        self.assertEqual(parser.descriptions, ['Keep your notes private.'])
        self.assertEqual(parser.parts, ['Visible'])
if __name__ == '__main__': unittest.main()
