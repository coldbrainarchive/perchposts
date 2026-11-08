#!/usr/bin/env python3
"""Patch v372 -> v374:
- Remove Leave/Invite from chat header (wrong location added in v372)
- Add Leave/Invite to feed-post-actions in post page (replacing like/share for huddles)
- Hide like/share for huddle posts in post page
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v372.js'
dst = '_deploy/assets/index-DUcNPOLc-v374.js'

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

# ── 1. Remove Leave/Invite from chat header (revert v372 change) ──────────────
# This is the exact string added by v372 patch (with Leave/Invite in wrong place)
OLD_HDR = (
    '(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:6},children:['
    'c?.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:()=>{if(!confirm(`Leave this huddle?`))return;'
    'const _un2=localStorage.getItem(`_myUsername`)||null;'
    'fetch(`${R}/leave-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:r,browser_id:Gn(),username:_un2})})'
    '.then(async _r=>{if(_r.ok){nt()(-1);}else{const _j=await _r.json().catch(()=>({}));alert(_j.error||`Could not leave`);}})}'
    ',children:`Leave`}),'
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
    'body:JSON.stringify({post_id:r,invite_username:_u.username,browser_id:Gn()})}).then(()=>{_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);});}'
    ',children:' + user_pill('_u.username', '_u.browser_id||null') +
    '},_u.username))})'
    ']})'
    ']})'
    ','
    '(0,L.jsxs)(`div`,{className:`sort-toggle`,children:['
)
NEW_HDR = (
    '(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:6},children:['
    '(0,L.jsxs)(`div`,{className:`sort-toggle`,children:['
)
if OLD_HDR in content:
    content = content.replace(OLD_HDR, NEW_HDR, 1)
    print('OK: Leave/Invite removed from chat header')
else:
    errors.append('FAIL: chat header Leave/Invite not found')

# ── 2. Replace like button in post page feed-post-actions with huddle conditional ──
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

# ── 3. Hide Share button for huddle posts in post page ────────────────────────
OLD_SHARE = (
    '(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:async e=>{e.preventDefault();let t=`${window.location.origin}/post/${c.id}`'
)
NEW_SHARE = (
    '!c?.is_huddle&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'onClick:async e=>{e.preventDefault();let t=`${window.location.origin}/post/${c.id}`'
)
if OLD_SHARE in content:
    content = content.replace(OLD_SHARE, NEW_SHARE, 1)
    print('OK: Share hidden for huddles in post page')
else:
    errors.append('FAIL: Share button in post page not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
