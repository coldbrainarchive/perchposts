#!/usr/bin/env python3
"""Patch v627 -> v628:
Custom video controls bar (no native control overlay):
- Progress scrubber (timeline)
- Mute button
- Fullscreen button
All at the bottom of the video, always visible after poster is dismissed.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v627.js'
dst = '_deploy/assets/index-DUcNPOLc-v628.js'

content = open(src, encoding='utf-8').read()
errors = []
q = chr(0x60)

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

# 1. Add onTimeUpdate to video element (updates scrubber as video plays)
patch(
    'if(v.paused){v.play();}else{v.pause();}}}),' ,
    ('if(v.paused){v.play();}else{v.pause();}},onTimeUpdate:e=>{'
     + 'const _inp=e.currentTarget.parentElement.querySelector(' + q + 'input[type=range]' + q + ');'
     + 'if(_inp&&e.currentTarget.duration)_inp.value=(e.currentTarget.currentTime/e.currentTarget.duration)*100;'
     + '}}),'),
    'add onTimeUpdate to sync scrubber'
)

# 2. Insert controls bar before video wrapper closing ]})
controls_bar = (
    ',(0,L.jsxs)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
    + ',bottom:0,left:0,right:0,padding:' + q + '6px 10px' + q
    + ',background:' + q + 'linear-gradient(transparent,rgba(0,0,0,0.7))' + q
    + ',display:' + q + 'flex' + q + ',alignItems:' + q + 'center' + q
    + ',gap:8,borderRadius:' + q + '0 0 10px 10px' + q
    + ',boxSizing:' + q + 'border-box' + q + ',pointerEvents:' + q + 'auto' + q + '},'
    + 'onClick:e=>e.stopPropagation(),'
    + 'children:['
    # Mute button
    + '(0,L.jsx)(' + q + 'button' + q + ',{type:' + q + 'button' + q
    + ',onClick:e=>{e.stopPropagation();const v=e.currentTarget.parentElement.parentElement.querySelector(' + q + 'video' + q + ');v.muted=!v.muted;e.currentTarget.textContent=v.muted?' + q + '🔇' + q + ':' + q + '🔊' + q + ';}'
    + ',style:{background:' + q + 'none' + q + ',border:' + q + 'none' + q + ',color:' + q + 'white' + q + ',cursor:' + q + 'pointer' + q + ',padding:0,fontSize:16,lineHeight:1,flexShrink:0},'
    + 'children:' + q + '🔊' + q + '}),'
    # Scrubber
    + '(0,L.jsx)(' + q + 'input' + q + ',{type:' + q + 'range' + q
    + ',min:0,max:100,defaultValue:0,step:0.1,'
    + 'style:{flex:1,cursor:' + q + 'pointer' + q + ',accentColor:' + q + 'white' + q + ',height:3},'
    + 'onInput:e=>{e.stopPropagation();const v=e.currentTarget.parentElement.parentElement.querySelector(' + q + 'video' + q + ');if(v.duration)v.currentTime=(e.target.value/100)*v.duration;}}),'
    # Fullscreen button
    + '(0,L.jsx)(' + q + 'button' + q + ',{type:' + q + 'button' + q
    + ',onClick:e=>{e.stopPropagation();const v=e.currentTarget.parentElement.parentElement.querySelector(' + q + 'video' + q + ');if(v.requestFullscreen)v.requestFullscreen();else if(v.webkitEnterFullscreen)v.webkitEnterFullscreen();}'
    + ',style:{background:' + q + 'none' + q + ',border:' + q + 'none' + q + ',color:' + q + 'white' + q + ',cursor:' + q + 'pointer' + q + ',padding:0,fontSize:16,lineHeight:1,flexShrink:0},'
    + 'children:' + q + '⛶' + q + '})'
    + ']})'
)

patch(
    '5,2 16,9 5,16' + q + '})})})})]})}return t===' + q + 'link' + q,
    '5,2 16,9 5,16' + q + '})})})})' + controls_bar + ']})}return t===' + q + 'link' + q,
    'add controls bar to video wrapper'
)

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
