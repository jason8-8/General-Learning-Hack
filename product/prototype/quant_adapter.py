"""Use legacy S only; its unvalidated adoption probability is never exposed."""
from __future__ import annotations
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'quant'))
from score_engine import WEIGHTS, score

LABELS = {
    'icp_fit': 'Audience fit', 'problem_intensity': 'Problem strength',
    'price_fit': 'Price fit', 'readiness': 'Readiness to change',
    'analog_success': 'Comparable outcomes', 'distribution_fit': 'Acquisition feasibility',
    'switching_ease': 'Ease of switching', 'competition_ease': 'Competitive room',
}
PROVENANCE = {'observed', 'inferred', 'user-supplied', 'assumed'}
RUBRIC = ('All eight factors are required; weights are never renormalised. '
          'With at least four observed/inferred factors linked to sources: S >= 0.70 promising, '
          'S >= 0.40 mixed, otherwise weak. Otherwise: insufficient evidence. '
          'These thresholds and legacy weights are design assumptions, not validated predictions. '
          'Assumption scenarios can show an index but do not upgrade evidence coverage.')

def assess(records=None, evidence_ids=()):
    records = records or {}
    if not isinstance(records, dict) or set(records) - set(WEIGHTS):
        raise ValueError('Unknown quant factors')
    rows, values = [], {}
    backed = 0
    for key, weight in WEIGHTS.items():
        record = records.get(key, {})
        if not isinstance(record, dict):
            raise ValueError('Each factor must be a record')
        value = record.get('value')
        provenance = record.get('provenance', 'assumed')
        refs = record.get('evidence_ids', [])
        reason = record.get('reason', '')
        if provenance not in PROVENANCE or not isinstance(refs, list) or any(r not in evidence_ids for r in refs):
            raise ValueError(f'Invalid provenance or source reference for {key}')
        if not isinstance(reason, str) or len(reason) > 1000:
            raise ValueError('Factor reason must be text under 1000 characters')
        if value is not None:
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f'{key} must be a finite number from 0 to 1, or null')
            if not reason.strip():
                raise ValueError(f'Explain the input for {LABELS[key]}')
            if provenance in ('observed', 'inferred') and not refs:
                raise ValueError(f'{key} needs a source citation')
            backed += int(provenance in ('observed', 'inferred') and bool(refs))
            values[key] = value
        rows.append({'key': key, 'label': LABELS[key], 'weight': weight, 'value': value,
                     'provenance': provenance if value is not None else 'missing',
                     'evidence_ids': refs, 'reason': reason})
    index = round(score(values)['S'], 4) if len(values) == len(WEIGHTS) else None
    outlook = 'insufficient evidence'
    if index is not None and backed >= 4:
        outlook = 'promising' if index >= .7 else 'mixed' if index >= .4 else 'weak'
    return {'outlook': outlook, 'index': index, 'factors': rows, 'supplied': len(values),
            'total': len(WEIGHTS), 'evidence_backed': backed, 'rubric': RUBRIC,
            'validated': False, 'price_comparison_enabled': False}
