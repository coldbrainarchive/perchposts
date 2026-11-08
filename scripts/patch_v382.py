#!/usr/bin/env python3
"""Patch v381 -> v382:
- Leave button for OP shows "leaving will delete this huddle" confirmation
- Leave button for members keeps existing "Leave this huddle?" confirmation
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v381.js'
dst = '_deploy/assets/index-DUcNPOLc-v382.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── Postcard (Ir): OP-aware confirm ───────────────────────────────────────────
IR_OLD = (
    'if(!confirm(`Leave this huddle?`))return;'
    'const _bid=Gn(),_un=localStorage.getItem(`_myUsername`)||null;'
)
IR_NEW = (
    'const _bid=Gn(),_un=localStorage.getItem(`_myUsername`)||null;'
    'const _isOp=_un&&e.username&&_un===e.username;'
    'if(!confirm(_isOp?`You created this huddle. Leaving will delete it for everyone — are you sure?`:`Leave this huddle?`))return;'
)
if IR_OLD in content:
    content = content.replace(IR_OLD, IR_NEW, 1)
    print('OK: postcard leave has OP-aware confirm')
else:
    errors.append('FAIL: postcard leave confirm not found')

# ── Post page (Wr): OP-aware confirm ──────────────────────────────────────────
WR_OLD = (
    'if(!confirm(`Leave this huddle?`))return;'
    'const _un3=localStorage.getItem(`_myUsername`)||null;'
)
WR_NEW = (
    'const _un3=localStorage.getItem(`_myUsername`)||null;'
    'const _isOp3=_un3&&c.username&&_un3===c.username;'
    'if(!confirm(_isOp3?`You created this huddle. Leaving will delete it for everyone — are you sure?`:`Leave this huddle?`))return;'
)
if WR_OLD in content:
    content = content.replace(WR_OLD, WR_NEW, 1)
    print('OK: post page leave has OP-aware confirm')
else:
    errors.append('FAIL: post page leave confirm not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
