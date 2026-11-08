#!/usr/bin/env python3
"""Patch v684 -> v685:
Fix slow mobile lightbox by:
1. Removing 'preload all at once' (splits mobile bandwidth 9-ways, worse than loading on demand)
2. Adding opacity fade on image swap (smooth cross-fade instead of blank flash while loading)
3. In _upd(): preload only the NEXT photo so bandwidth is focused where it's needed
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v684.js'
dst = '_deploy/assets/index-DUcNPOLc-v685.js'

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

# 1. Remove onLoad preload from thumbnail (was preloading all N photos at once)
for var, h in [('_pAtts', '320'), ('_cAtts', '240'), ('_tAtts', '320')]:
    old = ('{src:' + var + '[0].url'
           + ',onLoad:()=>{' + var + '.slice(1).forEach(_a=>{new Image().src=_a.url;})}'
           + ',style:{width:' + q + '100%' + q + ',height:' + h)
    new = '{src:' + var + '[0].url,style:{width:' + q + '100%' + q + ',height:' + h
    patch(old, new, f'{var} thumbnail: remove flood preload')

# 2. Remove forEach preload from lightbox open (was also preloading all at once)
for var in ['_pAtts', '_cAtts', '_tAtts']:
    old = ('document.body.appendChild(_ov);'
           + var + '.forEach(_a=>{new Image().src=_a.url;});}}),'+var+'.length>1&&')
    new = 'document.body.appendChild(_ov);}}),'+var+'.length>1&&'
    patch(old, new, f'{var} lightbox open: remove flood preload')

# 3. Add fade + focused next-photo preload inside _upd() for each lightbox
for var in ['_pAtts', '_cAtts', '_tAtts']:
    old = ('const _upd=()=>{_im.src='+var+'[_ci].url;'
           '_ctr.textContent=(_ci+1)+' + q + ' / ' + q + '+'+var+'.length;'
           '_mkDots();};')
    new = ('const _upd=()=>{'
           '_im.style.opacity=' + q + '0' + q + ';'
           '_im.src='+var+'[_ci].url;'
           '_im.onload=()=>{_im.style.opacity=' + q + '1' + q + '};'
           '_ctr.textContent=(_ci+1)+' + q + ' / ' + q + '+'+var+'.length;'
           '_mkDots();'
           'if(_ci+1<'+var+'.length)new Image().src='+var+'[_ci+1].url;'
           '};')
    patch(old, new, f'{var} _upd: fade + preload next photo')

# 4. Add transition:opacity 0.2s to _im style so fade is smooth
old_im = q + 'width:92vw;height:auto;max-height:${Math.round(_ih*0.88)}px;border-radius:10px;' + q
new_im = q + 'width:92vw;height:auto;max-height:${Math.round(_ih*0.88)}px;border-radius:10px;transition:opacity 0.2s;' + q
n = content.count(old_im)
if n == 0:
    errors.append('FAIL (_im transition): not found')
elif n > 3:
    errors.append('FAIL (_im transition): ' + str(n) + ' matches')
else:
    content = content.replace(old_im, new_im)
    print(f'OK ({n} replacements): _im: add opacity transition')

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
