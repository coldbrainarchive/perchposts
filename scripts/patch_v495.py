#!/usr/bin/env python3
"""Patch v494 -> v495:
Add Remove button + picker to huddle post page.
- Button shown only to OP, admin, or mod (between Invite and Leave)
- Picker shows existing huddle members; OP cannot remove mods/admins
- Fetches new /remove-from-huddle endpoint
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v494.js'
dst = '_deploy/assets/index-DUcNPOLc-v495.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add Remove state variables after _wpInvP ───────────────────────────────
OLD_STATE = ',[_wpInvP,_setWpInvP]=(0,_.useState)(null),_wpInvTimer=(0,_.useRef)(null)'
NEW_STATE  = (',[_wpInvP,_setWpInvP]=(0,_.useState)(null)'
              ',[_wpRemOpen,_setWpRemOpen]=(0,_.useState)(!1)'
              ',[_wpRemP,_setWpRemP]=(0,_.useState)(null)'
              ',_wpInvTimer=(0,_.useRef)(null)')
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: Remove state vars added')
else:
    errors.append('FAIL: state vars')

# ── 2. Insert Remove button between Invite and Leave ─────────────────────────
REMOVE_BTN = (
    '(()=>{const _rUn=localStorage.getItem(`_myUsername`)||null;'
    'const _rIsOp=c?.is_huddle&&_rUn&&c.username&&_rUn.toLowerCase()===c.username.toLowerCase();'
    'const _rIsAdm=_rUn&&_adminUsers.has(_rUn.toLowerCase());'
    'const _rIsMod=(()=>{try{const _rr=JSON.parse(localStorage.getItem(`auth_user`)||`{}`);'
    'return _rr.role===`mod`||_rr.role===`admin`;}catch(_e){return !1;}})();'
    'return c?.is_huddle&&(_rIsOp||_rIsAdm||_rIsMod)?'
    '(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
    'style:_wpRemOpen?{borderColor:`#f87171`,background:`rgba(248,113,113,0.1)`}:{},'
    'onClick:()=>{_setWpRemOpen(v=>!v);_setWpRemP(null);},'
    'children:_wpRemOpen?`✕ Cancel`:`Remove`}):null;})()'
)
OLD_BETWEEN = ('children:_wpInvOpen?`✕ Cancel`:`Invite`}),'
               'c?.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
               'onClick:()=>{const _un3=')
NEW_BETWEEN  = ('children:_wpInvOpen?`✕ Cancel`:`Invite`}),'
                + REMOVE_BTN + ','
                'c?.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,'
                'onClick:()=>{const _un3=')
if OLD_BETWEEN in content:
    content = content.replace(OLD_BETWEEN, NEW_BETWEEN, 1)
    print('OK: Remove button inserted')
else:
    errors.append('FAIL: button insertion')

# ── 3. Insert Remove picker after invite picker ───────────────────────────────
REMOVE_PICKER = (
    '_wpRemOpen&&(0,L.jsxs)(`div`,{style:{marginTop:8,padding:`10px 14px`,'
    'background:`#1a1d27`,borderRadius:12,border:`1px solid #374151`},children:['
    '_wpRemP&&(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8,alignItems:`center`,marginBottom:8},'
    'children:[(0,L.jsx)(Xn,{record:{username:_wpRemP.u,browser_id:null,is_admin:_wpRemP.r===`admin`},'
    'name:_wpRemP.u,color:Hn(null,_wpRemP.u)}),'
    '(0,L.jsx)(`button`,{type:`button`,style:{flex:1,padding:`8px`,borderRadius:8,border:`none`,'
    'background:`#ef4444`,color:`#fff`,fontWeight:700,fontSize:12,cursor:`pointer`,'
    'touchAction:`manipulation`},'
    'onClick:()=>{const _rUn2=localStorage.getItem(`_myUsername`)||null;'
    'fetch(`${R}/remove-from-huddle`,{method:`POST`,'
    'headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:c.id,remove_username:_wpRemP.u,'
    'req_username:_rUn2,browser_id:Gn()})}).then(async _rr=>{const _rj=await _rr.json().catch(()=>({}));'
    'if(!_rr.ok){alert(_rj.error||`Could not remove`);return;}'
    'if(_rj.post)l(Cr(_rj.post));'
    'const _rsc=_rj.systemComment||{id:`__sys_${Date.now()}`,'
    'content:`👢 ${_wpRemP.u} was removed from the huddle`,'
    'username:`__system__`,created_at:new Date().toISOString(),'
    'browser_id:null,parent_comment_id:null,is_mod:0};'
    'd(e=>[...e,_rsc]);_setWpRemOpen(!1);_setWpRemP(null);'
    '}).catch(err=>alert(`Remove failed: `+err.message));'
    '},children:`Remove `+_wpRemP.u})]}),\n'
    '(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:6},'
    'children:(()=>{const _rUn2=localStorage.getItem(`_myUsername`)||null;'
    'const _rIsOp2=_rUn2&&c.username&&_rUn2.toLowerCase()===c.username.toLowerCase();'
    'const _rIsAdm2=_rUn2&&_adminUsers.has(_rUn2.toLowerCase());'
    'const _rIsMod2=(()=>{try{const _rr2=JSON.parse(localStorage.getItem(`auth_user`)||`{}`);'
    'return _rr2.role===`mod`||_rr2.role===`admin`;}catch(_e){return !1;}})();'
    'return JSON.parse(c.huddle_members||`[]`).map(_m=>{const _ci=(_m||``).lastIndexOf(`:`);'
    'if(_ci>0){const _r=_m.slice(_ci+1);if(_r===`admin`||_r===`mod`)return{u:_m.slice(0,_ci),r:_r};}'
    'return{u:_m||``,r:null};}).filter(_m=>{if(!_m.u||_m.u.toLowerCase()===(_rUn2||``).toLowerCase())return !1;'
    'if(_rIsOp2&&!_rIsAdm2&&!_rIsMod2&&(_m.r===`admin`||_m.r===`mod`))return !1;return !0;})'
    '.map(_m=>(0,L.jsx)(`button`,{type:`button`,style:{background:`none`,border:`none`,padding:0,cursor:`pointer`,'
    'outline:_wpRemP?.u===_m.u?`2px solid #f87171`:`none`,borderRadius:999},'
    'onClick:()=>_setWpRemP(_wpRemP?.u===_m.u?null:_m),'
    'children:(0,L.jsx)(Xn,{record:{username:_m.u,browser_id:null,is_admin:_m.r===`admin`},'
    'name:_m.u,color:Hn(null,_m.u)})},_m.u));})()'
    '})]}),'
)

OLD_AFTER_PICKER = ('Invite `+_wpInvP.username})]}),(0,L.jsxs)(`div`,{className:`feed-post-actions`')
NEW_AFTER_PICKER  = ('Invite `+_wpInvP.username})]}),\n' + REMOVE_PICKER +
                     '(0,L.jsxs)(`div`,{className:`feed-post-actions`')
if OLD_AFTER_PICKER in content:
    content = content.replace(OLD_AFTER_PICKER, NEW_AFTER_PICKER, 1)
    print('OK: Remove picker inserted')
else:
    errors.append('FAIL: picker insertion')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
