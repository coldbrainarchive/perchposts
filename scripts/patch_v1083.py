#!/usr/bin/env python3
"""Patch v1082 -> v1083: the sign-up nest.
"tap to generate username" is replaced by a nest of 5 eggs from the server (/nest). Three taps crack an egg, and the
hatching tap picks that bird. Fresh eggs come only every 15 minutes, and sign-up only accepts a name from your own nest
(the worker checks nest_device). The bird kit now also exports ready and eye (eyelids for blinking)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1082.js'
dst = '_deploy/assets/index-DUcNPOLc-v1083.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# 1. bird kit (birds/*.js), now also exporting ready and eye. From v1083 on the kit ends with the new tail.
head, tail = 'const _ppKit=(()=>{const BASE={};let __bk;\n', 'return{get,sub,tagCol};})();\n'
new_tail = 'return{get,sub,tagCol,ready,eye};})();\n'
i, j = c.index(head), c.index(tail) + len(tail)
kit = ''.join(open('birds/' + f, encoding='utf-8').read() + '\n' for f in ['seg.js', 'birdkit.js', 'runtime.js'])
c = c[:i] + head + kit + new_tail + c[j:]; print('OK: bird kit updated')

# 2. the nest (birds/nest.js) and its React wrapper, next to the bird component
NEST_HEAD, NEST_TAIL = '/*ppnest*/', '/*/ppnest*/'
nest = open('birds/nest.js', encoding='utf-8').read()
wrapper = ("function _PNest({api,onPick}){const r=(0,_.useRef)(null),p=(0,_.useRef)(onPick);p.current=onPick;"
           "(0,_.useEffect)(()=>_ppNest(r.current,api,n=>p.current(n)),[api]);return(0,L.jsx)(`div`,{ref:r})}")
patch("function _PB({n,c,z,k,fb}){", NEST_HEAD + nest + "\n" + wrapper + NEST_TAIL + "function _PB({n,c,z,k,fb}){", 'nest code')

# 3. the sign-up form: the nest instead of the random-name box
start = c.index("C?(0,L.jsxs)(`div`,{onClick:function(){_su((function(){var _a=[")
end_marker = "children:_gu||`tap to generate username`})]})"
end = c.index(end_marker, start) + len(end_marker)
assert c.count(end_marker) == 1 and end - start < 12000, end - start
c = c[:start] + "C?(0,L.jsx)(_PNest,{api:R,onPick:_su})" + c[end:]; print('OK: nest in the sign-up form')

# 4. sign-up sends this browser's nest id, and forgets the nest once the account exists
patch("body:JSON.stringify({username:e,password:x,browser_id:Gn(),turnstile:_tsT})}),n=await t.json();",
      "body:JSON.stringify({username:e,password:x,browser_id:Gn(),turnstile:_tsT,nest_device:_ppNestDev()})}),n=await t.json();", 'register sends nest id')
patch("localStorage.setItem(`auth_token`,n.token),_authPing(),",
      "_ppNestDone(),localStorage.setItem(`auth_token`,n.token),_authPing(),", 'forget nest after sign-up')

open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
