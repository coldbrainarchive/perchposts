#!/usr/bin/env python3
"""Patch v833 -> v834: deleted accounts show as Extinct Bird, with a grey bird, a grey name and no profile
to open. Your Nest gets Delete my account, which needs your password. A creator leaving a huddle now passes
it on, so that warning changes. The server does the name swap, these are only for how it looks.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v833.js'
dst = '_deploy/assets/index-DUcNPOLc-v834.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label, count=1):
    global content
    n = content.count(old)
    if n != count:
        errors.append('FAIL (' + label + '): expected ' + str(count) + ' matches, found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

def t(s):
    return s.replace('`', q)

X = '`Extinct Bird`'

patch(t('function Hn(e,t){let n=t||'), t('function Hn(e,t){if(t===' + X + ')return`#9ca3af`;let n=t||'), 'grey name')
patch(t('function Jn(e){if(!e)return null;if(e.username&&_jailed'),
      t('function Jn(e){if(!e)return null;if(e.username===' + X + ')return{e:`🐦`,f:`grayscale(1) opacity(.75)`,s:null};if(e.username&&_jailed'), 'grey bird')
patch(t("cursor:t?`pointer`:`default`},'data-gpb':t||null,onClick:r,"),
      t("cursor:t&&t!==" + X + "?`pointer`:`default`},'data-gpb':t&&t!==" + X + "?t:null,onClick:t===" + X + "?void 0:r,"), 'no profile from the name')
patch(t('e.username&&!_isMe?((0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{fetch(`${R}/user-stats?username='),
      t('e.username&&e.username!==' + X + '&&!_isMe?((0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{fetch(`${R}/user-stats?username='), 'no Bird button')

patch(t('`You created this huddle. Leaving will delete it for everyone — are you sure?`'),
      t('`You created this huddle. Leaving passes it to the next member, or ends it if nobody else is in it. Are you sure?`'), 'leave warning')

patch(t('[_tsT,_setTsT]=(0,_.useState)(null),'), t('[_tsT,_setTsT]=(0,_.useState)(null),[_dlO,_setDlO]=(0,_.useState)(!1),[_dlP,_setDlP]=(0,_.useState)(``),[_dlB,_setDlB]=(0,_.useState)(!1),'), 'delete state')
patch(t('let re=async()=>{if(u)try{let e=await fetch(`${R}/update-password`'),
      t('let _dlGo=async()=>{if(!_dlP||_dlB)return;_setDlB(!0);try{let _r=await fetch(`${R}/delete-account`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({password:_dlP})}),_j=await _r.json().catch(()=>({}));if(!_r.ok){alert(_j.error||`Could not delete your account`);return}[`auth_token`,`auth_user`,`_myUsername`].forEach(_k=>localStorage.removeItem(_k));window.location.href=`/`}catch(_e){alert(_e.message)}finally{_setDlB(!1)}},'
        '_dlUi=()=>t===`admin`?null:_dlO?(0,L.jsxs)(`div`,{className:`content-card`,style:{display:`flex`,flexDirection:`column`,gap:8,marginTop:4},children:[(0,L.jsx)(`div`,{style:{fontSize:13,color:`#f87171`,fontWeight:700},children:`Delete your account?`}),(0,L.jsx)(`div`,{style:{fontSize:12,color:`#94a3b8`,lineHeight:1.45},children:`This can\'t be undone. Your posts and chirps stay on the site, shown as Extinct Bird, and your username is retired forever. Delete anything you want gone first.`}),(0,L.jsx)(`input`,{type:`password`,placeholder:`Your password`,value:_dlP,onChange:_e=>_setDlP(_e.target.value),style:{padding:`9px 12px`,borderRadius:10,border:`1px solid #3f4756`,background:`#0f1117`,color:`#f8fafc`,fontSize:16,width:`100%`,boxSizing:`border-box`}}),(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8},children:[(0,L.jsx)(`button`,{type:`button`,onClick:_dlGo,disabled:!_dlP||_dlB,style:{flex:1,padding:`10px 0`,borderRadius:12,border:`none`,background:`#ef4444`,color:`#ffffff`,fontWeight:700,fontSize:14,cursor:`pointer`,opacity:!_dlP||_dlB?.5:1},children:_dlB?`…`:`Delete forever`}),(0,L.jsx)(`button`,{type:`button`,onClick:()=>{_setDlO(!1);_setDlP(``)},style:{padding:`10px 14px`,borderRadius:12,border:`none`,background:`#1f2937`,color:`#94a3b8`,fontWeight:700,fontSize:14,cursor:`pointer`},children:`Cancel`})]})]}):(0,L.jsx)(`button`,{type:`button`,onClick:()=>_setDlO(!0),style:{background:`none`,border:`none`,color:`#64748b`,fontSize:12,fontWeight:600,padding:`8px 0`,cursor:`pointer`},children:`Delete my account`});'
        'let re=async()=>{if(u)try{let e=await fetch(`${R}/update-password`'),
      'delete logic')
patch(t('children:`Leave`})]})]}),D&&(0,L.jsxs)(L.Fragment,{children:[_pwOpen?'),
      t('children:`Leave`})]}),_dlUi()]}),D&&(0,L.jsxs)(L.Fragment,{children:[_pwOpen?'), 'button for members')
patch(t('children:`Leave`})]}),(0,L.jsx)(I,{to:`/mod`,onClick:a,'),
      t('children:`Leave`})]}),_dlUi(),(0,L.jsx)(I,{to:`/mod`,onClick:a,'), 'button for mods')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
