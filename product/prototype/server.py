#!/usr/bin/env python3
"""Local-only prototype: Python standard library, no credentials or paid calls."""
from __future__ import annotations
import argparse
from copy import deepcopy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import secrets
import re
from datetime import datetime, timezone
import threading
from urllib.parse import urlsplit

from contracts import audiences_record, brief_record, clean_text, fingerprint
from quant_adapter import LABELS, WEIGHTS, assess
from research import research, classify
from assessment import build_report, compare
import travel_service
import showcase_service

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / 'static'
RUNS = ROOT / '.runs'
STATE = {'packs': {}, 'reports': {}, 'comparisons': {}}
LOCK = threading.Lock()
TOKEN = secrets.token_urlsafe(32)

def store(kind, key, value):
    with LOCK:
        STATE[kind][key] = deepcopy(value)
        if len(STATE[kind]) > 100:
            del STATE[kind][next(iter(STATE[kind]))]

def load(kind, key):
    with LOCK:
        result = STATE[kind].get(key)
        if result is None:
            raise ValueError('Run expired or server restarted. Confirm the brief and research again.')
        return deepcopy(result)

def dispatch(path, data):
    if not isinstance(data, dict):
        raise ValueError('Request must be a JSON object')
    if path.startswith('/api/travel/'):
        return travel_service.dispatch(path, data)
    if path == '/api/save':
        report = load('reports', data.get('report_id'))
        saved = deepcopy(report)
        comparison_id = data.get('comparison_id')
        if comparison_id:
            comparison = load('comparisons', comparison_id)
            if comparison['baseline_id'] != report['id']:
                raise ValueError('Comparison belongs to a different baseline')
            saved['comparison'] = comparison
        else:
            saved.pop('comparison', None)
        saved['saved_at'] = datetime.now(timezone.utc).isoformat()
        saved['simulation']['saved_run'] = True
        RUNS.mkdir(exist_ok=True)
        target = RUNS / (report['id'] + '.json')
        temporary = RUNS / (report['id'] + '.' + secrets.token_hex(4) + '.tmp')
        temporary.write_text(json.dumps(saved, indent=2, allow_nan=False))
        temporary.replace(target)
        return {'id': report['id'], 'saved_at': saved['saved_at']}
    if path == '/api/replay':
        run_id = data.get('run_id', '')
        if not isinstance(run_id, str) or not re.fullmatch('[a-f0-9]{16}', run_id):
            raise ValueError('Invalid saved run')
        target = RUNS / (run_id + '.json')
        if not target.exists():
            raise ValueError('Saved run is unavailable')
        report = json.loads(target.read_text())
        report['evidence']['cached'] = True
        report['evidence']['mode'] = 'saved evidence replay; no new retrieval'
        report['simulation']['saved_run'] = True
        comparison = report.get('comparison')
        if comparison:
            revised = comparison['revised']
            revised['evidence']['cached'] = True
            revised['evidence']['mode'] = 'saved comparison replay; no new retrieval'
            revised['simulation']['saved_run'] = True
            revised['saved_at'] = report['saved_at']
            store('reports', revised['id'], revised)
            store('comparisons', revised['id'], comparison)
        store('reports', report['id'], report)
        return report
    if path == '/api/draft':
        description = clean_text(data.get('description', ''), 'description', True)
        return {'description': description, 'problem': '', 'benefit': description,
                'geography': '', 'alternatives': '', 'channel': '',
                'mode': 'manual draft fallback',
                'notice': 'No LLM connected. Your description is preserved; write the problem and refine the benefit before confirming.'}
    if path == '/api/research':
        if data.get('confirmed') is not True:
            raise ValueError('Confirm the brief before research')
        brief = brief_record(data.get('brief'))
        offline = data.get('offline', False)
        if not isinstance(offline, bool):
            raise ValueError('Offline must be true or false')
        if classify(brief) is None:
            raise ValueError('This prototype currently supports note-taking and personal-productivity ideas only. Use Start guided demo to see a complete example. Your brief has been kept for editing.')
        demo = json.loads((ROOT / 'demo.json').read_text())
        if data.get('demo') is True and brief['version'] == brief_record(demo['brief'])['version']:
            pack = research(brief, offline=True)
            pack['sources'] = demo['sources']
            pack['mode'] = 'guided demo: recorded vendor sources; no live retrieval'
            pack['cached'] = True
            pack['demo'] = True
            pack['version'] = fingerprint({'brief': brief['version'], 'sources': pack['sources'], 'demo': True})
            for worker in pack['workers']:
                worker['failures'] = []
        else:
            pack = research(brief, offline=offline)
        pack['brief'] = brief
        store('packs', pack['version'], pack)
        return pack
    if path == '/api/report':
        if data.get('audiences_confirmed') is not True:
            raise ValueError('Confirm audiences before running stress tests')
        pack = load('packs', data.get('pack_id'))
        audiences = audiences_record(data.get('audiences'))
        factors = data.get('factors', {})
        report = build_report(pack['brief'], pack, audiences, factors)
        store('reports', report['id'], report)
        return report
    if path == '/api/compare':
        baseline = load('reports', data.get('baseline_id'))
        proposition = clean_text(data.get('proposition', ''), 'proposition', True)
        factor = clean_text(data.get('factor', ''), 'factor', limit=100)
        reason = clean_text(data.get('reason', ''), 'reason', bool(factor), 1000)
        result = compare(baseline, proposition, factor, data.get('value'), reason)
        store('reports', result['revised']['id'], result['revised'])
        store('comparisons', result['revised']['id'], result)
        return result
    raise ValueError('Unknown endpoint')

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # No founder input, credentials or response bodies in logs.
    def send(self, status, body, content_type='application/json'):
        payload = json.dumps(body, allow_nan=False).encode() if content_type == 'application/json' else body
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(payload)
    def allowed_host(self):
        return self.headers.get('Host') in ('127.0.0.1:' + str(self.server.server_port), 'localhost:' + str(self.server.server_port))
    def do_GET(self):
        if not self.allowed_host():
            return self.send(403, {'error': 'Localhost access only'})
        path = urlsplit(self.path).path
        if path == '/api/showcase':
            from urllib.parse import parse_qs
            query = parse_qs(urlsplit(self.path).query).get('q', ['travel planning itinerary control privacy'])[0][:500]
            return self.send(200, showcase_service.study(query))
        scroll_assets = {'/scrollcraft.js': 'text/javascript; charset=utf-8', '/hindsight-scroll.js': 'text/javascript; charset=utf-8', '/scrollcraft.css': 'text/css; charset=utf-8', '/hindsight-scroll.css': 'text/css; charset=utf-8'}
        if path in scroll_assets:
            return self.send(200, (STATIC / path[1:]).read_bytes(), scroll_assets[path])
        if path == '/study-math.js':
            return self.send(200, (STATIC / 'study-math.js').read_bytes(), 'text/javascript; charset=utf-8')
        if path == '/api/travel':
            return self.send(200, travel_service.index())
        if path == '/api/demo':
            return self.send(200, json.loads((ROOT / 'demo.json').read_text()))
        if path == '/api/saved':
            runs = []
            if RUNS.exists():
                for source in sorted(RUNS.glob('*.json'), key=lambda p: p.stat().st_mtime, reverse=True)[:20]:
                    try:
                        record = json.loads(source.read_text())
                        runs.append({'id': record['id'], 'benefit': record['brief']['benefit'], 'saved_at': record['saved_at']})
                    except (ValueError, KeyError):
                        continue
            return self.send(200, runs)
        if path == '/api/status':
            return self.send(200, {'token': TOKEN, 'mode': 'No paid APIs', 'llm': False, 'search': False,
                'mirofish': False, 'factors': [{'key': k, 'label': LABELS[k], 'weight': v} for k, v in WEIGHTS.items()]})
        routes = {'/green-wireframe-head.png': ('green-wireframe-head.png', 'image/png'), '/': ('showcase.html', 'text/html; charset=utf-8'), '/lab': ('travel.html', 'text/html; charset=utf-8'), '/showcase.js': ('showcase.js', 'text/javascript; charset=utf-8'), '/showcase.css': ('showcase.css', 'text/css; charset=utf-8'), '/legacy': ('index.html', 'text/html; charset=utf-8'), '/travel.js': ('travel.js', 'text/javascript; charset=utf-8'), '/travel.css': ('travel.css', 'text/css; charset=utf-8'), '/app.js': ('app.js', 'text/javascript; charset=utf-8'),
                  '/style.css': ('style.css', 'text/css; charset=utf-8')}
        if path in ('/fonts/SpaceGrotesk.ttf', '/fonts/SpaceMono-Regular.ttf'):
            return self.send(200, (STATIC / path.lstrip('/')).read_bytes(), 'font/ttf')
        if path == '/logo.svg':
            return self.send(200, (ROOT.parents[1] / 'brand/logo.svg').read_bytes(), 'image/svg+xml')
        if path not in routes:
            return self.send(404, {'error': 'Not found'})
        filename, mime = routes[path]
        return self.send(200, (STATIC / filename).read_bytes(), mime)
    def do_POST(self):
        if not self.allowed_host() or self.headers.get('X-Session-Token') != TOKEN:
            return self.send(403, {'error': 'Invalid local session; reload the page'})
        origin = self.headers.get('Origin')
        if origin and origin not in ('http://127.0.0.1:' + str(self.server.server_port), 'http://localhost:' + str(self.server.server_port)):
            return self.send(403, {'error': 'Cross-origin requests are blocked'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 100_000:
                raise ValueError('Request too large or empty')
            data = json.loads(self.rfile.read(length), parse_constant=lambda _: (_ for _ in ()).throw(ValueError('Non-finite JSON number')))
            self.send(200, dispatch(urlsplit(self.path).path, data))
        except (ValueError, TypeError, KeyError) as exc:
            self.send(400, {'error': str(exc)})
        except Exception:
            self.send(500, {'error': 'Assessment could not complete. Your baseline remains available; retry the step.'})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'Launch assessment: http://127.0.0.1:{args.port} (zero paid API calls)', flush=True)
    server.serve_forever()
