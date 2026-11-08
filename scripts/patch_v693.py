#!/usr/bin/env python3
"""Patch v692 -> v693:
Fix ghost image strip on iOS Safari when viewing narrow portrait photos.
Root cause: transition:opacity 0.2s keeps the old (wider) image composited while
fading out. When a cached image fires onload instantly, both images are briefly
composited together — the old image's edge is visible beside the new narrow one.
Fix: disable transition before hiding (instant hide of old image), then re-enable
it only for the fade-in. Old image vanishes immediately, new one fades in smoothly.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v692.js'
dst = '_deploy/assets/index-DUcNPOLc-v693.js'

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

def patch_all(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append('FAIL (' + label + '): not found')
    else:
        content = content.replace(old, new)
        print(f'OK ({n}x): ' + label)

# 1. Remove transition from _im initial style — we'll re-add it per-update in onload
patch_all(
    q + 'max-width:92vw;max-height:${Math.round(_ih*0.88)}px;border-radius:10px;transition:opacity 0.2s;' + q,
    q + 'max-width:92vw;max-height:${Math.round(_ih*0.88)}px;border-radius:10px;' + q,
    '_im style: remove static transition'
)

# 2. In _upd(): disable transition before instant-hide, re-enable only for fade-in
for var in ['_pAtts', '_cAtts', '_tAtts']:
    old_upd = ('_im.style.opacity=' + q + '0' + q + ';_im.src=' + var + '[_ci].url;'
               '_im.onload=()=>{_im.style.opacity=' + q + '1' + q + '};')
    new_upd = ('_im.style.transition=' + q + 'none' + q + ';'
               '_im.style.opacity=' + q + '0' + q + ';'
               '_im.src=' + var + '[_ci].url;'
               '_im.onload=()=>{_im.style.transition=' + q + 'opacity 0.15s' + q + ';'
               '_im.style.opacity=' + q + '1' + q + '};')
    patch(old_upd, new_upd, f'{var} _upd: instant hide, smooth fade-in')

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
