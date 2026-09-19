"""Verify the actual extracted graph and population's lineage, not UI implementation."""
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import travel_service

class GraphContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=ROOT/'travel/knowledge-graph.json'
        if not p.exists():p=ROOT/'.travel-graph/graph.json'
        cls.graph=json.loads(p.read_text())
    def test_thousand_distinct_profiles_with_real_graph_lineage(self):
        g=self.graph;nodes={n['uuid'] for n in g['nodes']};edges={e['uuid'] for e in g['edges']}
        self.assertEqual(len(g['profiles']),1000)
        self.assertEqual(len({p['id'] for p in g['profiles']}),1000)
        self.assertEqual(len({p['persona'] for p in g['profiles']}),1000)
        for p in g['profiles']:
            self.assertTrue(p['graph_node_ids'])
            self.assertTrue(set(p['graph_node_ids'])<=nodes)
            self.assertTrue(set(p['graph_edge_ids'])<=edges)
    def test_graph_edges_reference_existing_nodes_and_anchored_sources(self):
        g=self.graph;nodes={n['uuid'] for n in g['nodes']};sources={s['id']:s['text'] for s in g['sources']}
        for item in g['nodes']+g['edges']:
            self.assertIn(item['attributes']['evidence_quote'],sources[item['attributes']['source_id']])
        for edge in g['edges']:
            self.assertIn(edge['source_node_uuid'],nodes)
            self.assertIn(edge['target_node_uuid'],nodes)
    def test_declared_ontology_is_enforced(self):
        g=self.graph
        node_types={x['name'] for x in g['ontology']['entity_types']}|{'Entity'}
        edge_types={x['name'] for x in g['ontology']['edge_types']}
        for n in g['nodes']:self.assertTrue(set(n['labels'])<=node_types)
        for e in g['edges']:self.assertIn(e['name'],edge_types)
    def test_graph_digest_matches_frozen_contents(self):
        g=dict(self.graph);expected=g.pop('sha256')
        self.assertEqual(expected,hashlib.sha256(json.dumps(g,sort_keys=True).encode()).hexdigest())
    def test_population_allocations_are_explicit_assumptions(self):
        self.assertIn('assumptions',self.graph['allocation'])
        self.assertEqual(len({p['scenario']['trips_per_year'] for p in self.graph['profiles']}),5)
    def test_api_rejects_invalid_scale_without_starting_job(self):
        with patch('travel_service.ACTIVE',None),patch('travel_service.threading.Thread') as thread:
            for count in (True,0,1001,'1000',-1):
                with self.assertRaises(ValueError):travel_service.launch({'count':count})
            thread.assert_not_called()

if __name__=='__main__':unittest.main()
