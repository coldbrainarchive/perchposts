#!/usr/bin/env python3
"""Patch v572 -> v573: iOS canvas won't read video pixels unless video is actively playing.
Switch from loadeddata+timeout to play()+ontimeupdate capture. iOS allows play() on muted
videos without user gesture. ontimeupdate fires when a real frame is available."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v572.js'
dst = '_deploy/assets/index-DUcNPOLc-v573.js'

content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append(f'FAIL ({label}): not found')
    elif n > 1:
        errors.append(f'FAIL ({label}): {n} matches (not unique)')
    else:
        content = content.replace(old, new)
        print(f'OK: {label}')

# Shared pattern: play() + ontimeupdate so iOS has a live frame to draw
COMMENT_NEW = (
    '_isVid?new Promise(_res=>{'
      'let _pv=document.createElement(`video`),'
          '_pu=URL.createObjectURL(_ff),'
          '_done=!1;'
      'const _cleanup=()=>{try{document.body.removeChild(_pv)}catch{}};'
      'const _cap=()=>{'
        'if(_done)return;_done=!0;'
        '_pv.pause();'
        'let _pc=document.createElement(`canvas`);'
        '_pc.width=_pv.videoWidth||320;'
        '_pc.height=_pv.videoHeight||240;'
        '_pc.getContext(`2d`).drawImage(_pv,0,0);'
        '_cleanup();'
        '_pc.toBlob(_b=>{URL.revokeObjectURL(_pu);_res(_b)},`image/jpeg`,0.7)'
      '};'
      '_pv.muted=!0;_pv.playsInline=!0;'
      '_pv.setAttribute(`playsinline`,``);'
      '_pv.preload=`auto`;'
      '_pv.style.cssText=`position:fixed;opacity:0;pointer-events:none;width:1px;height:1px;top:-9999px`;'
      '_pv.ontimeupdate=_cap;'
      '_pv.onerror=()=>{_cleanup();URL.revokeObjectURL(_pu);_res(null)};'
      '_pv.src=_pu;'
      'document.body.appendChild(_pv);'
      '_pv.play().catch(()=>{_cleanup();URL.revokeObjectURL(_pu);_res(null)});'
      'setTimeout(()=>{if(!_done)_cap()},4000)'
    '}):Promise.resolve(null)'
)

NEWPOST_NEW = (
    'let _vp2=null;if(t===`video`){const _pb2=await new Promise(_res=>{'
      'let _pv2=document.createElement(`video`),'
          '_pu3=URL.createObjectURL(e),'
          '_done2=!1;'
      'const _cl2=()=>{try{document.body.removeChild(_pv2)}catch{}};'
      'const _cap2=()=>{'
        'if(_done2)return;_done2=!0;'
        '_pv2.pause();'
        'let _pc2=document.createElement(`canvas`);'
        '_pc2.width=_pv2.videoWidth||320;'
        '_pc2.height=_pv2.videoHeight||240;'
        '_pc2.getContext(`2d`).drawImage(_pv2,0,0);'
        '_cl2();'
        '_pc2.toBlob(_b=>{URL.revokeObjectURL(_pu3);_res(_b)},`image/jpeg`,0.7)'
      '};'
      '_pv2.muted=!0;_pv2.playsInline=!0;'
      '_pv2.setAttribute(`playsinline`,``);'
      '_pv2.preload=`auto`;'
      '_pv2.style.cssText=`position:fixed;opacity:0;pointer-events:none;width:1px;height:1px;top:-9999px`;'
      '_pv2.ontimeupdate=_cap2;'
      '_pv2.onerror=()=>{_cl2();URL.revokeObjectURL(_pu3);_res(null)};'
      '_pv2.src=_pu3;'
      'document.body.appendChild(_pv2);'
      '_pv2.play().catch(()=>{_cl2();URL.revokeObjectURL(_pu3);_res(null)});'
      'setTimeout(()=>{if(!_done2)_cap2()},4000)'
    '});'
)

patch(
    '_isVid?new Promise(_res=>{let _pv=document.createElement(`video`),_pu=URL.createObjectURL(_ff),_done=!1;const _cleanup=()=>{try{document.body.removeChild(_pv)}catch{}};const _cap=()=>{if(_done)return;_done=!0;let _pc=document.createElement(`canvas`);_pc.width=_pv.videoWidth||320;_pc.height=_pv.videoHeight||240;_pc.getContext(`2d`).drawImage(_pv,0,0);_cleanup();_pc.toBlob(_b=>{URL.revokeObjectURL(_pu);_res(_b)},`image/jpeg`,0.7)};_pv.muted=!0;_pv.playsInline=!0;_pv.preload=`auto`;_pv.setAttribute(`playsinline`,``);_pv.style.cssText=`position:fixed;opacity:0;pointer-events:none;width:1px;height:1px;top:-9999px`;_pv.onloadeddata=()=>setTimeout(_cap,200);_pv.onseeked=_cap;_pv.onerror=()=>{_cleanup();URL.revokeObjectURL(_pu);_res(null)};_pv.src=_pu;document.body.appendChild(_pv);_pv.load()}):Promise.resolve(null)',
    COMMENT_NEW,
    'comment poster: play()+ontimeupdate for iOS'
)

patch(
    'let _vp2=null;if(t===`video`){const _pb2=await new Promise(_res=>{let _pv2=document.createElement(`video`),_pu3=URL.createObjectURL(e),_done2=!1;const _cl2=()=>{try{document.body.removeChild(_pv2)}catch{}};const _cap2=()=>{if(_done2)return;_done2=!0;let _pc2=document.createElement(`canvas`);_pc2.width=_pv2.videoWidth||320;_pc2.height=_pv2.videoHeight||240;_pc2.getContext(`2d`).drawImage(_pv2,0,0);_cl2();_pc2.toBlob(_b=>{URL.revokeObjectURL(_pu3);_res(_b)},`image/jpeg`,0.7)};_pv2.muted=!0;_pv2.playsInline=!0;_pv2.preload=`auto`;_pv2.setAttribute(`playsinline`,``);_pv2.style.cssText=`position:fixed;opacity:0;pointer-events:none;width:1px;height:1px;top:-9999px`;_pv2.onloadeddata=()=>setTimeout(_cap2,200);_pv2.onseeked=_cap2;_pv2.onerror=()=>{_cl2();URL.revokeObjectURL(_pu3);_res(null)};_pv2.src=_pu3;document.body.appendChild(_pv2);_pv2.load()});',
    NEWPOST_NEW,
    'new post poster: play()+ontimeupdate for iOS'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print(f'Paren delta: {p_delta}, Brace delta: {b_delta}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
