#!/usr/bin/env python3
"""Patch v681 -> v682:
Fix iOS Safari address bar issue: vh units are calculated from the FULL layout
viewport height (toolbar hidden), so when the address bar is visible the actual
visible height is smaller. Portrait photos constrained by max-height:88vh then
produce a width smaller than 92vw (black bars on sides).
Fix: capture window.innerHeight at lightbox open time and use px values instead
of vh units for both the overlay height and the image max-height.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v681.js'
dst = '_deploy/assets/index-DUcNPOLc-v682.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append('FAIL (' + label + '): not found')
    elif n > 3:
        errors.append('FAIL (' + label + '): ' + str(n) + ' matches')
    else:
        content = content.replace(old, new)
        print('OK (' + str(n) + ' replacements): ' + label)

# Replace all three lightbox setups: inject _ih=window.innerHeight and use px
old_block = ('let _ci=0;const _ov=document.createElement(' + q + 'div' + q + ');'
             '_ov.style.cssText=' + q + 'position:fixed;inset:0;background:rgba(0,0,0,0.93);'
             'z-index:9999;display:flex;align-items:center;justify-content:center;' + q + ';'
             'const _im=document.createElement(' + q + 'img' + q + ');'
             '_im.style.cssText=' + q + 'width:92vw;height:auto;max-height:88vh;border-radius:10px;' + q)

new_block = ('let _ci=0;const _ih=window.innerHeight;const _ov=document.createElement(' + q + 'div' + q + ');'
             '_ov.style.cssText=`position:fixed;top:0;left:0;width:100%;height:${_ih}px;background:rgba(0,0,0,0.93);'
             'z-index:9999;display:flex;align-items:center;justify-content:center;`;'
             'const _im=document.createElement(' + q + 'img' + q + ');'
             '_im.style.cssText=`width:92vw;height:auto;max-height:${Math.round(_ih*0.88)}px;border-radius:10px;`')

patch(old_block, new_block, 'lightbox: use window.innerHeight instead of vh to avoid address-bar squish')

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
