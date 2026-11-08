#!/usr/bin/env python3
"""Patch v374 -> v375:
- Post page Leave: navigate to /huddles after leaving (instead of history back)
- System comment rendering: render __system__ comments as subtle activity messages
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v374.js'
dst = '_deploy/assets/index-DUcNPOLc-v375.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Post page Leave button: navigate to /huddles instead of back ────────────
OLD_LEAVE_NAV = (
    '.then(async _r=>{if(_r.ok){nt()(-1);}else{const _j=await _r.json().catch(()=>({}));alert(_j.e'
)
NEW_LEAVE_NAV = (
    '.then(async _r=>{if(_r.ok){window.location.href=`/huddles`;}else{const _j=await _r.json().catch(()=>({}));alert(_j.e'
)
if OLD_LEAVE_NAV in content:
    content = content.replace(OLD_LEAVE_NAV, NEW_LEAVE_NAV, 1)
    print('OK: post page Leave navigates to /huddles')
else:
    errors.append('FAIL: post page Leave nav not found')

# ── 2. System comment rendering ────────────────────────────────────────────────
# Insert early return before the main comment JSX return for __system__ comments
OLD_COMMENT_RETURN = (
    '}function O(t){let n=[...t.target.value].find(e=>/\\p{Emoji}/u.test(e)&&e!==`‍`);'
    'n&&(c&&c(e.id,n),t.target.value=``,x(!1))}'
    'return(0,L.jsx)(`div`,{className:`chat-msg${_isMe?` chat-msg--mine`:``}`'
)
NEW_COMMENT_RETURN = (
    '}function O(t){let n=[...t.target.value].find(e=>/\\p{Emoji}/u.test(e)&&e!==`‍`);'
    'n&&(c&&c(e.id,n),t.target.value=``,x(!1))}'
    'if(e.username===`__system__`)return(0,L.jsx)(`div`,{'
    'style:{textAlign:`center`,color:`#64748b`,fontSize:12,padding:`6px 0`,fontStyle:`italic`,userSelect:`none`},'
    'children:e.content});'
    'return(0,L.jsx)(`div`,{className:`chat-msg${_isMe?` chat-msg--mine`:``}`'
)
if OLD_COMMENT_RETURN in content:
    content = content.replace(OLD_COMMENT_RETURN, NEW_COMMENT_RETURN, 1)
    print('OK: system comment rendering added')
else:
    errors.append('FAIL: comment return not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
