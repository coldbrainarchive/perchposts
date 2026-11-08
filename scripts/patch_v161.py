#!/usr/bin/env python3
"""Patch v160 -> v161: rename Member/Members designation to Flock."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v160.js'
dst = '_deploy/assets/index-DUcNPOLc-v161.js'

content = open(src, encoding='utf-8').read()
errors = []
changes = 0

replacements = [
    # Role label in user panel
    ('`Administrator`:D?`Moderator`:O?`Member`:r?`Anonymous`:`Guest`',
     '`Administrator`:D?`Moderator`:O?`Flock`:r?`Anonymous`:`Guest`'),
    # Mod panel Members heading
    ('children:[`Members `,(0,L.jsx)(`span`',
     'children:[`Flock `,(0,L.jsx)(`span`'),
    # Search placeholder
    ('placeholder:`Search members…`',
     'placeholder:`Search flock…`'),
    # Empty state
    ('children:`No registered members yet`',
     'children:`No flock members yet`'),
    # Delete confirm dialog
    ('`Delete ${i||`this member`}? This cannot be undone.`',
     '`Delete ${i||`this flock member`}? This cannot be undone.`'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f'OK: {repr(old[:40])} → {repr(new[:40])}')
        changes += 1
    else:
        errors.append(f'FAIL: not found: {repr(old[:60])}')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst} ({changes} replacements)')
