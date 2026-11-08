#!/usr/bin/env python3
"""Patch v687 -> v688:
Wrap-around lightbox navigation: reaching the last photo and going forward loops
to photo 1; going backward from photo 1 loops to the last photo.
Applied to zone clicks and touch swipe in all 3 lightboxes.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v687.js'
dst = '_deploy/assets/index-DUcNPOLc-v688.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append('FAIL (' + label + '): not found')
    elif n > 1:
        errors.append('FAIL (' + label + '): ' + str(n) + ' matches')
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

rz_style = ('const _rz=document.createElement(' + q + 'div' + q + ');'
            '_rz.style.cssText=' + q + 'position:absolute;right:0;top:0;width:40%;height:100%;cursor:e-resize;' + q + ';'
            '_rz.onclick=_e=>{_e.stopPropagation();')

for var in ['_pAtts', '_cAtts', '_tAtts']:
    # Patch lz onclick (backward) + rz onclick (forward) together for unique context
    old = (f'if(_ci>0)' + '{_ci--;_upd();}};' + rz_style +
           f'if(_ci<{var}.length-1)' + '{_ci++;_upd();}}')
    new = (f'_ci=(_ci-1+{var}.length)%{var}.length;_upd();}};' + rz_style +
           f'_ci=(_ci+1)%{var}.length;_upd();}}')
    patch(old, new, f'{var} lz+rz onclick: wrap both directions')

    # Patch swipe handler
    old_sw = (f'if(_dx<0&&_ci<{var}.length-1)' + '{_ci++;_upd();}else if(_dx>0&&_ci>0){_ci--;_upd();}}')
    new_sw = (f'if(_dx<0)' + '{' + f'_ci=(_ci+1)%{var}.length;_upd();' + '}'
              + f'else if(_dx>0)' + '{' + f'_ci=(_ci-1+{var}.length)%{var}.length;_upd();' + '}}')
    patch(old_sw, new_sw, f'{var} swipe: wrap both directions')

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
