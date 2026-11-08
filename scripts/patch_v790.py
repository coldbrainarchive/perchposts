#!/usr/bin/env python3
"""Patch v789 -> v790:
Tapping a flap notification opens the post without scrolling. Flaps have no comment attached, so
the link fell through to ?nc=<username>, which made the post page look for that person's comment.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v789.js'
dst = '_deploy/assets/index-DUcNPOLc-v790.js'

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

patch("(()=>{let _t=e.text||'';let _m=_t.match(",
      "(()=>{if(e.type===" + q + "vote" + q + ")return" + q + q + ";let _t=e.text||'';let _m=_t.match(",
      'flap notification links straight to the post')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print('Paren delta: ' + str(p_delta) + ', Brace delta: ' + str(b_delta))
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
