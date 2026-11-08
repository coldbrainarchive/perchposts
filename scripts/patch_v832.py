#!/usr/bin/env python3
"""Patch v831 -> v832, for accounts-only:
Uploads and the notification count send the login token, which the server now needs. Signed out, the chat's
+ button and Reply flash Sign In, the new post page asks you to sign in, and the notification count isn't
requested. If the login has expired the site signs out, so people see Sign In instead of failed actions.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v831.js'
dst = '_deploy/assets/index-DUcNPOLc-v832.js'

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

GATE = 'if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}'

patch(t('fetch(`${R}/upload`,{method:`POST`,'), t('fetch(`${R}/upload`,{method:`POST`,headers:er(),'), 'uploads send the token', 6)
patch(t('onClick:()=>_cMR.current?.click(),disabled:_cUL||m'), t('onClick:()=>{' + GATE + '_cMR.current?.click()},disabled:_cUL||m'), 'chat upload button')
patch(t('onClick:()=>{y(!1),s&&s(e)},children:`Reply`'), t('onClick:()=>{y(!1);' + GATE + 's&&s(e)},children:`Reply`'), 'reply button')
patch(t('try{let e=await fetch(`${R}/notif-count?${o}`);'),
      t('if(!localStorage.getItem(`auth_token`))return;try{let e=await fetch(`${R}/notif-count?${o}`,{headers:er()});if(e.status===401){localStorage.removeItem(`auth_token`);localStorage.removeItem(`auth_user`);localStorage.removeItem(`_myUsername`);location.reload();return}'), 'notification count')
patch(t('(0,L.jsx)(Ot,{path:`/new`,element:(0,L.jsx)(Ur,{user:e,userRole:n,memberUsername:o})})'),
      t('(0,L.jsx)(Ot,{path:`/new`,element:e?(0,L.jsx)(Ur,{user:e,userRole:n,memberUsername:o}):(0,L.jsx)(_Si,{})})'), 'new post needs an account')
patch(t('\nfunction _Bd(){'),
      t('\nfunction _Si(){(0,_.useEffect)(()=>{let _t=setTimeout(()=>window.dispatchEvent(new CustomEvent(`like-no-auth`)),150);return()=>clearTimeout(_t)},[]);return(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,alignItems:`center`,padding:`64px 24px`,textAlign:`center`,gap:8},children:[(0,L.jsx)(`div`,{style:{fontSize:17,fontWeight:700,color:`#f1f5f9`},children:`Sign in to post`}),(0,L.jsx)(`div`,{style:{fontSize:13,color:`#64748b`},children:`You need an account to post, chirp and upload`})]})}\nfunction _Bd(){'),
      'sign in page')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
