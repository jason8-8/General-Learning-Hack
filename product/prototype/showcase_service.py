"""Authored presentation fixture and real lexical retrieval. No model calls."""
from pathlib import Path
import json
import re
ROOT = Path(__file__).resolve().parent

def retrieve(query, limit=3):
    terms = set(re.findall(r'[a-z]{3,}', query.lower())) - {'the','and','for','with','that','this'}
    chunks = []
    for source in json.loads((ROOT/'travel/market-sources.json').read_text()):
        for i, text in enumerate(re.split(r'(?<=\.)\s+', source['text'])):
            words = set(re.findall(r'[a-z]{3,}', text.lower()))
            score = len(terms & words)
            if score:
                chunks.append({'id':f"{source['id']}-{i+1}",'source_id':source['id'],'title':source['title'],
                    'url':source['url'],'text':text,'score':score,'kind':'Saved research summary, not a verbatim publisher quote'})
    return sorted(chunks,key=lambda x:(-x['score'],x['id']))[:limit]

def study(query='travel planning itinerary control privacy'):
    fixture = json.loads((ROOT/'travel/showcase-fixture.json').read_text())
    pilots = []
    for filename in ('pilot-10.json', 'pilot-30.json'):
        run = json.loads((ROOT/'travel'/filename).read_text())
        pilots.append({key:run[key] for key in ('id', 'created_at', 'price_gbp_per_trip', 'requested', 'completed', 'counts', 'engine', 'model')})
        pilots[-1].update(failed=len(run['failed']), excluded=len(run['excluded']))
    return {**fixture,'recorded_pilots':pilots,'retrieval':{'query':query,'method':'Sentence chunks ranked by count of shared unique keywords; deterministic lexical retrieval, no embeddings',
        'chunks':retrieve(query),'generation':'Authored response fixtures. Retrieved passages are displayed as context; they did not generate these responses.'}}
