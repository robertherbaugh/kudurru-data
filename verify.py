#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Robert Herbaugh and the Kudurru contributors.
"""Verify a reviewed catalog snapshot without importing application code."""
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parent
listed = set()
for line in (root / 'SHA256SUMS').read_text().splitlines():
    digest, name = line.split('  ', 1)
    path = Path(name)
    if path.is_absolute() or '..' in path.parts or name in listed:
        raise ValueError('invalid or duplicate manifest path')
    if not re.fullmatch('[0-9a-f]{64}', digest):
        raise ValueError('invalid manifest digest')
    if (root / path).is_symlink():
        raise ValueError('symlink in catalog snapshot')
    if hashlib.sha256((root / path).read_bytes()).hexdigest() != digest:
        raise ValueError('manifest mismatch: ' + name)
    listed.add(name)
raw = (root / 'catalogue.json').read_bytes()
if len(raw) > 4 * 1024 * 1024:
    raise ValueError('catalog exceeds the consumer limit')

def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON field')
        result[key] = value
    return result

data = json.loads(raw, object_pairs_hook=unique)
if data['schemaVersion'] != 2 or data['license'] != 'Apache-2.0':
    raise ValueError('unreviewed schema or license')
if not re.fullmatch(r'\d{4}\.\d{2}\.\d{2}', data['version']):
    raise ValueError('invalid catalog version')
provenance = (root / 'PROVENANCE.md').read_text()
if hashlib.sha256(raw).hexdigest() not in provenance or data['version'] not in provenance:
    raise ValueError('catalog provenance is stale')
ids = {}
for collection in ['categories', 'services', 'safeSearch']:
    values = data[collection]
    keys = [entry['id'] for entry in values]
    if len(set(keys)) != len(keys) or any(not re.fullmatch(r'[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?', key) for key in keys):
        raise ValueError('invalid or duplicate catalog IDs')
    ids[collection] = set(keys)
    for entry in values:
        if not entry['name'] or entry['id'] not in provenance:
            raise ValueError('missing name or provenance')
for entry in data['services']:
    if entry['category'] not in ids['categories'] or not entry['rules'] or not entry['source']:
        raise ValueError('invalid service references or provenance')
    for field in ['requires', 'related']:
        if any(key not in ids['services'] or key == entry['id'] for key in entry.get(field, [])):
            raise ValueError('invalid service hint')
    if entry.get('icon') and 'icons/' + entry['icon'] + '.svg' not in listed:
        raise ValueError('missing declared service icon')
for entry in data['safeSearch']:
    if not entry['source'] or not entry['domains']:
        raise ValueError('missing engine provenance or domains')
print(json.dumps({'files_verified': len(listed), 'version': data['version'],
                  'categories': len(ids['categories']), 'services': len(ids['services']),
                  'safe_search_engines': len(ids['safeSearch'])}, sort_keys=True))
