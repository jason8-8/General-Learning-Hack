"""Three concurrent bounded source-review workers. No open-web search is claimed."""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
import re
import time
from urllib.request import Request, urlopen
from contracts import deduplicate, fingerprint

CATALOGUE = {
    'notes': [('Voicenotes', 'https://voicenotes.com/'), ('Obsidian', 'https://obsidian.md/')],
    'tasks': [('Todoist', 'https://www.todoist.com/'), ('TickTick', 'https://ticktick.com/')],
}

class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []
        self.descriptions = []
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'meta' and (attributes.get('name') == 'description' or attributes.get('property') == 'og:description'):
            if attributes.get('content'):
                self.descriptions.append(attributes['content'])
        if tag in ('script', 'style', 'noscript', 'svg'):
            self.hidden += 1
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript', 'svg'):
            self.hidden = max(0, self.hidden - 1)
    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.parts.append(data.strip())

def fetch_source(entry):
    title, url = entry
    request = Request(url, headers={'User-Agent': 'LaunchAssessmentPrototype/1.0 (source inspection)'})
    with urlopen(request, timeout=10) as response:
        if 'text/html' not in response.headers.get('Content-Type', ''):
            raise ValueError('Source is not an HTML page')
        raw = response.read(1_000_000).decode('utf-8', errors='replace')
    parser = TextParser()
    parser.feed(raw)
    text = re.sub(r'\s+', ' ', ' '.join(parser.parts)).strip()
    if len(text) < 80:
        raise ValueError('Page has insufficient readable text')
    # Short, exact extract. No invented summary or inferred numerical factors.
    sentences = re.split(r'(?<=[.!?])\s+', text)
    relevant = next((s for s in sentences if re.search(r'notes|tasks|capture|organis|organiz|record', s, re.I) and len(s) > 45), text)
    relevant = parser.descriptions[0] if parser.descriptions else relevant
    excerpt = ' '.join(relevant.split()[:24])
    return {'url': url, 'title': title, 'retrieved_at': datetime.now(timezone.utc).isoformat(),
            'publication_date': None, 'observation': excerpt,
            'supported_claim': f'{title} publishes the quoted product description on its own website.',
            'limitation': 'Vendor self-description; not independent customer evidence, demand, growth or willingness to pay. Publication date unknown.',
            'provenance': 'observed', 'content_hash': fingerprint(text), 'roles': []}

def classify(brief):
    text = (brief['description'] + ' ' + brief['benefit']).lower()
    if re.search(r'voice|note|transcri|journal|knowledge|read|bookmark', text):
        return 'notes'
    if re.search(r'task|habit|plan|focus|productiv|calendar|todo|to-do|routine', text):
        return 'tasks'
    return None

def audience_hypotheses(brief):
    category = classify(brief)
    if category == 'notes':
        return [
            {'name': 'Capture without stopping', 'need': 'People who need to capture ideas while typing is inconvenient.'},
            {'name': 'Find what I already know', 'need': 'People whose useful notes are scattered and hard to retrieve.'},
            {'name': 'Turn a note into a next step', 'need': 'People who capture commitments but lose them before acting.'}]
    if category == 'tasks':
        return [
            {'name': 'Choose the next useful action', 'need': 'People who struggle to prioritise an overwhelming task list.'},
            {'name': 'Keep a routine going', 'need': 'People who want repeatable habits without planning overhead.'},
            {'name': 'Recover when plans change', 'need': 'People whose schedule changes make rigid plans hard to maintain.'}]
    return [{'name': 'People experiencing the stated problem', 'need': brief['problem']}]

def research(brief, fetcher=fetch_source, offline=False):
    start = time.monotonic()
    category = classify(brief)
    entries = CATALOGUE.get(category, [])
    # Fetch each URL once even when roles overlap. Workers share Futures, not duplicate observations.
    with ThreadPoolExecutor(max_workers=4) as network:
        futures = {url: network.submit(fetcher, (title, url)) for title, url in entries} if not offline else {}
        def worker(role):
            items, failures = [], []
            for title, url in entries:
                if offline:
                    failures.append({'url': url, 'reason': 'Offline mode selected; retrieval not attempted'})
                    continue
                try:
                    item = dict(futures[url].result())
                    item['roles'] = [role]
                    items.append(item)
                except Exception:
                    # Do not log raw responses, URLs with credentials, or provider error bodies.
                    failures.append({'url': url, 'reason': 'Source unavailable or unreadable; no evidence substituted'})
            gap = {'market': 'No dated demand series or market-size evidence retrieved.',
                   'competitor': 'Bounded vendor catalogue only; this is not an exhaustive competitor search.',
                   'customer': 'No independent customer research retrieved. Audience groups are hypotheses.'}[role]
            return {'role': role, 'items': items, 'failures': failures, 'gap': gap}
        with ThreadPoolExecutor(max_workers=3) as workers:
            branches = list(workers.map(worker, ('market', 'competitor', 'customer')))
    items = deduplicate([item for branch in branches for item in branch['items']])
    return {'version': fingerprint({'brief': brief['version'], 'sources': items}),
            'brief_version': brief['version'], 'mode': 'offline' if offline else 'live bounded catalogue',
            'sources': items, 'workers': [{k: v for k, v in b.items() if k != 'items'} for b in branches],
            'audiences': audience_hypotheses(brief), 'audience_provenance': 'rule-based hypotheses; founder review required',
            'elapsed_seconds': round(time.monotonic() - start, 3), 'api_cost_usd': 0,
            'search_available': False, 'cached': False}
