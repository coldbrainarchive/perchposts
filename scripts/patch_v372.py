#!/usr/bin/env python3
"""Patch v371 -> v372:
- Add Leave/Invite buttons to huddle post page header (matching postcard buttons)
- Add invite state to Wr component
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v371.js'
dst = '_deploy/assets/index-DUcNPOLc-v372.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add invite state to Wr component ───────────────────────────────────────
OLD_WR_STATE = '[_huddleDenied,_setHuddleDenied]=(0,_.useState)(!1),'
NEW_WR_STATE = (
    '[_huddleDenied,_setHuddleDenied]=(0,_.useState)(!1),'
    '[_wpInvOpen,_setWpInvOpen]=(0,_.useState)(!1),'
    '[_wpInvQ,_setWpInvQ]=(0,_.useState)(``),'
    '[_wpInvR,_setWpInvR]=(0,_.useState)([]),'
    '_wpInvTimer=(0,_.useRef)(null),'
)
if OLD_WR_STATE in content:
    content = content.replace(OLD_WR_STATE, NEW_WR_STATE, 1)
    print('OK: invite state added to Wr')
else:
    errors.append('FAIL: Wr state not found')

# ── 2. Add Leave/Invite to the chat header (right side, before sort-toggle) ───
def user_pill(uname, bid='null'):
    return (
        '(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:4,height:22,'
        'padding:`0 7px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,'
        f'background:Hn({bid},{uname}),'
        'color:`#0a0a0a`,fontSize:11,fontWeight:700,whiteSpace:`nowrap`,'
        'lineHeight:1,flexShrink:0,boxSizing:`border-box`},'
        f'children:[(0,L.jsx)(`span`,{{children:(Jn({{username:{uname},browser_id:{bid}}})||{{}}).e||`\U0001f426`}}),'
        f'(0,L.jsx)(`span`,{{children:{uname}}})'
        ']})'
    )

OLD_HDR_RIGHT = (
    '(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:6},children:['
    '(0,L.jsxs)(`div`,{className:`sort-toggle`,children:['
)
NEW_HDR_RIGHT = (
    '(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:6},children:['
    # Leave button for huddles
    'c?.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:()=>{if(!confirm(`Leave this huddle?`))return;'
    'const _un2=localStorage.getItem(`_myUsername`)||null;'
    'fetch(`${R}/leave-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:r,browser_id:Gn(),username:_un2})})'
    '.then(async _r=>{if(_r.ok){nt()(-1);}else{const _j=await _r.json().catch(()=>({}));alert(_j.error||`Could not leave`);}})},'
    'children:`Leave`}),'
    # Invite button for huddles
    'c?.is_huddle&&(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-flex`,alignItems:`center`},children:['
    '(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:()=>{_setWpInvOpen(v=>!v);_setWpInvQ(``);_setWpInvR([]);},'
    'children:`Invite`}),'
    '_wpInvOpen&&(0,L.jsxs)(`div`,{style:{position:`absolute`,top:`calc(100% + 6px)`,right:0,'
    'background:`#1a1d27`,border:`1px solid #374151`,borderRadius:10,padding:10,'
    'zIndex:100,minWidth:240,boxShadow:`0 4px 20px rgba(0,0,0,0.4)`},'
    'onClick:t=>{t.stopPropagation();},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,color:`#94a3b8`,marginBottom:6},children:`Add to huddle:`}),'
    '(0,L.jsx)(`input`,{className:`search-input`,'
    'style:{background:`#0f1117`,border:`1px solid #374151`,borderRadius:6,padding:`4px 8px`,width:`100%`,boxSizing:`border-box`,marginBottom:4},'
    'value:_wpInvQ,'
    'onChange:t=>{_setWpInvQ(t.target.value);clearTimeout(_wpInvTimer.current);'
    '_wpInvTimer.current=setTimeout(()=>{'
    'if(t.target.value.trim()){fetch(`${R}/search-users?q=${encodeURIComponent(t.target.value.trim())}`)'
    '.then(_r=>_r.ok?_r.json():{users:[]}).then(_d=>_setWpInvR(_d.users||[])).catch(()=>_setWpInvR([]));}else{_setWpInvR([]);}},300);},'
    'placeholder:`Search users…`}),'
    '_wpInvR.length>0&&(0,L.jsx)(`div`,{style:{maxHeight:120,overflowY:`auto`},'
    'children:_wpInvR.slice(0,6).map(_u=>(0,L.jsx)(`button`,{type:`button`,'
    'style:{display:`flex`,width:`100%`,padding:`4px 6px`,border:`none`,background:`none`,cursor:`pointer`,borderRadius:6},'
    'onClick:()=>{fetch(`${R}/invite-to-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:r,invite_username:_u.username,browser_id:Gn()})}).then(()=>{_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);});},'
    'children:' + user_pill('_u.username', '_u.browser_id||null') +
    '},_u.username))})'
    ']})'
    ']})'
    ','
    '(0,L.jsxs)(`div`,{className:`sort-toggle`,children:['
)
if OLD_HDR_RIGHT in content:
    content = content.replace(OLD_HDR_RIGHT, NEW_HDR_RIGHT, 1)
    print('OK: Leave/Invite added to post page header')
else:
    errors.append('FAIL: chat header right side not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
