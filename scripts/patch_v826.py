#!/usr/bin/env python3
"""Patch v825 -> v826: one purple flash everywhere. It's the dim and brighten pulse from v824, blinking
twice, used by notifications, Find, huddle system messages and the Sign In button. It holds the glow
briefly then fades (forwards plus the transition), except on pinned chirps, which keep their glow.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v825.js'
dst = '_deploy/assets/index-DUcNPOLc-v826.js'

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

GLOW = '0 0 0 4px rgba(192,132,252,0.6),0 0 20px rgba(192,132,252,0.8)'

patch(t('function _glow(e){e=e.closest(`.chat-msg-body`)||e;if(e.classList.contains(`chat-pinned`)){e.classList.remove(`chat-flash`);void e.offsetWidth;e.classList.add(`chat-flash`);setTimeout(()=>e.classList.remove(`chat-flash`),1600);return}e.style.transition=`box-shadow 0.3s`;e.style.boxShadow=`' + GLOW + '`;setTimeout(()=>{e.style.boxShadow=``;setTimeout(()=>{e.style.transition=``},350)},1500)}'),
      t('function _glow(e){e=e.closest(`.chat-msg-body`)||e;clearTimeout(e._gt);e.classList.remove(`chat-flash`);void e.offsetWidth;e.style.transition=`box-shadow 0.3s`;e.classList.add(`chat-flash`);e._gt=setTimeout(()=>{e.classList.remove(`chat-flash`);e._gt=setTimeout(()=>{e.style.transition=``},350)},1500)}'),
      'one flash')
patch('.chat-msg-body.chat-pinned.chat-flash{animation:chat-pin-flash .7s linear 2}'
      '@keyframes chat-pin-flash{0%,45%{box-shadow:0 0 0 0 rgba(192,132,252,0),0 0 0 rgba(192,132,252,0)}'
      '55%,100%{box-shadow:' + GLOW + '}}',
      '.chat-flash{animation:chat-flash .5s ease-in-out 2 forwards}'
      '@keyframes chat-flash{0%,100%{box-shadow:' + GLOW + '}'
      '35%{box-shadow:0 0 0 1px rgba(192,132,252,0.15),0 0 0 rgba(192,132,252,0)}'
      '70%{box-shadow:0 0 0 6px rgba(216,180,254,1),0 0 34px rgba(192,132,252,1)}}', 'flash style')
patch(t('className:`app-chip`,style:{background:`#c084fc`,color:`#14081d`,borderColor:`#a855f7`,cursor:`pointer`,transition:`box-shadow 0.3s`,boxShadow:Z?`' + GLOW + '`:``},children:`Sign In`'),
      t('className:`app-chip`+(Z?` chat-flash`:``),style:{background:`#c084fc`,color:`#14081d`,borderColor:`#a855f7`,cursor:`pointer`,transition:`box-shadow 0.3s`},children:`Sign In`'),
      'sign in')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
