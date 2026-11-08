#!/usr/bin/env python3
"""Patch v223 -> v224: fix await inside non-async state setter callback."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v223.js'
dst = '_deploy/assets/index-DUcNPOLc-v224.js'

content = open(src, encoding='utf-8').read()
errors = []

# await Dr() inside a(_pr=>({...})) is invalid — _pr=>({}) is not async.
# Fix: await Dr() first, then merge into state.
OLD = 'a(_pr=>({..._pr,...await Dr(_f.map(_e=>_e.id))}));'
NEW = 'const _sc=await Dr(_f.map(_e=>_e.id));a(_pr=>({..._pr,..._sc}));'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: await Dr() hoisted out of state setter')
else:
    errors.append('FAIL: await Dr pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
