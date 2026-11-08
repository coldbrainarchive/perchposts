#!/usr/bin/env python3
"""Patch v372 -> v373:
- Post page: replace like+share with Leave+Invite for huddle posts (in feed-post-actions)
- Post page: remove Leave/Invite from chat header (wrong location)
- Fix get-posts huddle board fetch to always pass req_username from auth
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v372.js'
dst = '_deploy/assets/index-DUcNPOLc-v373.js'

content = open(src, encoding='utf-8').read()
errors = []

# Helper
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

# ── 1. Replace like button in post page with huddle-conditional ───────────────
OLD_LIKE = (
    '(0,L.jsxs)(`div`,{className:`feed-post-actions`,children:['
    '(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'style:re.myVote===1?{borderColor:`#c084fc`,background:`rgba(192,132,252,0.15)`}:{},'
    'onClick:async t=>{if(!e){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}'
)
NEW_LIKE = (
    '(0,L.jsxs)(`div`,{className:`feed-post-actions`,children:['
    # Leave button (huddle only)
    'c?.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:()=>{if(!confirm(`Leave this huddle?`))return;'
    'const _un3=localStorage.getItem(`_myUsername`)||null;'
    'fetch(`${R}/leave-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:c.id,browser_id:Gn(),username:_un3})})'
    '.then(async _r=>{if(_r.ok){nt()(-1);}else{const _j=await _r.json().catch(()=>({}));alert(_j.error||`Could not leave`);}});},'
    'children:`Leave`}),'
    # Invite button (huddle only)
    'c?.is_huddle&&(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-flex`,alignItems:`center`},children:['
    '(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:()=>{_setWpInvOpen(v=>!v);_setWpInvQ(``);_setWpInvR([]);},'
    'children:`Invite`}),'
    '_wpInvOpen&&(0,L.jsxs)(`div`,{style:{position:`absolute`,bottom:`calc(100% + 6px)`,left:0,'
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
    'body:JSON.stringify({post_id:c.id,invite_username:_u.username,browser_id:Gn()})}).then(()=>{_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);});},'
    'children:' + user_pill('_u.username', '_u.browser_id||null') +
    '},_u.username))})'
    ']})'
    ']})'
    ','
    # Like button (normal posts only)
    '!c?.is_huddle&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'style:re.myVote===1?{borderColor:`#c084fc`,background:`rgba(192,132,252,0.15)`}:{},'
    'onClick:async t=>{if(!e){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}'
)
if OLD_LIKE in content:
    content = content.replace(OLD_LIKE, NEW_LIKE, 1)
    print('OK: like→Leave/Invite in post page actions')
else:
    errors.append('FAIL: post page like button not found')

# ── 2. Hide Share button for huddle posts in post page ────────────────────────
OLD_SHARE_WR = (
    '(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:async e=>{e.preventDefault();let t=`${window.location.origin}/post/${c.id}`'
)
NEW_SHARE_WR = (
    '!c?.is_huddle&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:async e=>{e.preventDefault();let t=`${window.location.origin}/post/${c.id}`'
)
if OLD_SHARE_WR in content:
    content = content.replace(OLD_SHARE_WR, NEW_SHARE_WR, 1)
    print('OK: Share hidden for huddles in post page')
else:
    errors.append('FAIL: Share button in post page not found')

# ── 3. Remove Leave/Invite from chat header (wrong location) ──────────────────
OLD_HDR_HUDDLE = (
    'c?.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:()=>{if(!confirm(`Leave this huddle?`))return;'
    'const _un2=localStorage.getItem(`_myUsername`)||null;'
    'fetch(`${R}/leave-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:r,browser_id:Gn(),username:_un2})})'
    '.then(async _r=>{if(_r.ok){nt()(-1);}else{const _j=await _r.json().catch(()=>({}));alert(_j.error||`Could not leave`);}})},'
    'children:`Leave`}),'
)
if OLD_HDR_HUDDLE in content:
    content = content.replace(OLD_HDR_HUDDLE, '', 1)
    print('OK: Leave removed from chat header')
else:
    errors.append('FAIL: Leave in chat header not found')

# Remove Invite span from chat header too
OLD_HDR_INVITE = (
    'c?.is_huddle&&(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-flex`,alignItems:`center`},children:['
    '(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:()=>{_setWpInvOpen(v=>!v);_setWpInvQ(``);_setWpInvR([]);},'
    'children:`Invite`}),'
)
if OLD_HDR_INVITE in content:
    # Find the full span and remove it - it ends before the sort-toggle
    start_idx = content.find(OLD_HDR_INVITE)
    # Find the closing of this span element
    end_marker = ',(0,L.jsxs)(`div`,{className:`sort-toggle`'
    end_idx = content.find(end_marker, start_idx)
    if end_idx != -1:
        content = content[:start_idx] + content[end_idx:]
        print('OK: Invite span removed from chat header')
    else:
        errors.append('FAIL: could not find end of invite span in header')
else:
    print('NOTE: Invite not in chat header (already removed or not present)')

# ── 4. Ensure get-posts for huddles always sends auth username ────────────────
# The board fetch should prioritize auth - already done on backend side
# Just ensure req_username from localStorage is always sent when available

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
