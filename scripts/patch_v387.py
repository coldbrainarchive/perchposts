#!/usr/bin/env python3
"""Patch v386 -> v387:
- Profile page: rename Message → Huddle button, navigate to /new?huddle=1&invite=username
- New post page (Ur): init _isHuddle and _hmTagged from URL params so the user
  and huddle mode are pre-filled when arriving from a profile Huddle button tap
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v386.js'
dst = '_deploy/assets/index-DUcNPOLc-v387.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Rename button label ─────────────────────────────────────────────────────
OLD1 = 'children:`Message`'
NEW1 = 'children:`Huddle`'
if OLD1 in content:
    content = content.replace(OLD1, NEW1, 1)
    print('OK: button renamed to Huddle')
else:
    errors.append('FAIL: Message button label not found')

# ── 2. Change onMessage handler to navigate to new post page ──────────────────
OLD2 = 'onMessage:(_u)=>window.dispatchEvent(new CustomEvent(`open-dm`,{detail:_u}))'
NEW2 = 'onMessage:(_u)=>{window.location.href=`/new?huddle=1&invite=${encodeURIComponent(_u)}`;}'
if OLD2 in content:
    content = content.replace(OLD2, NEW2, 1)
    print('OK: onMessage navigates to /new with huddle+invite params')
else:
    errors.append('FAIL: onMessage handler not found')

# ── 3. Init _isHuddle from URL param ──────────────────────────────────────────
OLD3 = '[_isHuddle,_setIsHuddle]=(0,_.useState)(!1),[_hmTagQ,_setHmTagQ]=(0,_.useState)(``)'
NEW3 = '[_isHuddle,_setIsHuddle]=(0,_.useState)(i.get(`huddle`)===`1`),[_hmTagQ,_setHmTagQ]=(0,_.useState)(``)'
if OLD3 in content:
    content = content.replace(OLD3, NEW3, 1)
    print('OK: _isHuddle initialized from ?huddle=1')
else:
    errors.append('FAIL: _isHuddle state not found')

# ── 4. Init _hmTagged from URL param ──────────────────────────────────────────
OLD4 = '[_hmTagged,_setHmTagged]=(0,_.useState)([])'
NEW4 = '[_hmTagged,_setHmTagged]=(0,_.useState)(()=>{const _inv=i.get(`invite`);return _inv?[{username:_inv}]:[];})'
if OLD4 in content:
    content = content.replace(OLD4, NEW4, 1)
    print('OK: _hmTagged initialized from ?invite=username')
else:
    errors.append('FAIL: _hmTagged state not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
