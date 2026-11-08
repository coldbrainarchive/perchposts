#!/usr/bin/env python3
"""Patch v239 -> v240: user stats card + DM inbox replacing notifications/posts tabs."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v239.js'
dst = '_deploy/assets/index-DUcNPOLc-v240.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add _UserCard component before Vr ─────────────────────────────────────
OLD_VR_START = 'function Vr(){let[e,t]=(0,_.us'
NEW_VR_START = (
    'function _UserCard({username:_un,onMessage:_om}){'
    'const[_s,_ss]=(0,_.useState)(null);'
    '(0,_.useEffect)(()=>{'
    'if(!_un)return;'
    'fetch(`${R}/user-stats?username=${encodeURIComponent(_un)}`)'
    '.then(r=>r.json()).then(d=>_ss(d)).catch(()=>{});'
    '},[_un]);'
    'if(!_s)return null;'
    'const _wc=_s.worm_count||0;'
    'const _rk=_RANKS.find(r=>_wc>=r.min&&_wc<=r.max);'
    'const _me=Qn()?.username;'
    'const _meta=(_rk?`${_rk.e} ${_rk.n} \xb7 `:``)+`\U0001fab1 ${_wc}`+(_s.joined_at?` \xb7 Joined ${Un(_s.joined_at)}`:``);\n'
    'return(0,L.jsxs)(`div`,{style:{padding:`12px 18px`,background:`#0f1117`,borderBottom:`1px solid #2e303a`,display:`flex`,alignItems:`center`,gap:12},'
    'children:[(0,L.jsxs)(`div`,{style:{flex:1},'
    'children:[(0,L.jsx)(`div`,{style:{color:`#f8fafc`,fontWeight:700,fontSize:15},children:_un}),'
    '(0,L.jsx)(`div`,{style:{color:`#64748b`,fontSize:12,marginTop:3},children:_meta})]}),'
    '_me&&_me!==_un&&(0,L.jsx)(`button`,{onClick:()=>_om(_un),'
    'style:{padding:`6px 16px`,borderRadius:10,border:`none`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:12,cursor:`pointer`},'
    'children:`\U0001f4ac Message`})]});}'
    '\nfunction Vr(){let[e,t]=(0,_.us'
)
if OLD_VR_START in content:
    content = content.replace(OLD_VR_START, NEW_VR_START, 1)
    print('OK: _UserCard component added')
else:
    errors.append('FAIL: Vr start not found')

# ── 2. Insert _UserCard in Vr render when username filter active ──────────────
OLD_VR_RENDER = '(0,L.jsx)(Lr,{}),(0,L.jsxs)(`main`,{className:`home-feed`'
NEW_VR_RENDER = (
    '(0,L.jsx)(Lr,{}),'
    'p&&(0,L.jsx)(_UserCard,{username:p,onMessage:(_u)=>window.dispatchEvent(new CustomEvent(`open-dm`,{detail:_u}))}),'
    '(0,L.jsxs)(`main`,{className:`home-feed`'
)
if OLD_VR_RENDER in content:
    content = content.replace(OLD_VR_RENDER, NEW_VR_RENDER, 1)
    print('OK: _UserCard inserted in Vr')
else:
    errors.append('FAIL: Vr render anchor not found')

# ── 3. Add _dmInit state in qr ───────────────────────────────────────────────
OLD_QR_STATE = '[u,d]=(0,_.useState)(!1),[f,p]=(0,_.useState)(0)'
NEW_QR_STATE = '[u,d]=(0,_.useState)(!1),[_dmInit,_setDmInit]=(0,_.useState)(null),[f,p]=(0,_.useState)(0)'
if OLD_QR_STATE in content:
    content = content.replace(OLD_QR_STATE, NEW_QR_STATE, 1)
    print('OK: _dmInit state added to qr')
else:
    errors.append('FAIL: qr state anchor not found')

# ── 4. Add open-dm event listener in qr (alongside like-no-auth) ─────────────
OLD_LISTENER = (
    'let e=()=>{Q(!0),setTimeout(()=>Q(!1),1500)};'
    'return window.addEventListener(`like-no-auth`,e),()=>window.removeEventListener(`like-no-auth`,e)'
)
NEW_LISTENER = (
    'let e=()=>{Q(!0),setTimeout(()=>Q(!1),1500)};'
    'let _odm=ev=>{_setDmInit(ev.detail);d(!0)};'
    'return window.addEventListener(`like-no-auth`,e),window.addEventListener(`open-dm`,_odm),'
    '()=>{window.removeEventListener(`like-no-auth`,e);window.removeEventListener(`open-dm`,_odm)}'
)
if OLD_LISTENER in content:
    content = content.replace(OLD_LISTENER, NEW_LISTENER, 1)
    print('OK: open-dm event listener added in qr')
else:
    errors.append('FAIL: like-no-auth listener not found')

# ── 5. Pass initDmUser to Kr ─────────────────────────────────────────────────
OLD_KR_CALL = '(0,L.jsx)(Kr,{user:e,userRole:n,modName:i,browseUsername:o,lastMemberUsername:c,onClose:()=>d(!1)'
NEW_KR_CALL = '(0,L.jsx)(Kr,{user:e,userRole:n,modName:i,browseUsername:o,lastMemberUsername:c,initDmUser:_dmInit,onClose:()=>{d(!1);_setDmInit(null)}'
if OLD_KR_CALL in content:
    content = content.replace(OLD_KR_CALL, NEW_KR_CALL, 1)
    print('OK: initDmUser passed to Kr')
else:
    errors.append('FAIL: Kr call in qr not found')

# ── 6. Add initDmUser prop to Kr signature ───────────────────────────────────
OLD_KR_SIG = 'function Kr({user:e,userRole:t,modName:n,browseUsername:r,lastMemberUsername:i,onClose:a,onLeave:o,onLogin:s})'
NEW_KR_SIG = 'function Kr({user:e,userRole:t,modName:n,browseUsername:r,lastMemberUsername:i,onClose:a,onLeave:o,onLogin:s,initDmUser:_initDm=null})'
if OLD_KR_SIG in content:
    content = content.replace(OLD_KR_SIG, NEW_KR_SIG, 1)
    print('OK: initDmUser added to Kr signature')
else:
    errors.append('FAIL: Kr signature not found')

# ── 7. Add DM state in Kr ────────────────────────────────────────────────────
OLD_KR_STATE = '[g,v]=(0,_.useState)(!0),[_gu,_su]=(0,_.useState)(``),[y,b]='
NEW_KR_STATE = (
    '[g,v]=(0,_.useState)(!0),'
    '[_dmConvs,_setDmConvs]=(0,_.useState)([]),'
    '[_dmThread,_setDmThread]=(0,_.useState)(null),'
    '[_dmMsgs,_setDmMsgs]=(0,_.useState)([]),'
    '[_dmInput,_setDmInput]=(0,_.useState)(``),'
    '[_dmSending,_setDmSending]=(0,_.useState)(!1),'
    '[_gu,_su]=(0,_.useState)(``),[y,b]='
)
if OLD_KR_STATE in content:
    content = content.replace(OLD_KR_STATE, NEW_KR_STATE, 1)
    print('OK: DM state added to Kr')
else:
    errors.append('FAIL: Kr state anchor not found')

# ── 8. Replace notifications fetch effect with inbox fetch + thread fetch ─────
OLD_NOTIF_EFF = (
    'c===`notifications`&&(v(!0),(async()=>{let t=new URLSearchParams({browser_id:k});'
    'D&&e?t.set(`mod_user_id`,e.id):r&&t.set(`username`,r),i&&t.set(`exclude_username`,i);'
    'let n=await fetch(`${R}/notifications?${t}`,{headers:er()});'
    'h((n.ok?await n.json():{}).notifs||[]),v(!1)})())},[c,e,r])'
)
NEW_NOTIF_EFF = (
    'c===`inbox`&&!_dmThread&&(async()=>{'
    'let _r=await fetch(`${R}/dm-inbox`,{headers:er()});'
    '_setDmConvs((_r.ok?await _r.json():{}).conversations||[])})()},'
    '[c,_dmThread,e]);'
    '(0,_.useEffect)(()=>{'
    'if(!_dmThread||!e)return;'
    '(async()=>{'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[])})()},'
    '[_dmThread,e]);'
    '(0,_.useEffect)(()=>{'
    'if(!_initDm)return;l(`inbox`);_setDmThread(_initDm);},'
    '[_initDm])'
)
if OLD_NOTIF_EFF in content:
    content = content.replace(OLD_NOTIF_EFF, NEW_NOTIF_EFF, 1)
    print('OK: notifications effect replaced with inbox+thread effects')
else:
    errors.append('FAIL: notifications effect not found')

# ── 9. Change Kr tabs array ───────────────────────────────────────────────────
OLD_TABS = 'M=e?[{id:`notifications`,label:`Notifications`},{id:`posts`,label:`Posts`},{id:`account`,label:`Your Nest`}]:[{id:`account`,label:`Your Nest`}]'
NEW_TABS = 'M=e?[{id:`inbox`,label:`Inbox`},{id:`account`,label:`Your Nest`}]:[{id:`account`,label:`Your Nest`}]'
if OLD_TABS in content:
    content = content.replace(OLD_TABS, NEW_TABS, 1)
    print('OK: Kr tabs changed to inbox')
else:
    errors.append('FAIL: Kr tabs not found')

# ── 10. Change Kr initial tab state ──────────────────────────────────────────
OLD_TAB_INIT = 'let[c,l]=(0,_.useState)(e?`notifications`:`account`)'
NEW_TAB_INIT = 'let[c,l]=(0,_.useState)(e?`inbox`:`account`)'
if OLD_TAB_INIT in content:
    content = content.replace(OLD_TAB_INIT, NEW_TAB_INIT, 1)
    print('OK: Kr initial tab set to inbox')
else:
    errors.append('FAIL: Kr initial tab state not found')

# ── 11. Replace notifications render with inbox render ───────────────────────
OLD_NOTIF_RENDER = (
    'c===`notifications`&&(0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`},'
    'children:g?(0,L.jsx)(`div`,{style:{padding:32,color:`#64748b`,textAlign:`center`,fontSize:14},children:`Loading…`}):'
    'j.length===0?(0,L.jsxs)(`div`,{style:{padding:`48px 20px`,color:`#64748b`,textAlign:`center`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600},children:`No notifications yet`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:12,marginTop:4},children:`Activity on your posts and comments shows up here`})]})'
    ':j.map(e=>{let t=!!e.time&&e.time>ee.current;'
)
# Check if this exact string exists
if OLD_NOTIF_RENDER in content:
    print('notif render found - will replace')
else:
    print('notif render NOT found - trying shorter anchor')
    OLD_NOTIF_RENDER = None

if OLD_NOTIF_RENDER:
    # Find the full extent - ends at c===`posts`
    idx = content.find(OLD_NOTIF_RENDER)
    end_idx = content.find('c===`posts`&&', idx)
    full_old = content[idx:end_idx]
    NEW_INBOX_RENDER = (
        'c===`inbox`&&(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,flex:1},'
        'children:[_dmThread?'
        # Thread view
        '(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,flex:1},'
        'children:['
        '(0,L.jsxs)(`div`,{style:{padding:`10px 16px`,borderBottom:`1px solid #2e303a`,display:`flex`,alignItems:`center`,gap:10},'
        'children:[(0,L.jsx)(`button`,{onClick:()=>{_setDmThread(null);_setDmMsgs([]);},'
        'style:{background:`none`,border:`none`,color:`#94a3b8`,fontSize:18,cursor:`pointer`,padding:0,lineHeight:1},'
        'children:`←`}),'
        '(0,L.jsx)(`span`,{style:{color:`#f8fafc`,fontWeight:700,fontSize:14},children:_dmThread})]},'
        '(0,L.jsx)(`div`,{style:{flex:1,overflowY:`auto`,display:`flex`,flexDirection:`column`,gap:2,padding:`8px 0`},'
        'children:_dmMsgs.length===0?'
        '(0,L.jsx)(`div`,{style:{padding:32,color:`#64748b`,textAlign:`center`,fontSize:13},children:`No messages yet`}):'
        '_dmMsgs.map((_msg,_mi)=>{'
        'const _mine=_msg.from_username===(Qn()?.username||``);'
        'return(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,alignItems:_mine?`flex-end`:`flex-start`,padding:`2px 14px`},'
        'children:['
        '(0,L.jsx)(`div`,{style:{background:_mine?`#3b1f6e`:`#1e2530`,color:`#dbe4ee`,borderRadius:14,padding:`7px 12px`,fontSize:13,maxWidth:`78%`,wordBreak:`break-word`},children:_msg.content}),'
        '(0,L.jsx)(`div`,{style:{color:`#475569`,fontSize:10,marginTop:2},children:Un(_msg.created_at)})'
        ']},_mi)'
        '})}),'
        '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8,padding:`10px 14px`,borderTop:`1px solid #2e303a`},'
        'children:[(0,L.jsx)(`input`,{value:_dmInput,onChange:ev=>_setDmInput(ev.target.value),'
        'onKeyDown:async ev=>{if(ev.key===`Enter`&&!ev.shiftKey&&_dmInput.trim()&&!_dmSending){'
        'ev.preventDefault();_setDmSending(!0);'
        'await fetch(`${R}/send-dm`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
        'body:JSON.stringify({to_username:_dmThread,content:_dmInput.trim()})});'
        '_setDmInput(``);'
        'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
        '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);'
        '_setDmSending(!1);}},'
        'placeholder:`Message ${_dmThread}…`,'
        'style:{flex:1,background:`#1e2530`,border:`1px solid #374151`,borderRadius:10,padding:`8px 12px`,color:`#f8fafc`,fontSize:13,outline:`none`}}),'
        '(0,L.jsx)(`button`,{disabled:_dmSending||!_dmInput.trim(),'
        'onClick:async()=>{if(!_dmInput.trim()||_dmSending)return;_setDmSending(!0);'
        'await fetch(`${R}/send-dm`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
        'body:JSON.stringify({to_username:_dmThread,content:_dmInput.trim()})});'
        '_setDmInput(``);'
        'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
        '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);'
        '_setDmSending(!1);},'
        'style:{padding:`8px 14px`,borderRadius:10,border:`none`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:13,cursor:`pointer`,opacity:_dmSending?0.6:1},'
        'children:`Send`})]})]})'
        # Conversation list
        ':(0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`},'
        'children:_dmConvs.length===0?'
        '(0,L.jsxs)(`div`,{style:{padding:`48px 20px`,color:`#64748b`,textAlign:`center`},'
        'children:[(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600},children:`No messages yet`}),'
        '(0,L.jsx)(`div`,{style:{fontSize:12,marginTop:4},children:`Search for a user and tap Message to start a chat`})]})'
        ':_dmConvs.map((_cv,_ci)=>'
        '(0,L.jsxs)(`div`,{onClick:()=>{_setDmThread(_cv.contact);_setDmMsgs([]);},'
        'style:{display:`flex`,alignItems:`center`,gap:12,padding:`12px 18px`,'
        'borderBottom:`1px solid #1a1c23`,cursor:`pointer`,background:`transparent`},'
        'children:[(0,L.jsxs)(`div`,{style:{flex:1,minWidth:0},'
        'children:[(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:6},'
        'children:[(0,L.jsx)(`span`,{style:{color:`#f8fafc`,fontWeight:700,fontSize:13},children:_cv.contact}),'
        '_cv.unread>0&&(0,L.jsx)(`span`,{style:{background:`#c084fc`,color:`#14081d`,borderRadius:999,fontSize:10,fontWeight:700,padding:`1px 6px`},children:_cv.unread})]}),'
        '(0,L.jsx)(`div`,{style:{color:`#475569`,fontSize:12,marginTop:2,overflow:`hidden`,textOverflow:`ellipsis`,whiteSpace:`nowrap`},children:_cv.last_content||``})]}),'
        '(0,L.jsx)(`span`,{style:{color:`#374151`,fontSize:11},children:Un(_cv.last_at)})]},_ci)'
        ')})]}),'
    )
    content = content[:idx] + NEW_INBOX_RENDER + content[end_idx:]
    print('OK: inbox render added')

# ── 12. Remove posts render (tab is gone, clean up) ───────────────────────────
OLD_POSTS_RENDER = (
    'c===`posts`&&(0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`},'
    'children:f.length===0?(0,L.jsxs)(`div`,{style:{padding:`48px 20px`,color:`#64748b`,textAlign:`center`},'
    'children:[(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600},children:`No posts yet`})]})'
    ':f.map((e,t)=>(0,L.jsxs)(I,{to:`/post/${e.id}`,onClick:a,'
    'style:{display:`block`,padding:`12px 18px`,borderBottom:t<f.length-1?`1px solid #1a1c23`:`none`,textDecoration:`none`},'
    'onMouseEnter:e=>e.currentTarget.style.background=`#1f2028`,'
    'onMouseLeave:e=>e.currentTarget.style.background=`transparent`,'
    'children:[(0,L.jsx)(`div`,{style:{color:`#e2e8f0`,fontSize:14,fontWeight:600,marginBottom:3},children:e.title}),'
    '(0,L.jsxs)(`div`,{style:{color:`#475569`,fontSize:12},'
    'children:[e.board?`${e.board} \xb7 `:``,Un(e.created_at)]})]},e.id))}),'
)
if OLD_POSTS_RENDER in content:
    content = content.replace(OLD_POSTS_RENDER, '', 1)
    print('OK: posts render removed')
else:
    errors.append('FAIL: posts render not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
