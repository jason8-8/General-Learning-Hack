"""Independent rule-based stress tests; never pretend these are customer interviews."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import time
from contracts import fingerprint
from quant_adapter import assess

LENSES = [
    ('Time saved', 'Does the benefit save more time than capture, correction and setup consume?', 'Measure end-to-end time against the current workaround.', 'problem_intensity'),
    ('Trust', 'What happens when an output is wrong, missing or sensitive?', 'Ask participants to find and correct a deliberately flawed output.', 'readiness'),
    ('Switching', 'Why would someone move an established workflow into another app?', 'Observe a first-use session with their existing material.', 'switching_ease'),
    ('Repeat use', 'Does this solve a recurring job or a one-off inconvenience?', 'Run a seven-day diary study and record voluntary returns.', 'icp_fit'),
    ('Discovery', 'Can the founder reach people at the moment they feel this problem?', 'Test one narrowly targeted invitation with a measurable response.', 'distribution_fit'),
    ('Alternatives', 'Is the core benefit distinct from tools people already have?', 'Compare task completion with the strongest existing alternative.', 'competition_ease'),
]

def stress_tests(brief, audiences, factors, evidence_ids):
    start = time.monotonic()
    def run(pair):
        index, lens = pair
        name, objection, test, key = lens
        audience = audiences[index % len(audiences)]
        quant = assess(factors, evidence_ids)
        return {'id': 'reaction-' + str(index + 1), 'lens': name, 'audience': audience['name'],
                'need': audience['need'], 'proposition': brief['benefit'], 'objection': objection,
                'next_test': test, 'scenario': {'factor': key, 'proposed_value': None,
                  'reason': 'Founder must supply a justified value; no numerical change invented.'},
                'quant_tool': {'index': quant['index'], 'outlook': quant['outlook']},
                'provenance': 'authored rule-based stress test; not an LLM agent or observed customer'}
    with ThreadPoolExecutor(max_workers=6) as executor:
        reactions = list(executor.map(run, enumerate(LENSES)))
    return {'mode': 'rule-based fallback', 'mirofish': False, 'agent_count': 0,
            'reaction_count': len(reactions), 'rounds': 1, 'independent': True,
            'reactions': reactions, 'elapsed_seconds': round(time.monotonic() - start, 3),
            'api_cost_usd': 0, 'saved_run': False,
            'limitation': 'Six authored stress-test passes, not six simulated customers. No votes, demand estimates or social interaction.'}

def build_report(brief, pack, audiences, factors):
    ids = [source['id'] for source in pack['sources']]
    quant = assess(factors, ids)
    simulation = stress_tests(brief, audiences, factors, ids)
    sections = [
        {'title': 'Commercial outlook', 'text': 'Insufficient evidence for a launch recommendation. Validate the problem and repeat use before forecasting revenue.', 'evidence_ids': []},
        {'title': 'Competitors and alternatives', 'text': 'Inspect the retrieved vendor pages for overlap with your proposition. Catalogue coverage is limited and does not establish saturation.', 'evidence_ids': ids},
        {'title': 'Consumer preferences', 'text': 'No independent preference study is available. Test accuracy, privacy, workflow fit and time saved with real users.', 'evidence_ids': []},
        {'title': 'Market trend', 'text': 'Unknown. A current product page cannot establish a six-month demand trend.', 'evidence_ids': []},
        {'title': 'Competitor stagnation', 'text': 'Unknown. Dated release history and comparable time windows are required.', 'evidence_ids': []},
        {'title': 'Missing angles', 'text': 'Test willingness to pay, repeat use, accessibility, acquisition cost and whether the existing workaround is good enough.', 'evidence_ids': []},
        {'title': 'Barriers and execution risk', 'text': 'Hypotheses to investigate: switching effort, trust in outputs, privacy expectations and integration with existing habits.', 'evidence_ids': []},
        {'title': 'Retention and commercial viability', 'text': 'Unknown. Measure voluntary return use and actual purchase decisions; synthetic reactions do not fill these gaps.', 'evidence_ids': []},
    ]
    sections[0]['text'] = ('Model rubric: ' + quant['outlook'] + '. This is an unvalidated heuristic assessment. '
                           'No success probability or revenue forecast is available.')
    report = {'brief': deepcopy(brief), 'evidence': deepcopy(pack), 'audiences': deepcopy(audiences),
              'factor_inputs': deepcopy(factors), 'quant': quant, 'simulation': simulation, 'sections': sections,
              'assumptions': ['English-only research.', 'Launch geography: ' + (brief['geography'] or 'unknown; no geographic demand claim.'),
                              'Audiences are founder-confirmed hypotheses, not validated segments.',
                              'Legacy weights and rubric thresholds are unvalidated.',
                              'Vendor descriptions do not establish demand or customer preferences.'],
              'next_tests': [{'title': 'Problem interview', 'action': 'Recruit five people with the first confirmed need. Ask about their most recent experience and current workaround.'},
                             {'title': 'Feature proposition test', 'action': 'Show the baseline and one changed benefit in random order. Record the reasons for a choice; do not treat a small sample as market demand.'},
                             {'title': 'Repeat-use trial', 'action': 'Observe a seven-day trial, track voluntary returns and ask what participants used instead.'}]}
    report['id'] = fingerprint({'brief': brief, 'pack': pack['version'], 'audiences': audiences, 'factors': factors})
    return report

def compare(baseline, proposition, factor, value, reason):
    if factor == 'price_fit':
        raise ValueError('Price comparisons are disabled pending numerical fixes and tests')
    if factor and factor not in {row['key'] for row in baseline['quant']['factors']}:
        raise ValueError('Unknown factor')
    factors = deepcopy(baseline['factor_inputs'])
    if factor:
        factors[factor] = {'value': value, 'provenance': 'assumed', 'evidence_ids': [], 'reason': reason}
    brief = deepcopy(baseline['brief'])
    brief['benefit'] = proposition
    brief['version'] = fingerprint({k: v for k, v in brief.items() if k != 'version'})
    # Evidence is carried forward visibly, not treated as fresh research supporting the changed proposition.
    pack = deepcopy(baseline['evidence'])
    pack['cached'] = True
    pack['mode'] = 'baseline evidence reused for hypothetical comparison'
    revised = build_report(brief, pack, baseline['audiences'], factors)
    old, new = baseline['quant']['index'], revised['quant']['index']
    return {'baseline_id': baseline['id'], 'revised': revised,
            'changed_factor': factor or None, 'delta': round(new - old, 4) if old is not None and new is not None else None,
            'limitation': 'Feature scenario only. Evidence has not been refreshed; the altered proposition is an assumption. No odds uplift is implied.'}
