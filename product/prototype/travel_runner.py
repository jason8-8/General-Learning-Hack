"""Bounded local interviews through the actual MiroFish-local IPC/OASIS layer.
Graph-derived populations are supplied as frozen inputs; social diffusion and validation are separate.
"""
import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import sys
import time


def write(path, data):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2, allow_nan=False))
    temporary.replace(path)


def parse_answer(raw):
    text = str(raw or '').strip()
    if text.startswith('```'):
        text = text.split('\n', 1)[1].rsplit('```', 1)[0]
    answer = json.loads(text)
    if not isinstance(answer, dict):
        raise ValueError('Response must be an object')
    if answer.get('decision') not in ('consider_paying', 'free_only', 'decline'):
        raise ValueError('Missing valid decision')
    for key in ('reason', 'valuable_feature', 'objection', 'next_test'):
        if not isinstance(answer.get(key), str) or not answer[key].strip():
            raise ValueError('Missing ' + key)
    scenario = answer.get('scenario', {})
    if not isinstance(scenario, dict):
        raise ValueError('Scenario must be an object')
    for key in ('hours_saved_per_trip', 'value_per_hour_gbp', 'trips_per_year'):
        value = scenario.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1000:
            raise ValueError('Invalid scenario ' + key)
    if not isinstance(scenario.get('rationale'), str):
        raise ValueError('Missing scenario rationale')
    return answer


