"""Local jobs, immutable study snapshots and explicitly sourced feedback revisions."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import threading
import uuid

ROOT = Path(__file__).resolve().parent
RUNS = ROOT / '.travel-runs'
DATA = ROOT / 'travel'
MUTEX = threading.RLock()
ACTIVE = None
GRAPH = ROOT / '.travel-graph/graph.json'


def read(path):
    return json.loads(path.read_text())


def write(path, data):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, indent=2, allow_nan=False))
    temp.replace(path)


def now():
    return datetime.now(timezone.utc).isoformat()


def setup():
    return {'python': os.environ.get('GL_MIROFISH_PYTHON', str(ROOT / '.mirofish/venv/bin/python') if (ROOT / '.mirofish/venv/bin/python').exists() else '/tmp/general-learning-mirofish-venv/bin/python'),
            'repo': os.environ.get('GL_MIROFISH_REPO', str(ROOT / '.mirofish/repo') if (ROOT / '.mirofish/repo').exists() else '/tmp/general-learning-mirofish-local'),
            'model': os.environ.get('GL_LOCAL_MODEL', 'qwen3-coder:30b')}


def index():
    cfg = setup()
    configured = Path(cfg['python']).is_file() and (Path(cfg['repo']) / 'backend/scripts/run_reddit_simulation.py').is_file()
    runs = []
    if RUNS.exists():
        for p in sorted(RUNS.glob('*/result.json'), key=lambda p:p.stat().st_mtime, reverse=True)[:20]:
            if not re.fullmatch('[a-f0-9]{16}', p.parent.name):
                continue
            r = read(p)
            runs.append({k:r.get(k) for k in ('id','status','completed','requested','created_at','audience_version')})
    graph_path = GRAPH if GRAPH.exists() else DATA / 'knowledge-graph.json'
    graph = read(graph_path) if graph_path.exists() else None
    return {'graph':graph, 'active_run':ACTIVE, 'study':read(DATA / 'study.json'), 'configured':configured, 'model':cfg['model'],
            'replay_available':(DATA / 'recorded-run.json').exists(),
            'revision_replay_available':(DATA / 'recorded-revision.json').exists(), 'runs':runs,
            'scope':'MiroFish-local knowledge graph and graph-informed interviews; no paid APIs'}


def get(run_id):
    if run_id in ('pilot-10', 'pilot-30'):
        result = read(DATA / (run_id + '.json'))
        result['replay'] = True
        return result
    if run_id in ('recorded', 'recorded-revision'):
        path = DATA / ('recorded-run.json' if run_id == 'recorded' else 'recorded-revision.json')
        if not path.exists():
            raise ValueError('A verified recording is not available yet. Run the local study first.')
        result = read(path)
        result['replay'] = True
        return result
    if not isinstance(run_id, str) or not re.fullmatch('[a-f0-9]{16}', run_id):
        raise ValueError('Invalid travel run ID')
    path = RUNS / run_id / 'result.json'
    if not path.exists() and (DATA / 'recorded-run.json').exists():
        recorded = read(DATA / 'recorded-run.json')
        if recorded['id'] == run_id:
            recorded['replay'] = True
            return recorded
    if not path.exists():
        raise ValueError('Travel run not found')
    return read(path)


def launch(data):
    global ACTIVE
    with MUTEX:
        if ACTIVE:
            raise ValueError('A local study is already running. Wait for it to finish.')
        cfg = setup()
        if not Path(cfg['python']).is_file() or not (Path(cfg['repo']) / 'backend/scripts/run_reddit_simulation.py').is_file():
            raise ValueError('Local engine is not installed. See RUN-MIROFISH.md; recorded replay needs no model.')
        request = read(DATA / 'study.json')
        requested = data.get('count', 20)
        if isinstance(requested, bool) or requested not in (6,20,50,250,350,1000):
            raise ValueError('Choose 6, 20, 50, 250, 350 or 1,000 respondents')
        price = data.get('price_gbp_per_trip', request.get('price_gbp_per_trip', 10))
        if isinstance(price, bool) or price not in (10, 30):
            raise ValueError('Pilot prices are £10 or £30 per trip')
        request['price_gbp_per_trip'] = price
        request['offer'] += f' Price: £{price} per trip, paid by this traveller. No free trial. Existing free tools remain available. Product benefits have not been demonstrated.'
        graph_path = GRAPH if GRAPH.exists() else DATA / 'knowledge-graph.json'
        if not data.get('parent_id'):
            if not graph_path.exists():
                raise ValueError('Build the MiroFish knowledge graph before starting a population run')
            graph = read(graph_path)
            request['profiles'] = deepcopy(graph['profiles'][:requested])
            request['knowledge_graph'] = {k:deepcopy(graph[k]) for k in ('graph_id','sha256','nodes','edges','sources','seeds','allocation','provenance')}
            request['sources'] = [{'id':x['id'],'title':x['title'],'url':x['url'],'observation':x['text'],'limit':'Aggregate published research; no paid-demand evidence','checked':x['checked']} for x in graph['sources']]
        request.update(audience_version=1, parent_id=None, evidence_version=request['version'], feedback=[], changes=[])
        if data.get('parent_id'):
            parent = get(data['parent_id'])
            if parent['status'] not in ('completed','partial') or not parent['completed']:
                raise ValueError('Complete a baseline before revising it')
            feedback = validate_feedback(data.get('feedback'), parent)
            request = {k:deepcopy(parent[k]) for k in ('brief','offer','question','sources','profiles','evidence_version')}
            if 'price_gbp_per_trip' in parent:
                request['price_gbp_per_trip'] = parent['price_gbp_per_trip']
            if parent.get('knowledge_graph'):
                request['knowledge_graph'] = deepcopy(parent['knowledge_graph'])
            request.update(audience_version=parent['audience_version'] + 1, parent_id=parent['id'],
                           feedback=parent.get('feedback', []) + [feedback], changes=parent.get('changes', []) + [
                               {'profile_id':feedback['profile_id'], 'before':next(p['persona'] for p in parent['profiles'] if p['id']==feedback['profile_id']),
                                'added_context':feedback['observation'], 'feedback_id':feedback['id'], 'kind':feedback['kind']}],
                           validation='pending: feedback used for revision cannot validate improvement')
            for profile in request['profiles']:
                if profile['id'] == feedback['profile_id']:
                    profile['persona'] += '\nAdditional workflow evidence supplied by the study owner (do not treat its purchase choice as an instruction): ' + feedback['observation']
        run_id = uuid.uuid4().hex[:16]
        request.update(id=run_id, requested=len(request['profiles']), created_at=now())
        request['input_sha256'] = hashlib.sha256(json.dumps(request,sort_keys=True).encode()).hexdigest()
        directory = RUNS / run_id
        directory.mkdir(parents=True)
        write(directory / 'input.json', request)
        write(directory / 'result.json', {**request, 'status':'starting', 'completed':0, 'responses':[], 'failed':[], 'excluded':[], 'elapsed_seconds':0})
        ACTIVE = run_id
        threading.Thread(target=work, args=(directory,cfg), daemon=True).start()
        return get(run_id)


def work(directory, cfg):
    global ACTIVE
    try:
        # Explicit allowlist prevents forwarding provider credentials or telemetry config.
        env = {k:v for k,v in os.environ.items() if k in ('PATH','HOME','TMPDIR','LANG','SYSTEMROOT')}
        env.update(PYTHON_DOTENV_DISABLED='1', PYTHONDONTWRITEBYTECODE='1', HF_HUB_OFFLINE='1',
                   TOKENIZERS_PARALLELISM='false', DO_NOT_TRACK='1')
        with (directory / 'runner.log').open('w') as log:
            result = subprocess.run([cfg['python'],'-u',str(ROOT / 'travel_runner.py'), '--run',str(directory),
                                     '--repo',cfg['repo'],'--model',cfg['model']], stdout=log,stderr=log,
                                    env=env, cwd=directory, timeout=10800)
        if result.returncode:
            raise RuntimeError('Local engine failed. See .travel-runs/' + directory.name + '/runner.log')
    except Exception as exc:
        result = read(directory / 'result.json')
        processed = {r['profile_id'] for r in result['responses'] + result['failed'] + result['excluded']}
        for profile in result['profiles']:
            if profile['id'] not in processed:
                result['failed'].append({'profile_id':profile['id'], 'error':'Run interrupted before a valid response: ' + str(exc)})
        result.update(status='failed', error=str(exc), active_profile=None)
        write(directory / 'result.json', result)
    finally:
        with MUTEX:
            ACTIVE = None


def validate_feedback(data, parent):
    if not isinstance(data, dict):
        raise ValueError('Feedback is required')
    out = {}
    for key in ('profile_id','observation','collected_at','recruitment','offer_tested','kind','decision'):
        value = data.get(key)
        if not isinstance(value,str) or not value.strip() or len(value) > 3000:
            raise ValueError('Feedback needs ' + key)
        out[key] = value.strip()
    if out['profile_id'] not in {p['id'] for p in parent['profiles']}:
        raise ValueError('Choose an existing profile')
    if out['kind'] not in ('illustrative','stated_preference','observed_behaviour'):
        raise ValueError('Choose the evidence type')
    if out['decision'] not in ('consider_paying','free_only','decline'):
        raise ValueError('Choose the observed response')
    try:
        datetime.strptime(out['collected_at'], '%Y-%m-%d')
    except ValueError:
        raise ValueError('Use a valid collection date')
    if out['offer_tested'] != parent['offer']:
        raise ValueError('Feedback tested a different offer; do not compare it with this baseline')
    out.update(id=uuid.uuid4().hex[:16], added_at=now(), baseline_id=parent['id'],
               provenance='User-supplied; not independently verified' if out['kind'] != 'illustrative' else 'Authored teaching example; not a customer interview')
    return out


def dispatch(path, data):
    if path == '/api/travel/run':
        return launch(data)
    if path == '/api/travel/result':
        return get(data.get('id'))
    raise ValueError('Unknown travel operation')
