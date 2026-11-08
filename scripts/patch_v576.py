#!/usr/bin/env python3
"""Patch v575 -> v576:
- Video thumbnail: add centered play button circle over img overlay; hide both on tap
- Image: add small expand icon badge in bottom-right corner; replace full image block as one unit
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v575.js'
dst = '_deploy/assets/index-DUcNPOLc-v576.js'

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

# ── 1. Video: add centered play button overlay; hide both img + play btn on tap ──
patch(
    '_vpost&&(0,L.jsx)(`img`,{src:_vpost,alt:``,style:{position:`absolute`,inset:0,width:`100%`,height:`100%`,objectFit:`cover`,borderRadius:10,cursor:`pointer`,display:`block`},onClick:_pe=>{_pe.currentTarget.style.display=`none`;_pe.currentTarget.previousElementSibling.play()}})',
    '_vpost&&(0,L.jsx)(`img`,{src:_vpost,alt:``,style:{position:`absolute`,inset:0,width:`100%`,height:`100%`,objectFit:`cover`,borderRadius:10,cursor:`pointer`,display:`block`},onClick:_pe=>{_pe.currentTarget.style.display=`none`;_pe.currentTarget.nextElementSibling.style.display=`none`;_pe.currentTarget.previousElementSibling.play()}}),_vpost&&(0,L.jsx)(`div`,{style:{position:`absolute`,inset:0,display:`flex`,alignItems:`center`,justifyContent:`center`,pointerEvents:`none`,borderRadius:10},children:(0,L.jsx)(`div`,{style:{width:48,height:48,borderRadius:999,background:`rgba(0,0,0,0.52)`,backdropFilter:`blur(4px)`,display:`flex`,alignItems:`center`,justifyContent:`center`},children:(0,L.jsx)(`svg`,{width:18,height:18,viewBox:`0 0 18 18`,fill:`white`,children:(0,L.jsx)(`polygon`,{points:`5,2 16,9 5,16`})})})})',
    'add play button over video thumbnail'
)

# ── 2. Image: full block replacement — add expand icon badge in corner ──
patch(
    'if(t===`image`)return(0,L.jsx)(`div`,{style:{marginTop:10},children:(0,L.jsx)(`img`,{src:n,alt:``,style:{maxWidth:`100%`,borderRadius:10,display:`block`,maxHeight:400,objectFit:`cover`,cursor:`zoom-in`},onError:e=>{e.target.style.display=`none`},onClick:()=>{let _ov=document.createElement(`div`);_ov.style.cssText=`position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:zoom-out`;let _im=document.createElement(`img`);_im.src=n;_im.style.cssText=`max-width:92vw;max-height:92vh;border-radius:10px;object-fit:contain`;_ov.appendChild(_im);_ov.onclick=()=>{document.body.removeChild(_ov);document.body.style.overflow=``};document.body.style.overflow=`hidden`;document.body.appendChild(_ov)}})});if(t===`video`)',
    'if(t===`image`)return(0,L.jsxs)(`div`,{style:{position:`relative`,marginTop:10},children:[(0,L.jsx)(`img`,{src:n,alt:``,style:{maxWidth:`100%`,borderRadius:10,display:`block`,maxHeight:400,objectFit:`cover`,cursor:`zoom-in`},onError:e=>{e.target.style.display=`none`},onClick:()=>{let _ov=document.createElement(`div`);_ov.style.cssText=`position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:zoom-out`;let _im=document.createElement(`img`);_im.src=n;_im.style.cssText=`max-width:92vw;max-height:92vh;border-radius:10px;object-fit:contain`;_ov.appendChild(_im);_ov.onclick=()=>{document.body.removeChild(_ov);document.body.style.overflow=``};document.body.style.overflow=`hidden`;document.body.appendChild(_ov)}}),(0,L.jsx)(`div`,{style:{position:`absolute`,bottom:6,right:6,background:`rgba(0,0,0,0.45)`,backdropFilter:`blur(4px)`,borderRadius:6,padding:`2px 5px`,fontSize:11,color:`#fff`,pointerEvents:`none`,lineHeight:1},children:`⤢`})]});if(t===`video`)',
    'add expand icon badge on image'
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
