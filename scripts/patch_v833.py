#!/usr/bin/env python3
"""Patch v832 -> v833: a Turnstile bot check on sign up. The widget only loads in Sign Up mode, so login
and browsing don't pay for it. Tokens are single use, so any failed sign up resets the widget.
The sitekey is public. The secret is TURNSTILE_SECRET on the worker.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v832.js'
dst = '_deploy/assets/index-DUcNPOLc-v833.js'
SITEKEY = '0x4AAAAAAF2NzjZf3SAW03_C'

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

RESET = '_tsI.current!=null&&window.turnstile?.reset(_tsI.current);_setTsT(null);'

patch(t('[C,w]=(0,_.useState)(!1),[T,E]=(0,_.useState)(!1),[_wc,_swc]'),
      t('[C,w]=(0,_.useState)(!1),_tsR=(0,_.useRef)(null),_tsI=(0,_.useRef)(null),[_tsT,_setTsT]=(0,_.useState)(null),[T,E]=(0,_.useState)(!1),[_wc,_swc]'),
      'state')
patch(t('(0,_.useEffect)(()=>{(async()=>{let t=new URLSearchParams({browser_id:k});D&&e?t.set(`mod_user_id`,e.id):r&&t.set(`username`,r);let n=await fetch(`${R}/user-stats?${t}`'),
      t('(0,_.useEffect)(()=>{if(!C||e)return;let _off=!1,_go=()=>{if(_off||!_tsR.current||!window.turnstile)return;_tsI.current=window.turnstile.render(_tsR.current,{sitekey:`' + SITEKEY + '`,action:`signup`,theme:`dark`,size:`flexible`,callback:_setTsT,"expired-callback":()=>_setTsT(null),"error-callback":()=>_setTsT(null)})};if(window.turnstile)_go();else{let _s=document.querySelector(`script[data-ts]`);if(!_s){_s=document.createElement(`script`);_s.src=`https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit`;_s.dataset.ts=`1`;document.head.appendChild(_s)}_s.addEventListener(`load`,_go)}return()=>{_off=!0;_setTsT(null);if(_tsI.current!=null&&window.turnstile)window.turnstile.remove(_tsI.current);_tsI.current=null}},[C,e]),(0,_.useEffect)(()=>{(async()=>{let t=new URLSearchParams({browser_id:k});D&&e?t.set(`mod_user_id`,e.id):r&&t.set(`username`,r);let n=await fetch(`${R}/user-stats?${t}`'),
      'load widget')
patch(t('if(E(!0),C){let e=_gu;try{let t=await fetch(`${R}/register`'),
      t('if(E(!0),C){let e=_gu;if(!_tsT){E(!1);alert(`Please wait for the bot check to finish`);return}try{let t=await fetch(`${R}/register`'),
      'wait for the check')
patch(t('body:JSON.stringify({username:e,password:x,browser_id:Gn()})}),n=await t.json();if(E(!1),!t.ok){alert(n.error||`Registration failed`);return}'),
      t('body:JSON.stringify({username:e,password:x,browser_id:Gn(),turnstile:_tsT})}),n=await t.json();if(E(!1),!t.ok){' + RESET + 'alert(n.error||`Registration failed`);return}'),
      'send token')
patch(t('s(n.user,n.user.role||`user`,e),a()}catch(e){E(!1),alert(e.message)}}else try{'),
      t('s(n.user,n.user.role||`user`,e),a()}catch(e){E(!1);' + RESET + 'alert(e.message)}}else try{'),
      'reset on network failure')
patch(t('(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8},children:[(0,L.jsx)(`button`,{onClick:ie,disabled:T,'),
      t('C&&(0,L.jsx)(`div`,{ref:_tsR,style:{minHeight:65}}),(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8},children:[(0,L.jsx)(`button`,{onClick:ie,disabled:T,'),
      'widget box')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
