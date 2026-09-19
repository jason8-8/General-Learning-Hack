"""Provider-independent records. All external/LLM inputs pass validation here."""
from __future__ import annotations
import hashlib
import json
from urllib.parse import urlsplit, urlunsplit

VERSION = 'launch-assessment-v1'

def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]

def clean_text(value, name, required=False, limit=5000):
    if not isinstance(value, str) or len(value) > limit:
        raise ValueError(f'{name} must be text of at most {limit} characters')
    value = value.strip()
    if required and not value:
        raise ValueError(f'{name} is required')
    return value

def brief_record(data):
    if not isinstance(data, dict):
        raise ValueError('Brief must be an object')
    result = {key: clean_text(data.get(key, ''), key, key in ('description', 'problem', 'benefit'))
              for key in ('description', 'problem', 'benefit', 'geography', 'alternatives', 'channel')}
    result['language'] = 'English'
    result['version'] = fingerprint(result)
    return result

def audiences_record(data):
    if not isinstance(data, list) or not 1 <= len(data) <= 3:
        raise ValueError('Confirm between one and three audiences')
    result = []
    for row in data:
        if not isinstance(row, dict):
            raise ValueError('Each audience must be an object')
        result.append({key: clean_text(row.get(key, ''), key, True, 800)
                       for key in ('name', 'need')})
    return result

def canonical_url(url):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Sources require a public HTTPS URL')
    return urlunsplit(('https', parsed.netloc.lower(), parsed.path.rstrip('/') or '/', '', ''))

def deduplicate(items):
    """Three workers citing one page count as one source, not three observations."""
    unique = {}
    for item in items:
        key = canonical_url(item['url'])
        if key in unique:
            unique[key]['roles'] = sorted(set(unique[key]['roles'] + item['roles']))
        else:
            unique[key] = dict(item, url=key, id='src-' + fingerprint(key)[:8])
    return sorted(unique.values(), key=lambda item: item['id'])
