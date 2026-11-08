#!/usr/bin/env python3
"""Patch v389 -> v390:
- All user search result pills: apply CSS color filter from Jn() so bird looks
  identical to how it appears on posts/comments (hue-rotate + saturation)
- Admin users in search results: show admin-bird.png (hat) instead of generic bird
  by passing is_admin from the role field returned by /search-users
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v389.js'
dst = '_deploy/assets/index-DUcNPOLc-v390.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    '(0,L.jsx)(`span`,{children:(Jn({username:_u.username,browser_id:_u.browser_id||null})||{}).e||`\U0001f426`})'
)
NEW = (
    '(()=>{const _jd=Jn({username:_u.username,browser_id:_u.browser_id||null,is_admin:_u.role===`admin`})||{};'
    'return typeof _jd===`object`&&_jd.hat?'
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{height:13,width:13,objectFit:`contain`}}):'
    '(0,L.jsx)(`span`,{style:_jd.f?{filter:_jd.f}:{},children:_jd.e||`\U0001f426`});})() '
)

count = content.count(OLD)
if count == 4:
    content = content.replace(OLD, NEW)
    print(f'OK: fixed {count} inline pill emoji renders (filter + admin bird)')
else:
    errors.append(f'FAIL: expected 4 occurrences, found {count}')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
