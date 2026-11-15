#!/usr/bin/env python3
"""Patch v1084 -> v1085: the bot check is hidden and runs when you press Sign Up.
Turnstile renders with execution 'execute' + appearance 'interaction-only': nothing shows on the form, Sign Up starts the
check, and the account is created as soon as it passes. The box only appears if Cloudflare wants someone to tick it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1084.js'
dst = '_deploy/assets/index-DUcNPOLc-v1085.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch("_tsI=(0,_.useRef)(null),", "_tsI=(0,_.useRef)(null),_tsW=(0,_.useRef)(null),", 'waiting ref')
patch("action:`signup`,theme:`dark`,size:`flexible`,callback:_setTsT,\"expired-callback\":()=>_setTsT(null),\"error-callback\":()=>_setTsT(null)})",
      "action:`signup`,theme:`dark`,size:`flexible`,execution:`execute`,appearance:`interaction-only`,"
      "callback:t=>{_setTsT(t);_tsW.current&&_tsW.current(t)},\"expired-callback\":()=>_setTsT(null),"
      "\"error-callback\":()=>{_setTsT(null);_tsW.current&&_tsW.current(null)},\"timeout-callback\":()=>{_setTsT(null);_tsW.current&&_tsW.current(null)}})",
      'run only on Sign Up, show only if needed')
patch("let e=_gu;if(!_tsT){E(!1);alert(`Please wait for the bot check to finish`);return}try{",
      "let e=_gu,_tk=_tsT||(_tsI.current!=null&&window.turnstile?await new Promise(res=>{_tsW.current=res;try{window.turnstile.execute(_tsI.current)}catch(err){res(null)}}):null);_tsW.current=null;"
      "if(!_tk){E(!1);_tsI.current!=null&&window.turnstile?.reset(_tsI.current);alert(`The bot check didn't go through. Please try again.`);return}try{",
      'Sign Up runs the check first')
patch("password:x,browser_id:Gn(),turnstile:_tsT,nest_device", "password:x,browser_id:Gn(),turnstile:_tk,nest_device", 'send the fresh token')
patch("C&&(0,L.jsx)(`div`,{ref:_tsR,style:{minHeight:65}})", "C&&(0,L.jsx)(`div`,{ref:_tsR})", 'no empty space when hidden')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
