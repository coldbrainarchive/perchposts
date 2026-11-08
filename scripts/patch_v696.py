#!/usr/bin/env python3
"""Patch v695 -> v696:
Fix Huddles in the Vr() home tab component (the user accesses huddles via
tabs on the home page, not via /board/feedback).
Same fix as v695 did for Hr(): split y into y (flock filter) and _y (sort+showActivity)
so huddles shows last_activity sort and Active timestamp.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v695.js'
dst = '_deploy/assets/index-DUcNPOLc-v696.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append('FAIL (' + label + '): not found')
    elif n > 1:
        errors.append('FAIL (' + label + '): ' + str(n) + ' matches')
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

# 1. Split y: y stays as flock-only filter, _y controls sort+showActivity
patch(
    'let y=u===' + q + 'activity' + q + ',',
    'let y=u===' + q + 'activity' + q + ',_y=y||u===' + q + 'feedback' + q + ',',
    'Vr: add _y for huddle sort+showActivity'
)

# 2. Sort: use _y instead of y
patch(
    'n===0?y?new Date(t.last_activity||t.created_at)-new Date(e.last_activity||e.created_at)',
    'n===0?_y?new Date(t.last_activity||t.created_at)-new Date(e.last_activity||e.created_at)',
    'Vr sort: use _y for last_activity'
)

# 3. showActivity prop: use _y
patch(
    'showActivity:y,',
    'showActivity:_y,',
    'Vr showActivity: use _y so Huddles shows Active timestamp'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print('Paren delta: ' + str(p_delta) + ', Brace delta: ' + str(b_delta))
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
