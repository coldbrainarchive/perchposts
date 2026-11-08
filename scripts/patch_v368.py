#!/usr/bin/env python3
"""Patch v367 -> v368: pass isHuddle prop to Pr link preview component so View Huddle works."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v367.js'
dst = '_deploy/assets/index-DUcNPOLc-v368.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add isHuddle to Pr component destructured props ───────────────────────
OLD_PR_SIG = 'function Pr({postId:e,title:t,text:n,image:r})'
NEW_PR_SIG = 'function Pr({postId:e,title:t,text:n,image:r,isHuddle:_ih})'
if OLD_PR_SIG in content:
    content = content.replace(OLD_PR_SIG, NEW_PR_SIG, 1)
    print('OK: isHuddle prop added to Pr signature')
else:
    errors.append('FAIL: Pr function signature not found')

# ── 2. Fix the conditional inside Pr to use _ih instead of e.is_huddle ────────
OLD_COND = '(e.is_huddle||e.community_id===`feedback`)?`View Huddle →`:`View Post →`'
NEW_COND = '_ih?`View Huddle →`:`View Post →`'
if OLD_COND in content:
    content = content.replace(OLD_COND, NEW_COND, 1)
    print('OK: View Post → uses _ih prop')
else:
    errors.append('FAIL: View Post → conditional not found')

# Also fix the View Post button (second instance - in Ir/different component)
OLD_COND2 = '(e.is_huddle||e.community_id===`feedback`)?`View Huddle`:`View Post`'
NEW_COND2 = '(e.is_huddle||e.community_id===`feedback`)?`View Huddle`:`View Post`'
# This one IS in Ir where e IS the post object, so it's already correct — leave it

# ── 3. Pass isHuddle when calling Pr from Ir ──────────────────────────────────
OLD_PR_CALL = '(0,L.jsx)(Pr,{postId:e.id,title:e.title||null,text:f||null,image:p?.type===`image`?p.url:null})'
NEW_PR_CALL = '(0,L.jsx)(Pr,{postId:e.id,title:e.title||null,text:f||null,image:p?.type===`image`?p.url:null,isHuddle:!!(e.is_huddle||e.community_id===`feedback`)})'
if OLD_PR_CALL in content:
    content = content.replace(OLD_PR_CALL, NEW_PR_CALL, 1)
    print('OK: isHuddle passed to Pr from Ir')
else:
    errors.append('FAIL: Pr call from Ir not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
