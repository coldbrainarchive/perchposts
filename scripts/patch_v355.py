#!/usr/bin/env python3
"""Patch v354 -> v355: skip title/body validation for huddle posts."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v354.js'
dst = '_deploy/assets/index-DUcNPOLc-v355.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '{try{if(!a.trim())return alert(`Give your post a title`);'
    'if(!s.trim()&&!T)return alert(`Add a body, or attach a link, photo, or video`);'
    'if(l)return;'
)
NEW = (
    '{try{if(!_isHuddle&&!a.trim())return alert(`Give your post a title`);'
    'if(!_isHuddle&&!s.trim()&&!T)return alert(`Add a body, or attach a link, photo, or video`);'
    'if(_isHuddle&&_hmTagged.length===0)return alert(`Add at least one user to your huddle`);'
    'if(l)return;'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: title/body validation skipped for huddles')
else:
    errors.append('FAIL: submit validation not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