async def run(args):
    started = time.monotonic()
    directory = Path(args.run).resolve()
    request = json.loads((directory / 'input.json').read_text())
    result = {**request, 'status': 'running', 'responses': [], 'failed': [], 'excluded': [],
              'completed': 0, 'elapsed_seconds': 0, 'api_spend_usd': 0,
              'usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'calls': 0},
              'engine': 'MiroFish-local IPCHandler → OASIS INTERVIEW → Ollama',
              'scope': 'Graph-informed independent synthetic interviews; no social rounds' if request.get('knowledge_graph') else 'Independent synthetic interviews; no social rounds or graph extraction',
              'checkpoints': [],
              'model': args.model, 'endpoint': 'http://127.0.0.1:11434/v1',
              'model_config': {'temperature': 0.3, 'max_tokens': 400, 'max_retries': 0},
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    output = directory / 'result.json'
    def progress():
        result['elapsed_seconds'] = round(time.monotonic() - started, 2)
        write(output, result)
    progress()
    # Prevent upstream dotenv loading or telemetry from using any saved credentials.
    os.environ['PYTHON_DOTENV_DISABLED'] = '1'
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    os.chdir(directory)
    sys.path.insert(0, str(Path(args.repo).resolve() / 'backend/scripts'))
    from run_reddit_simulation import IPCHandler
    from camel.models import ModelFactory
    from camel.types import ModelPlatformType
    import oasis
    from oasis import ActionType
    from oasis.social_agent import AgentGraph, SocialAgent
    from oasis.social_platform.config import UserInfo
    from camel.prompts import TextPrompt
    source = Path(args.repo) / 'backend/scripts/run_reddit_simulation.py'
    result['mirofish_source_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    model = ModelFactory.create(model_platform=ModelPlatformType.OPENAI,
        model_type=args.model, api_key='ollama-local-only', url=result['endpoint'],
        model_config_dict={'temperature': 0.3, 'max_tokens': 400,
                           'response_format': {'type':'json_object'}}, timeout=120, max_retries=0)
    original = model.arun
    async def measured(*a, **kw):
        response = await original(*a, **kw)
        result['usage']['calls'] += 1
        usage = getattr(response, 'usage', None)
        if usage:
            for key in ('prompt_tokens', 'completion_tokens'):
                result['usage'][key] += getattr(usage, key, 0) or 0
        return response
    model.arun = measured
    profiles = [{'username': p['id'], 'bio': p['label'], 'persona': p['persona'],
                 'mbti':'unspecified', 'gender':'unspecified', 'age':'unspecified',
                 'country':'unspecified'} for p in request['profiles']]
    write(directory / 'profiles.json', profiles)
    # Use OASIS's supported custom system template to remove its default Twitter role.
    template = TextPrompt("You are one synthetic traveller in a product research interview. "
        "Respond in first person from this workflow: {persona}. "
        "Do not assume the product is useful. Consider your existing alternatives and constraints. "
        "Do not invent capabilities, prices or demographics. A conditional yes, free-only answer, or rejection "
        "are equally valid. Distinguish hypothetical assumptions from facts. Return the requested JSON without tools.")
    graph = AgentGraph()
    result['system_prompts'] = []
    for i, profile in enumerate(request['profiles']):
        info = UserInfo(name=profile['id'], description=profile['label'],
                        profile={'persona': profile['persona']}, recsys_type='reddit')
        agent = SocialAgent(agent_id=i, user_info=info, user_info_template=template,
                            model=model, available_actions=[ActionType.DO_NOTHING])
        graph.add_agent(agent)
        result['system_prompts'].append({'profile_id':profile['id'], 'prompt':agent.system_message.content})
    env = oasis.make(agent_graph=graph, platform=oasis.DefaultPlatformType.REDDIT,
                     database_path=str(directory / 'reddit_simulation.db'), semaphore=4)
    await env.reset()
    handler = IPCHandler(str(directory), env, graph)
    prompt = ('You are responding in a synthetic research interview as the assigned traveller. '
              'Do not act as an adviser or invent market facts. Your profile does not prescribe a purchase choice. '
              'Evaluate the offer as described, not as a better imagined product.\n'
              + json.dumps({'brief': request['brief'], 'offer': request['offer'],
                            'question': request['question'], 'evidence': request['sources']})
              + ('\nA price is stated in the offer. consider_paying means hypothetically choosing the paid offer at that exact price; free_only means keeping existing free tools; decline means neither. Never infer a budget or willingness to pay from missing information. If the paid benefit is unproven, explain that uncertainty. This is not an actual purchase. ' if request.get('price_gbp_per_trip') else '\nNo price has been set. consider_paying means conditional interest, not a purchase or conversion. ')
              +
              'Return only JSON with decision (consider_paying, free_only or decline), reason, valuable_feature, '
              'objection, next_test, and scenario {hours_saved_per_trip, value_per_hour_gbp, trips_per_year, rationale}. '
              'The scenario numbers are your explicit hypothetical assumptions, not measured facts or willingness to pay. '
              'Use zero if no time saving. next_test must describe a concrete real-world experiment, not a source ID. '
              'Check that numerical assumptions are internally consistent with their rationale. Keep each string under 15 words. Include a profile-specific constraint in the reason; do not claim features absent from the offer.')
    result['prompt'] = prompt
    progress()
    try:
        async def interview(i, profile):
            result['active_profile'] = profile['id']
            progress()
            try:
                success = await asyncio.wait_for(handler.handle_interview('interview-' + str(i), i, prompt), 150)
                record = json.loads((directory / 'ipc_responses' / ('interview-' + str(i) + '.json')).read_text())
                if not success or record['status'] != 'completed':
                    raise RuntimeError('Engine interview failed; inspect runner.log')
                raw = record['result'].get('response')
                try:
                    answer = parse_answer(raw)
                except (ValueError, TypeError) as exc:
                    result['excluded'].append({'profile_id': profile['id'], 'raw': raw, 'error': str(exc)})
                    return
                s = answer['scenario']
                calculation = {'annual_hours_saved': round(s['hours_saved_per_trip'] * s['trips_per_year'], 2),
                    'annual_time_value_gbp': round(s['hours_saved_per_trip'] * s['trips_per_year'] * s['value_per_hour_gbp'], 2),
                    'formula': 'hours_saved_per_trip × trips_per_year × value_per_hour_gbp',
                    'provenance': 'Deterministic Python applied to synthetic assumptions. Not revenue or willingness to pay.'}
                result['responses'].append({'profile_id': profile['id'], 'label': profile['label'],
                    'raw':raw, 'answer':answer, 'calculation':calculation, 'timestamp':record['result']['timestamp']})
                result['completed'] = len(result['responses'])
            except Exception as exc:
                result['failed'].append({'profile_id':profile['id'], 'error': str(exc)[:300]})
            finally:
                progress()
        # Bounded concurrency; each agent keeps separate memory and a separate trace row.
        # Milestones pause between batches, preserving every actual response.
        for start in range(0, len(request['profiles']), 4):
            await asyncio.gather(*(interview(i, request['profiles'][i])
                                   for i in range(start, min(start+4,len(request['profiles'])))))
            attempted = len(result['responses']) + len(result['failed']) + len(result['excluded'])
            previous = result['checkpoints'][-1]['attempted'] if result['checkpoints'] else 0
            if any(previous < gate <= attempted for gate in (50,250,1000)):
                unique = len({r['raw'] for r in result['responses']})
                checkpoint = {'attempted':attempted,'completed':result['completed'],
                    'failed':len(result['failed']),'excluded':len(result['excluded']),
                    'unique_raw_responses':unique,'elapsed_seconds':round(time.monotonic()-started,2),
                    'decision_counts':{c:sum(r['answer']['decision']==c for r in result['responses']) for c in ('consider_paying','free_only','decline')}}
                result['checkpoints'].append(checkpoint)
                progress()
                if result['completed'] / attempted < .95:
                    result['halt_reason']='Fewer than 95% valid responses at the scale checkpoint; remaining profiles were not attempted.'
                    break
    finally:
        await env.close()
    result.pop('active_profile', None)
    result['status'] = 'completed' if result['completed'] == result['requested'] else 'partial' if result['completed'] else 'failed'
    result['not_attempted'] = result['requested'] - len(result['responses']) - len(result['failed']) - len(result['excluded'])
    result['counts'] = {choice: sum(r['answer']['decision'] == choice for r in result['responses'])
                        for choice in ('consider_paying','free_only','decline')}
    progress()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--model', default='qwen3-coder:30b')
    args = parser.parse_args()
    asyncio.run(run(args))
