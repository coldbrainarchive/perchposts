#!/usr/bin/env python3
"""Patch v826 -> v827: after its two blinks the flash fades away slowly over 1.5s. The fade has to be a
second animation: a CSS transition doesn't run from an animated value when the class comes off, so the
glow just vanished. Pinned chirps skip the fade and go back to their steady glow.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v826.js'
dst = '_deploy/assets/index-DUcNPOLc-v827.js'

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

patch(t('e.style.transition=`box-shadow 0.3s`;e.classList.add(`chat-flash`);e._gt=setTimeout(()=>{e.classList.remove(`chat-flash`);e._gt=setTimeout(()=>{e.style.transition=``},350)},1500)}'),
      t('e.classList.add(`chat-flash`);e._gt=setTimeout(()=>e.classList.remove(`chat-flash`),2600)}'),
      'chirp timing')
patch(t('Q(!0),setTimeout(()=>Q(!1),1500)'), t('Q(!0),setTimeout(()=>Q(!1),2600)'), 'sign in timing')
patch(t('cursor:`pointer`,transition:`box-shadow 0.3s`},children:`Sign In`'), t('cursor:`pointer`},children:`Sign In`'), 'sign in transition')
patch('.chat-flash{animation:chat-flash .5s ease-in-out 2 forwards}',
      '.chat-flash{animation:chat-flash .5s ease-in-out 2,chat-flash-fade 1.5s ease-out 1s forwards}'
      '.chat-msg-body.chat-pinned.chat-flash{animation:chat-flash .5s ease-in-out 2}'
      '@keyframes chat-flash-fade{from{box-shadow:' + GLOW + '}to{box-shadow:0 0 0 0 rgba(192,132,252,0),0 0 0 rgba(192,132,252,0)}}',
      'fade')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
