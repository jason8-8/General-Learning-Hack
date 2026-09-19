"""MiroFish-local extraction/store/entity/profile pipeline, with provenance checks.
The upstream classes execute; adapters add source lineage and bound local calls.
"""
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent


def build(repo, model, output, progress=lambda _: None):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    os.environ.update(PYTHON_DOTENV_DISABLED='1', LLM_API_KEY='ollama-local-only',
                      LLM_BASE_URL='http://127.0.0.1:11434/v1', LLM_MODEL_NAME=model)
    sys.path.insert(0, str(Path(repo).resolve() / 'backend'))
    from app.services.graph_builder import GraphBuilderService
    from app.services.local_graph_extractor import LocalGraphExtractor
    from app.services import local_graph_store
    from app.services.entity_reader import EntityReader
    from app.services.oasis_profile_generator import OasisProfileGenerator
    from openai import OpenAI
    local_graph_store.GRAPH_DIR = str(output / 'graphs')
    started = time.monotonic()
    audit = {'engine':'MiroFish-local GraphBuilderService / LocalGraphExtractor / LocalGraphStore / EntityReader / OasisProfileGenerator',
             'model':model,'created_at':datetime.now(timezone.utc).isoformat(), 'calls':[], 'rejected':[],
             'usage':{'calls':0,'prompt_tokens':0,'completion_tokens':0},'status':'building'}
    def persist():
        audit['elapsed_seconds']=round(time.monotonic()-started,2)
        (output/'audit.json').write_text(json.dumps(audit,indent=2))
    client=OpenAI(api_key='ollama-local-only',base_url='http://127.0.0.1:11434/v1',timeout=180,max_retries=0)
    def chat(messages, temperature=.2, max_tokens=2200):
        response=client.chat.completions.create(model=model,messages=messages,temperature=temperature,
            max_tokens=max_tokens,response_format={'type':'json_object'})
        raw=response.choices[0].message.content
        audit['calls'].append({'messages':messages,'raw':raw,'finish_reason':response.choices[0].finish_reason})
        audit['usage']['calls']+=1
        for k in ('prompt_tokens','completion_tokens'):
            audit['usage'][k]+=getattr(response.usage,k,0) or 0
        persist()
        if response.choices[0].finish_reason!='stop':raise ValueError('Graph/profile output truncated')
        return json.loads(raw)
    sources=json.loads((ROOT/'travel/graph-sources.json').read_text())
    ontology={'entity_types':[{'name':s} for s in ['AudienceCohort','Product','Need','Concern','ResearchSource']],
              'edge_types':[{'name':s} for s in ['reports','has_attitude','offers','raises_concern','supports_task']]}
    builder=GraphBuilderService()
    gid=builder.create_graph('AI travel assistant research')
    # Store proper JSON; upstream set_ontology uses Python repr instead of JSON.
    store=local_graph_store.LocalGraphStore(gid)
    store.set_meta('AI travel assistant research','Published claims, not person-level truth',ontology,audit['created_at'])
    class AuditedExtractor(LocalGraphExtractor):
        def _extract_from_chunk(self,chunk,ontology_summary):
            from app.services.local_graph_extractor import EXTRACT_SYSTEM_PROMPT
            prompt=EXTRACT_SYSTEM_PROMPT+'\nUse AudienceCohort for the five named AI attitude cohorts. Put an exact supporting substring from the input in attributes.evidence_quote for EVERY entity and edge. Do not invent extra cohorts or travel preferences.'
            result=chat([{'role':'system','content':prompt},{'role':'user','content':f'Ontology: {ontology_summary}\nResearch summary:\n{chunk}'}])
            cleaned={'entities':[],'edges':[]}
            for kind in cleaned:
                for item in result.get(kind,[]):
                    allowed = {x['name'] for x in ontology['entity_types' if kind == 'entities' else 'edge_types']}
                    if item.get('type' if kind == 'entities' else 'name') not in allowed:
                        audit['rejected'].append({'source_id':self.source_id,'item':item,'reason':'Type outside declared ontology'})
                        continue
                    quote=item.get('attributes',{}).get('evidence_quote','')
                    if not quote or quote not in chunk:
                        audit['rejected'].append({'source_id':self.source_id,'item':item,'reason':'Missing exact evidence anchor'})
                        continue
                    item.setdefault('attributes',{}).update(source_id=self.source_id,provenance='LLM extraction from a recorded research summary; inspect source')
                    cleaned[kind].append(item)
            return cleaned
    extractor=AuditedExtractor(gid,ontology)
    for source in sources:
        progress('Extracting graph: '+source['id'])
        extractor.source_id=source['id']
        store.add_episode(json.dumps(source))
        extractor.extract_and_store([source['text']])
        persist()
    graph=builder.get_graph_data(gid)
    if not graph['nodes'] or not graph['edges']:raise ValueError('Extraction did not yield a usable knowledge graph')
    cohorts=EntityReader().filter_defined_entities(gid,['AudienceCohort'],True).entities
    expected={'AI Enthusiasts','AI Advocates','AI Cautious','AI Skeptics','AI Detractors'}
    cohorts=[c for c in cohorts if c.name in expected]
    if {c.name for c in cohorts}!=expected:raise ValueError('Five source-defined attitude cohorts were not extracted; inspect audit')
    class TravelProfiles(OasisProfileGenerator):
        def _generate_profile_with_llm(self,entity_name,entity_type,entity_summary,entity_attributes,context):
            result=chat([{'role':'system','content':'Create a synthetic travel-study attitude seed from the supplied knowledge-graph context. Return JSON with bio and persona only. No invented demographics, specific travel frequency, budget, employment, purchase choice or price. Preserve source uncertainty. Do not turn a general AI attitude into a prescribed product decision. Maximum 90 words.'},
                         {'role':'user','content':json.dumps({'name':entity_name,'summary':entity_summary,'attributes':entity_attributes,'graph_context':context})}],max_tokens=400)
            if not isinstance(result.get('persona'),str) or not result['persona'].strip():raise ValueError('No generated persona')
            return result
    generator=TravelProfiles(api_key='ollama-local-only',base_url='http://127.0.0.1:11434/v1',model_name=model,graph_id=gid)
    seeds=[]
    for i,entity in enumerate(sorted(cohorts,key=lambda c:c.name)):
        progress('Generating graph-based attitude seed: '+entity.name)
        seed=generator.generate_profile_from_entity(entity,i,use_llm=True)
        seeds.append({'entity_id':entity.uuid,'name':entity.name,'persona':seed.persona,'bio':seed.bio,
                      'related_edges':entity.related_edges, 'source_id':entity.attributes.get('source_id')})
    # Fully crossed study design, not inferred population weights. No duplicated profiles.
    companions=['alone','with a partner','with friends','with family','with colleagues']
    frequency=[1,2,3,5,8]
    alternatives=['search engines and maps','booking sites and saved lists','ChatGPT plus manual checking','an established personal spreadsheet']
    effort=['Usually spends 2 hours planning each trip.','Usually spends 8 hours planning each trip.']
    profiles=[]
    for seed,company,trips,alternative,time_need in itertools.product(seeds,companions,frequency,alternatives,effort):
        persona=f"{seed['persona']} Travel scenario assumptions: travels {company}, takes {trips} trips a year, currently uses {alternative}. {time_need} These are hypothetical study conditions, not sourced personal facts. Decide based on the actual offer; do not infer a purchase choice from your AI attitude alone."
        profiles.append({'id':f"G{len(profiles)+1:04d}",'label':seed['name']+' / '+company,'persona':persona,
            'sources':[seed['source_id']], 'graph_node_ids':[seed['entity_id']],
            'graph_edge_ids':[e['uuid'] for e in graph['edges'] if seed['entity_id'] in (e['source_node_uuid'],e['target_node_uuid'])],
            'scenario':{'companions':company,'trips_per_year':trips,'alternative':alternative,'planning_effort':time_need},
            'assumption':'Balanced factorial stress-test design. Equal allocation is not an estimated population distribution.'})
    random.Random(20260920).shuffle(profiles)
    for i,p in enumerate(profiles):p['id']=f'G{i+1:04d}'
    assert len(profiles)==1000 and len({p['persona'] for p in profiles})==1000
    graph.update(sources=sources,seeds=seeds,profiles=profiles,ontology=ontology,
        provenance=audit['engine'],allocation='5 graph-derived attitude cohorts × 5 travel parties × 5 trip frequencies × 4 alternatives × 2 planning-effort scenarios. All allocations are assumptions.',
        limitations=['Aggregate published research, not 1,000 real people.','Attitude seeds generated by MiroFish profile generator; travel scenarios are explicit design assumptions.','No social influence or diffusion rounds are claimed.'])
    graph['sha256']=hashlib.sha256(json.dumps(graph,sort_keys=True).encode()).hexdigest()
    (output/'graph.json').write_text(json.dumps(graph,indent=2))
    audit.update(status='completed',graph_id=gid,nodes=graph['node_count'],edges=graph['edge_count'],profiles=len(profiles));persist()
    return graph

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--model',default='qwen3-coder:30b');p.add_argument('--output',required=True);a=p.parse_args()
    build(a.repo,a.model,a.output,lambda message:print(message,flush=True))
