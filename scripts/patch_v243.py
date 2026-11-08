#!/usr/bin/env python3
"""Patch v242 -> v243: restore Notifications tab, add Inbox between Notifications and Your Nest."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v242.js'
dst = '_deploy/assets/index-DUcNPOLc-v243.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Restore tabs: Notifications | Inbox | Your Nest ───────────────────────
OLD_TABS = 'M=e?[{id:`inbox`,label:`Inbox`},{id:`account`,label:`Your Nest`}]:[{id:`account`,label:`Your Nest`}]'
NEW_TABS = 'M=e?[{id:`notifications`,label:`Notifications`},{id:`inbox`,label:`Inbox`},{id:`account`,label:`Your Nest`}]:[{id:`account`,label:`Your Nest`}]'
if OLD_TABS in content:
    content = content.replace(OLD_TABS, NEW_TABS, 1)
    print('OK: tabs restored to Notifications | Inbox | Your Nest')
else:
    errors.append('FAIL: tabs array not found')

# ── 2. Change initial tab back to notifications ───────────────────────────────
OLD_INIT = 'let[c,l]=(0,_.useState)(e?`inbox`:`account`)'
NEW_INIT = 'let[c,l]=(0,_.useState)(e?`notifications`:`account`)'
if OLD_INIT in content:
    content = content.replace(OLD_INIT, NEW_INIT, 1)
    print('OK: initial tab restored to notifications')
else:
    errors.append('FAIL: initial tab state not found')

# ── 3. Add notifications fetch effect alongside inbox effect ──────────────────
OLD_EFF = 'c===`inbox`&&!_dmThread&&(async()=>{let _r=await fetch(`${R}/dm-inbox`,{headers:er()});_setDmConvs((_r.ok?await _r.json():{}).conversations||[])})()},[c,_dmThread,e])'
NEW_EFF = (
    'c===`inbox`&&!_dmThread&&(async()=>{let _r=await fetch(`${R}/dm-inbox`,{headers:er()});'
    '_setDmConvs((_r.ok?await _r.json():{}).conversations||[])})()},[c,_dmThread,e]);'
    '(0,_.useEffect)(()=>{'
    'c===`notifications`&&(v(!0),(async()=>{let t=new URLSearchParams({browser_id:k});'
    'D&&e?t.set(`mod_user_id`,e.id):r&&t.set(`username`,r),i&&t.set(`exclude_username`,i);'
    'let n=await fetch(`${R}/notifications?${t}`,{headers:er()});'
    'h((n.ok?await n.json():{}).notifs||[]),v(!1)})())},[c,e,r]'
)
if OLD_EFF in content:
    content = content.replace(OLD_EFF, NEW_EFF, 1)
    print('OK: notifications fetch effect restored')
else:
    errors.append('FAIL: inbox effect anchor not found')

# ── 4. Add notifications render before inbox render ───────────────────────────
OLD_INBOX_RENDER = "children:[c===`inbox`&&(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,flex:1}"
NEW_INBOX_RENDER = (
    "children:["
    "c===`notifications`&&(0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`},"
    "children:g?(0,L.jsx)(`div`,{style:{padding:32,color:`#64748b`,textAlign:`center`,fontSize:14},children:`Loading…`}):"
    "j.length===0?(0,L.jsxs)(`div`,{style:{padding:`48px 20px`,color:`#64748b`,textAlign:`center`},"
    "children:[(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600},children:`No notifications yet`}),"
    "(0,L.jsx)(`div`,{style:{fontSize:12,marginTop:4},children:`Activity on your posts and comments shows up here`})]}):"
    "j.map(e=>{let t=!!e.time&&e.time>ee.current;"
    "return(0,L.jsxs)(I,{to:e.postId?`/post/${e.postId}${e.targetId?`?highlight=${e.targetId}`:``}`:`#`,"
    "onClick:a,style:{display:`flex`,alignItems:`flex-start`,gap:12,padding:`12px 18px`,"
    "textDecoration:`none`,borderBottom:`1px solid #1a1c23`,background:t?`rgba(192,132,252,0.07)`:`transparent`},"
    "children:[(0,L.jsx)(`span`,{style:{fontSize:20,lineHeight:1,flexShrink:0},children:e.icon}),"
    "(0,L.jsxs)(`div`,{style:{flex:1,minWidth:0},"
    "children:[(0,L.jsx)(`div`,{style:{color:t?`#f8fafc`:`#94a3b8`,fontSize:13,lineHeight:1.4},children:e.text}),"
    "(0,L.jsx)(`div`,{style:{color:`#475569`,fontSize:11,marginTop:3},children:Un(e.time)})]})]},"
    "e.id)})}),c===`inbox`&&(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,flex:1}"
)
if OLD_INBOX_RENDER in content:
    content = content.replace(OLD_INBOX_RENDER, NEW_INBOX_RENDER, 1)
    print('OK: notifications render restored before inbox')
else:
    errors.append('FAIL: inbox render anchor not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

opens_p = content.count('(')
closes_p = content.count(')')
opens_b = content.count('{')
closes_b = content.count('}')
print(f'Parens: {opens_p-closes_p}, Braces: {opens_b-closes_b}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
