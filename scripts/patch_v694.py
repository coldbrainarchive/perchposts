#!/usr/bin/env python3
"""Patch v693 -> v694:
Make Huddles board sort by activity first, same as Flock.
Flock slug = 'activity', Huddles slug = 'feedback'.
The sort variable b was only true for 'activity' (Flock).
Add 'feedback' (Huddles) so it also sorts by last_activity desc.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v693.js'
dst = '_deploy/assets/index-DUcNPOLc-v694.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

old = 'let b=e===' + q + 'activity' + q
new = 'let b=e===' + q + 'activity' + q + '||e===' + q + 'feedback' + q

n = content.count(old)
if n == 0:
    errors.append('FAIL: sort condition not found')
elif n > 1:
    errors.append('FAIL: ' + str(n) + ' matches')
else:
    content = content.replace(old, new)
    print('OK: Huddles board now sorts by activity first')

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
