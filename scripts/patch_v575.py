#!/usr/bin/env python3
"""Patch v574 -> v575: Replace poster attribute with img overlay.
poster attribute causes ghosting on pause/resume — uncontrollable browser behaviour.
Instead render a separate <img> overlay that hides on tap and starts the video."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v574.js'
dst = '_deploy/assets/index-DUcNPOLc-v575.js'

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

# Replace poster attr + onPlay with a sibling <img> overlay
patch(
    'return(0,L.jsx)(`div`,{style:{marginTop:10},children:(0,L.jsx)(`video`,{src:n,controls:!0,playsInline:!0,preload:`metadata`,...(_vpost?{poster:_vpost}:{}),onPlay:_vpe=>{_vpe.target.removeAttribute(`poster`)},style:{maxWidth:`100%`,borderRadius:10,maxHeight:400}})})}return t===`link`',
    'return(0,L.jsxs)(`div`,{style:{position:`relative`,marginTop:10},children:[(0,L.jsx)(`video`,{src:n,controls:!0,playsInline:!0,preload:`metadata`,style:{maxWidth:`100%`,borderRadius:10,maxHeight:400,display:`block`}}),_vpost&&(0,L.jsx)(`img`,{src:_vpost,alt:``,style:{position:`absolute`,inset:0,width:`100%`,height:`100%`,objectFit:`cover`,borderRadius:10,cursor:`pointer`,display:`block`},onClick:_pe=>{_pe.currentTarget.style.display=`none`;_pe.currentTarget.previousElementSibling.play()}})]})}return t===`link`',
    'replace poster attr with img overlay — no more ghosting'
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
