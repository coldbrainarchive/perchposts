#!/usr/bin/env python3
"""Patch v368 -> v369:
- Huddle post cards: replace like+share with Leave+Invite buttons
- Invite opens a user-search dropdown (same style as new post huddle form)
- Leave calls /leave-huddle
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v368.js'
dst = '_deploy/assets/index-DUcNPOLc-v369.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add invite state to Ir component ──────────────────────────────────────
OLD_IR_STATE = (
    'function Ir({post:e,commentCount:t=0,score:n=0,myVote:r=0,onVote:i,showActivity:a=!1})'
    '{let[o,s]=(0,_.useState)(`Share`),[c,l]=(0,_.useState)(!1),'
)
NEW_IR_STATE = (
    'function Ir({post:e,commentCount:t=0,score:n=0,myVote:r=0,onVote:i,showActivity:a=!1})'
    '{let[o,s]=(0,_.useState)(`Share`),[c,l]=(0,_.useState)(!1),'
    '[_invOpen,_setInvOpen]=(0,_.useState)(!1),'
    '[_invQ,_setInvQ]=(0,_.useState)(``),'
    '[_invR,_setInvR]=(0,_.useState)([]),'
    '_invTimer=(0,_.useRef)(null),'
    '[_invSending,_setInvSending]=(0,_.useState)(!1),'
)
if OLD_IR_STATE in content:
    content = content.replace(OLD_IR_STATE, NEW_IR_STATE, 1)
    print('OK: invite state added to Ir')
else:
    errors.append('FAIL: Ir state not found')

# ── 2. Replace the feed-post-actions row for huddle vs normal ─────────────────
# The actions row: like button + comments + share + time
# For huddles: hide like+share, show Leave+Invite instead

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

OLD_ACTIONS = (
    'className:`feed-post-actions`,children:['
    '(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'style:r===1&&i?{borderColor:`#c084fc`,background:`rgba(192,132,252,0.15)`}:{},'
    'onClick:t=>{t.preventDefault(),t.stopPropagation(),i?i(e.id,r===1?0:1):window.dispatchEvent(new CustomEvent(`like-no-auth`))},'
    'children:[(0,L.jsx)(`span`,{children:`👍`}),(0,L.jsx)(`span`,{children:n})]}),'
)
NEW_ACTIONS = (
    'className:`feed-post-actions`,children:['
    '!(e.is_huddle||e.community_id===`feedback`)&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'style:r===1&&i?{borderColor:`#c084fc`,background:`rgba(192,132,252,0.15)`}:{},'
    'onClick:t=>{t.preventDefault(),t.stopPropagation(),i?i(e.id,r===1?0:1):window.dispatchEvent(new CustomEvent(`like-no-auth`))},'
    'children:[(0,L.jsx)(`span`,{children:`👍`}),(0,L.jsx)(`span`,{children:n})]}),'
    # Leave button (huddle only)
    '(e.is_huddle||e.community_id===`feedback`)&&(0,L.jsx)(`button`,{type:`button`,'
    'className:`feed-post-action-pill`,'
    'onClick:t=>{t.preventDefault();t.stopPropagation();'
    'if(!confirm(`Leave this huddle?`))return;'
    'const _bid=Gn(),_un=localStorage.getItem(`_myUsername`)||null;'
    'fetch(`${R}/leave-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:e.id,browser_id:_bid,username:_un})}).then(()=>window.location.reload());'
    '},children:`Leave`}),'
    # Invite button (huddle only) - relative positioned for dropdown
    '(e.is_huddle||e.community_id===`feedback`)&&(0,L.jsxs)(`span`,{style:{position:`relative`},children:['
    '(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:t=>{t.preventDefault();t.stopPropagation();_setInvOpen(v=>!v);_setInvQ(``);_setInvR([]);},'
    'children:`Invite`}),'
    '_invOpen&&(0,L.jsxs)(`div`,{style:{position:`absolute`,bottom:`calc(100% + 6px)`,left:0,'
    'background:`#1a1d27`,border:`1px solid #374151`,borderRadius:10,padding:10,'
    'zIndex:100,minWidth:240,boxShadow:`0 4px 20px rgba(0,0,0,0.4)`},'
    'onClick:t=>{t.stopPropagation();},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,color:`#94a3b8`,marginBottom:6},children:`Add to huddle:`}),'
    '(0,L.jsx)(`input`,{className:`search-input`,'
    'style:{background:`#0f1117`,border:`1px solid #374151`,borderRadius:6,padding:`4px 8px`,width:`100%`,boxSizing:`border-box`,marginBottom:4},'
    'value:_invQ,'
    'onChange:t=>{_setInvQ(t.target.value);clearTimeout(_invTimer.current);'
    '_invTimer.current=setTimeout(()=>{'
    'if(t.target.value.trim()){fetch(`${R}/search-users?q=${encodeURIComponent(t.target.value.trim())}`)'
    '.then(r=>r.ok?r.json():{users:[]}).then(d=>_setInvR(d.users||[])).catch(()=>_setInvR([]));}else{_setInvR([]);}},300);},'
    'placeholder:`Search users…`}),'
    '_invR.length>0&&(0,L.jsx)(`div`,{style:{maxHeight:120,overflowY:`auto`},'
    'children:_invR.slice(0,6).map(_u=>(0,L.jsx)(`button`,{type:`button`,'
    'style:{display:`flex`,width:`100%`,padding:`4px 6px`,border:`none`,background:`none`,cursor:`pointer`,borderRadius:6},'
    'onClick:()=>{if(_invSending)return;_setInvSending(!0);'
    'fetch(`${R}/invite-to-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:e.id,invite_username:_u.username,browser_id:Gn()})}).then(()=>{_setInvR([]);_setInvQ(``);_setInvOpen(!1);}).finally(()=>_setInvSending(!1));},'
    'children:' + user_pill('_u.username', '_u.browser_id||null') +
    '},_u.username))})'
    ']})'  # close dropdown div
    ']})'  # close span
    ','
)
if OLD_ACTIONS in content:
    content = content.replace(OLD_ACTIONS, NEW_ACTIONS, 1)
    print('OK: huddle actions (Leave/Invite) added, like hidden for huddles')
else:
    errors.append('FAIL: feed-post-actions not found')

# ── 3. Hide Share button for huddles ──────────────────────────────────────────
OLD_SHARE = (
    '(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:h,'
    'children:[(0,L.jsx)(`span`,{children:`↗`}),(0,L.jsx)(`span`,{children:o})]})'
)
NEW_SHARE = (
    '!(e.is_huddle||e.community_id===`feedback`)&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:h,'
    'children:[(0,L.jsx)(`span`,{children:`↗`}),(0,L.jsx)(`span`,{children:o})]})'
)
if OLD_SHARE in content:
    content = content.replace(OLD_SHARE, NEW_SHARE, 1)
    print('OK: Share button hidden for huddles')
else:
    errors.append('FAIL: Share button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
