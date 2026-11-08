#!/usr/bin/env python3
"""Patch v694 -> v695:
Properly fix Huddles board: sort by activity + show Active timestamp WITHOUT
using the Flock cross-board filter.
- b: only true for Flock (slug='activity') — controls which posts to show (all boards vs one board)
- _sa: true for Flock OR Huddles — controls sort order and showActivity timestamp
This way Huddles shows only huddle posts (lr filter) but sorted by last_activity.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v694.js'
dst = '_deploy/assets/index-DUcNPOLc-v695.js'

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

# 1. Revert b to flock-only filter; add _sa for sort+showActivity
patch(
    'let b=e===' + q + 'activity' + q + '||e===' + q + 'feedback' + q,
    'let b=e===' + q + 'activity' + q + ',_sa=b||e===' + q + 'feedback' + q,
    'split b (filter) from _sa (sort+showActivity)'
)

# 2. Sort: use _sa instead of b
patch(
    'e.pinned===t.pinned?b?new Date(t.last_activity||t.created_at)-new Date(e.last_activity||e.created_at)',
    'e.pinned===t.pinned?_sa?new Date(t.last_activity||t.created_at)-new Date(e.last_activity||e.created_at)',
    'sort: use _sa for last_activity ordering'
)

# 3. showActivity prop: use _sa instead of b
patch(
    'showActivity:b,',
    'showActivity:_sa,',
    'showActivity: use _sa so Huddles shows Active timestamp'
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
