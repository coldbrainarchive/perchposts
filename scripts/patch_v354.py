#!/usr/bin/env python3
"""Patch v353 -> v354: Huddles feature frontend.
- POST/HUDDLE toggle on new post page
- Huddle form (title optional + member search picker)
- Remove Huddles board from normal post board picker
- Get-post passes req_username/browser_id, handles 403 access denied
- Get-posts passes req_username/browser_id for huddles board membership filtering
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v353.js'
dst = '_deploy/assets/index-DUcNPOLc-v354.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add huddle state variables to Ur component ─────────────────────────────
OLD_STATE = (
    '[ne,re]=(0,_.useState)(!1),'
    '_npSrch,_setNpSrch]=(0,_.useState)(``),'
)
# The full state chain end (from v353 with search state)
OLD_STATE_FULL = (
    '[ne,re]=(0,_.useState)(!1),'
    'ie=(0,_.useRef)(null),j=(0,_.useRef)(null)'
)
NEW_STATE_FULL = (
    '[ne,re]=(0,_.useState)(!1),'
    '[_isHuddle,_setIsHuddle]=(0,_.useState)(!1),'
    '[_hmTagQ,_setHmTagQ]=(0,_.useState)(``),'
    '[_hmTagR,_setHmTagR]=(0,_.useState)([]),'
    '[_hmTagged,_setHmTagged]=(0,_.useState)([]),'
    '_hmTimer=(0,_.useRef)(null),'
    'ie=(0,_.useRef)(null),j=(0,_.useRef)(null)'
)
if OLD_STATE_FULL in content:
    content = content.replace(OLD_STATE_FULL, NEW_STATE_FULL, 1)
    print('OK: huddle state vars added to Ur')
else:
    errors.append('FAIL: Ur state chain not found')

# ── 2. Add POST/HUDDLE toggle before content-card ─────────────────────────────
OLD_NAV = "children:`New post`})]}),(0,L.jsxs)(`div`,{className:`content-card feed-post-card`"
NEW_NAV = (
    "children:`New post`})]})"
    ",(0,L.jsxs)(`div`,{style:{display:`flex`,gap:6,padding:`4px 0 10px`},children:["
    "(0,L.jsx)(`button`,{type:`button`,"
    "onClick:()=>{_setIsHuddle(!1);_setHmTagged([]);_setHmTagQ(``);},"
    "style:{padding:`4px 12px`,borderRadius:999,border:`1px solid rgba(148,163,184,0.3)`,"
    "background:_isHuddle?`transparent`:`#a855f7`,color:_isHuddle?`#94a3b8`:`#fff`,"
    "fontSize:12,fontWeight:700,cursor:`pointer`,letterSpacing:`0.04em`},"
    "children:`POST`}),"
    "(0,L.jsx)(`button`,{type:`button`,"
    "onClick:()=>{_setIsHuddle(!0);},"
    "style:{padding:`4px 12px`,borderRadius:999,border:`1px solid rgba(148,163,184,0.3)`,"
    "background:_isHuddle?`#a855f7`:`transparent`,color:_isHuddle?`#fff`:`#94a3b8`,"
    "fontSize:12,fontWeight:700,cursor:`pointer`,letterSpacing:`0.04em`},"
    "children:`\U0001f465 HUDDLE`})"
    "]})"
    ",(0,L.jsxs)(`div`,{className:`content-card feed-post-card`"
)
if OLD_NAV in content:
    content = content.replace(OLD_NAV, NEW_NAV, 1)
    print('OK: POST/HUDDLE toggle added')
else:
    errors.append('FAIL: nav/card boundary not found')

# ── 3. Hide board picker when huddle mode ──────────────────────────────────────
OLD_HDR = "className:`feed-post-header`,children:"
NEW_HDR = "className:`feed-post-header`,style:{display:_isHuddle?`none`:``},children:"
if OLD_HDR in content:
    content = content.replace(OLD_HDR, NEW_HDR, 1)
    print('OK: board picker hidden when huddle')
else:
    errors.append('FAIL: feed-post-header not found')

# ── 4. Remove Huddles/feedback board from normal board picker ──────────────────
OLD_BOARD_FILTER = (
    'nr.filter(e=>!e.virtual&&e.slug!==`feedback`&&(!_npSrch||e.name.toLowerCase().includes(_npSrch.toLowerCase())||e.slug.toLowerCase().includes(_npSrch.toLowerCase()))).map('
)
# Check what the current filter looks like
import re
board_filter_m = re.search(r'nr\.filter\(e=>!e\.virtual[^)]*\)\.map\(e=>\(0,L\.jsx\)\(`button`,\{className:`search-suggestion`', content)
if board_filter_m:
    old_bf = content[board_filter_m.start():board_filter_m.end()]
    # Check if feedback is already excluded
    if '`feedback`' not in old_bf:
        new_bf = old_bf.replace('nr.filter(e=>!e.virtual', 'nr.filter(e=>!e.virtual&&e.slug!==`feedback`', 1)
        content = content.replace(old_bf, new_bf, 1)
        print('OK: feedback board excluded from picker')
    else:
        print('OK: feedback already excluded from picker')
else:
    errors.append('FAIL: board filter map not found')

# ── 5. Make title placeholder conditional + add huddle member picker ───────────
OLD_TITLE = (
    'value:a,onChange:e=>o(e.target.value),'
    'placeholder:`Give the thread a title…`,'
    'disabled:l,'
)
NEW_TITLE = (
    'value:a,onChange:e=>o(e.target.value),'
    'placeholder:_isHuddle?`Give this huddle a title (optional)`:`Give the thread a title…`,'
    'disabled:l,'
)
if OLD_TITLE in content:
    content = content.replace(OLD_TITLE, NEW_TITLE, 1)
    print('OK: title placeholder conditional')
else:
    errors.append('FAIL: title input not found')

# ── 6. Hide content textarea when huddle + show member picker ──────────────────
OLD_TEXTAREA = (
    'value:s,onChange:e=>c(e.target.value),'
    'placeholder:T?`Add a caption (optional)…`:`What\'s going on?`,'
    'disabled:l,rows:5,'
)
NEW_TEXTAREA = (
    'value:s,onChange:e=>c(e.target.value),'
    'placeholder:T?`Add a caption (optional)…`:`What\'s going on?`,'
    'disabled:l,rows:5,'
    'style:{...({width:`100%`,boxSizing:`border-box`,padding:0,border:`none`,fontSize:16,'
    'resize:`none`,background:`transparent`,color:`#d4dde7`,outline:`none`,'
    'minHeight:90,fontFamily:`inherit`,lineHeight:1.6,touchAction:`manipulation`}),'
    'display:_isHuddle?`none`:``},'
)
# This is tricky - the textarea style is inline. Let me find the exact textarea string.
OLD_TA2 = (
    "(0,L.jsx)(`textarea`,{value:s,onChange:e=>c(e.target.value),"
    "placeholder:T?`Add a caption (optional)…`:`What’s going on?`,"
    "disabled:l,rows:5,style:{width:`100%`,boxSizing:`border-box`,padding:0,"
    "border:`none`,fontSize:16,resize:`none`,background:`transparent`,color:`#d4dde7`,"
    "outline:`none`,minHeight:90,fontFamily:`inherit`,lineHeight:1.6,touchAction:`manipulation`}})"
)
NEW_TA2 = (
    # The huddle member picker (shown when _isHuddle)
    '_isHuddle&&(0,L.jsxs)(`div`,{style:{marginTop:6},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:12,color:`#94a3b8`,marginBottom:6},'
    'children:`Add the users you want in this huddle:`}),'
    '_hmTagged.length>0&&(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:4,marginBottom:6},'
    'children:_hmTagged.map(_u=>(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,'
    'gap:4,padding:`2px 8px`,borderRadius:999,background:`rgba(168,85,247,0.15)`,'
    'border:`1px solid rgba(168,85,247,0.4)`,fontSize:12,color:`#c084fc`},'
    'children:[`@`,_u.username,'
    '(0,L.jsx)(`button`,{type:`button`,onClick:()=>_setHmTagged(_hmTagged.filter(_t=>_t.username!==_u.username)),'
    'style:{background:`none`,border:`none`,color:`#c084fc`,cursor:`pointer`,padding:`0 0 0 2px`,fontSize:11},'
    'children:`\xd7`})]},_u.username))})'
    ','
    '(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8,'
    'padding:`4px 8px`,borderRadius:8,border:`1px solid #374151`,background:`#0f1117`},'
    'children:['
    '(0,L.jsx)(`span`,{style:{fontSize:14,flexShrink:0},children:`\U0001f465`}),'
    '(0,L.jsx)(`input`,{value:_hmTagQ,'
    'onChange:e=>{_setHmTagQ(e.target.value);clearTimeout(_hmTimer.current);'
    '_hmTimer.current=setTimeout(()=>{'
    'if(e.target.value.trim()){fetch(`${R}/search-users?q=${encodeURIComponent(e.target.value.trim())}`)'
    '.then(_r=>_r.ok?_r.json():{users:[]})'
    '.then(_d=>_setHmTagR(_d.users||[]))'
    '.catch(()=>_setHmTagR([]));}else{_setHmTagR([]);}},300);},'
    'placeholder:`+ USER`,'
    'style:{flex:1,background:`transparent`,border:`none`,color:`#e2e8f0`,'
    'fontSize:13,outline:`none`}})'
    ']})'
    ','
    '_hmTagR.length>0&&(0,L.jsx)(`div`,{style:{marginTop:4,maxHeight:140,overflowY:`auto`,'
    'borderRadius:8,border:`1px solid #374151`,background:`#0f1117`},'
    'children:_hmTagR.filter(_u=>!_hmTagged.find(_t=>_t.username===_u.username)).slice(0,8)'
    '.map(_u=>(0,L.jsx)(`button`,{type:`button`,'
    'onClick:()=>{_setHmTagged([..._hmTagged,_u]);_setHmTagQ(``);_setHmTagR([]);},'
    'style:{display:`block`,width:`100%`,padding:`6px 10px`,border:`none`,'
    'background:`none`,color:`#e2e8f0`,fontSize:13,textAlign:`left`,cursor:`pointer`},'
    'children:`@${_u.username}`},_u.username))})'
    ']})'
    ','
    # Normal textarea (hidden when huddle)
    "!_isHuddle&&(0,L.jsx)(`textarea`,{value:s,onChange:e=>c(e.target.value),"
    "placeholder:T?`Add a caption (optional)…`:`What's going on?`,"
    "disabled:l,rows:5,style:{width:`100%`,boxSizing:`border-box`,padding:0,"
    "border:`none`,fontSize:16,resize:`none`,background:`transparent`,color:`#d4dde7`,"
    "outline:`none`,minHeight:90,fontFamily:`inherit`,lineHeight:1.6,touchAction:`manipulation`}})"
)
if OLD_TA2 in content:
    content = content.replace(OLD_TA2, NEW_TA2, 1)
    print('OK: huddle member picker added, textarea hidden when huddle')
else:
    errors.append('FAIL: textarea not found for member picker replacement')

# ── 7. Modify submit to include huddle data ────────────────────────────────────
OLD_SUBMIT = (
    'JSON.stringify({title:a,content:T?s+jr+JSON.stringify(T)+`]`:s,'
    'board:d.name,category:d.name,community_id:d.slug,'
    'continent:null,country:v||null,browser_id:f,...t})'
)
NEW_SUBMIT = (
    'JSON.stringify({title:a||(_isHuddle?null:null),'
    'content:_isHuddle?`Huddle with: ${[n,..._hmTagged.map(_u=>_u.username)].filter(Boolean).join(", ")}`:(T?s+jr+JSON.stringify(T)+`]`:s),'
    'board:_isHuddle?`Huddles`:d.name,'
    'category:_isHuddle?`Huddles`:d.name,'
    'community_id:_isHuddle?`feedback`:d.slug,'
    'continent:null,country:_isHuddle?null:(v||null),'
    'browser_id:f,'
    'is_huddle:_isHuddle,'
    'huddle_members:_isHuddle?_hmTagged.map(_u=>_u.username):[],'
    '...t})'
)
if OLD_SUBMIT in content:
    content = content.replace(OLD_SUBMIT, NEW_SUBMIT, 1)
    print('OK: submit includes huddle data')
else:
    errors.append('FAIL: submit JSON.stringify not found')

# ── 8. Pass req_username/browser_id to get-posts for huddles board ────────────
OLD_BOARD_FETCH = (
    'if(u&&u!==`activity`)turl+=`&board=${encodeURIComponent(u)}`;'
    'if(d)turl+=`&continent=${encodeURIComponent(d)}`;'
    'if(f)turl+=`&country=${encodeURIComponent(f)}`;'
    'if(p)turl+=`&username=${encodeURIComponent(p)}`;'
    'fetch(turl).then(r2=>r2.ok?r2.json():{posts:[]}).then(d2=>{setTagR(Sr(d2.posts||[]))}).catch(()=>setTagR(null))'
)
NEW_BOARD_FETCH = (
    'if(u&&u!==`activity`)turl+=`&board=${encodeURIComponent(u)}`;'
    'if(d)turl+=`&continent=${encodeURIComponent(d)}`;'
    'if(f)turl+=`&country=${encodeURIComponent(f)}`;'
    'if(p)turl+=`&username=${encodeURIComponent(p)}`;'
    'if(u&&(u===`feedback`||u===`huddles`)){const _bid=Gn();const _un=localStorage.getItem(`_myUsername`)||null;if(_bid)turl+=`&req_browser_id=${encodeURIComponent(_bid)}`;if(_un)turl+=`&req_username=${encodeURIComponent(_un)}`;}'
    'fetch(turl).then(r2=>r2.ok?r2.json():{posts:[]}).then(d2=>{setTagR(Sr(d2.posts||[]))}).catch(()=>setTagR(null))'
)
if OLD_BOARD_FETCH in content:
    content = content.replace(OLD_BOARD_FETCH, NEW_BOARD_FETCH, 1)
    print('OK: huddles board fetch passes req_username/browser_id')
else:
    errors.append('FAIL: board fetch not found')

# ── 9. Pass req params to get-post + handle 403 huddle access denied ──────────
OLD_GETPOST = (
    'let e=await fetch(`${R}/get-post?id=${r}`);if(!e.ok)return;'
    'let{post:t,comments:n}=await e.json();'
)
NEW_GETPOST = (
    'const _bid2=Gn(),_un2=localStorage.getItem(`_myUsername`)||null;'
    'let _gpUrl=`${R}/get-post?id=${r}&req_browser_id=${encodeURIComponent(_bid2)}`;'
    'if(_un2)_gpUrl+=`&req_username=${encodeURIComponent(_un2)}`;'
    'let e=await fetch(_gpUrl);'
    'if(e.status===403){const _errJ=await e.json().catch(()=>({}));if(_errJ.huddle)_setHuddleDenied(!0);return;}'
    'if(!e.ok)return;'
    'let{post:t,comments:n}=await e.json();'
)
if OLD_GETPOST in content:
    content = content.replace(OLD_GETPOST, NEW_GETPOST, 1)
    print('OK: get-post passes req params + handles 403')
else:
    errors.append('FAIL: get-post fetch not found')

# ── 10. Add _huddleDenied state to Wr component ────────────────────────────────
OLD_WR_STATE = 'function Wr({user:e,userRole:t,memberUsername:n}){let{id:r}=it(),'
NEW_WR_STATE = 'function Wr({user:e,userRole:t,memberUsername:n}){let{id:r}=it(),_setHuddleDenied_ref=(0,_.useRef)(null),'
# Actually let's use useState
OLD_WR_STATE2 = "function Wr({user:e,userRole:t,memberUsername:n}){let{id:r}=it(),[i]=kn(),a=i.get(`highlight`),"
NEW_WR_STATE2 = "function Wr({user:e,userRole:t,memberUsername:n}){let{id:r}=it(),[_huddleDenied,_setHuddleDenied]=(0,_.useState)(!1),[i]=kn(),a=i.get(`highlight`),"
if OLD_WR_STATE2 in content:
    content = content.replace(OLD_WR_STATE2, NEW_WR_STATE2, 1)
    print('OK: _huddleDenied state added to Wr')
else:
    errors.append('FAIL: Wr state not found')

# ── 11. Show access denied page in Wr when huddleDenied ───────────────────────
OLD_LOADING = "if(!c)return(0,L.jsx)(`div`,{children:`Loading...`});"
NEW_LOADING = (
    "if(_huddleDenied)return(0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`,"
    "alignItems:`center`,justifyContent:`center`,padding:40,textAlign:`center`,color:`#94a3b8`},"
    "children:[(0,L.jsx)(`div`,{style:{fontSize:32,marginBottom:12},children:`\U0001f465`}),"
    "(0,L.jsx)(`div`,{style:{fontSize:16,fontWeight:700,color:`#f8fafc`,marginBottom:6},"
    "children:`Members only`}),"
    "(0,L.jsx)(`div`,{style:{fontSize:13},children:`You're not a member of this huddle.`})]});"
    "if(!c)return(0,L.jsx)(`div`,{children:`Loading...`});"
)
if OLD_LOADING in content:
    content = content.replace(OLD_LOADING, NEW_LOADING, 1)
    print('OK: huddle access denied page added')
else:
    errors.append('FAIL: loading check not found')

# ── 12. Store username in localStorage when logged in (for req_username) ────────
# Find where myUsername is set in the my-username fetch
OLD_MY_UN = "t.ok&&ee((await t.json()).username||null)"
NEW_MY_UN = "t.ok&&(async()=>{const _u=(await t.json()).username||null;ee(_u);if(_u)localStorage.setItem(`_myUsername`,_u);})()"
if OLD_MY_UN in content:
    content = content.replace(OLD_MY_UN, NEW_MY_UN, 1)
    print('OK: username cached in localStorage')
else:
    # Try alternative
    print('NOTE: my-username cache not applied (alternative location)')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
