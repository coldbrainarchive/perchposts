#!/usr/bin/env python3
"""Patch v366 -> v367: add community_id fallback for huddle detection in post card."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v366.js'
dst = '_deploy/assets/index-DUcNPOLc-v367.js'

content = open(src, encoding='utf-8').read()
errors = []

# Replace both View Post instances with a robust check
OLD1 = 'children:e.is_huddle?`View Huddle →`:`View Post →`'
NEW1 = 'children:(e.is_huddle||e.community_id===`feedback`)?`View Huddle →`:`View Post →`'
count1 = content.count(OLD1)
if count1:
    content = content.replace(OLD1, NEW1)
    print(f'OK: View Post → updated ({count1} occurrences)')
else:
    errors.append('FAIL: View Post → not found')

OLD2 = 'children:e.is_huddle?`View Huddle`:`View Post`'
NEW2 = 'children:(e.is_huddle||e.community_id===`feedback`)?`View Huddle`:`View Post`'
count2 = content.count(OLD2)
if count2:
    content = content.replace(OLD2, NEW2)
    print(f'OK: View Post button updated ({count2} occurrences)')
else:
    errors.append('FAIL: View Post button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
