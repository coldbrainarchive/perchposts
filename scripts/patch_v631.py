#!/usr/bin/env python3
"""Patch v629 -> v631:
1. Fullscreen button top-left; native controls in fullscreen
2. Play bubble reappears on pause and is tappable to resume
Fix: insert onPlay/onPause BEFORE props-close } not after it.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v629.js'
dst = '_deploy/assets/index-DUcNPOLc-v631.js'

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

# In the video jsx: onClick ends with }} (else-body + fn-body),
# then } closes props, then ) closes jsx, then ,
# Target: ...v.pause();}}}, = else-body} + fn-body} + props-close} + ),
# Replace: insert onPlay,onPause before props-close }
on_play  = ('onPlay:e=>{const pb=e.currentTarget.nextElementSibling&&e.currentTarget.nextElementSibling.nextElementSibling;'
            + 'if(pb)pb.style.display=' + q + 'none' + q + '}')
on_pause = ('onPause:e=>{const pb=e.currentTarget.nextElementSibling&&e.currentTarget.nextElementSibling.nextElementSibling;'
            + 'if(pb){pb.style.display=' + q + 'flex' + q + ';pb.style.pointerEvents=' + q + 'auto' + q + ';'
            + 'pb.onclick=()=>{pb.style.display=' + q + 'none' + q + ';pb.style.pointerEvents=' + q + 'none' + q + ';e.currentTarget.play();}}}')

# Target ends with }}}), where:
# first two }} = else-body + fn-body (part of onClick value)
# third } = props object close
# ) = jsx call close, , = separator
# New: keep first }}, add new props, then close props }),
patch(
    'if(v.paused){v.play();}else{v.pause();}}}),',
    'if(v.paused){v.play();}else{v.pause();}},' + on_play + ',' + on_pause + '}),',
    'add onPlay/onPause for play bubble'
)

# 2. Remove pointerEvents:none from play bubble outer div
patch(
    'pointerEvents:' + q + 'none' + q + ',borderRadius:10},children:',
    'borderRadius:10},children:',
    'remove pointerEvents:none from play bubble'
)

# 3. Add fullscreen button top-left
fs_btn = (
    ',(0,L.jsx)(' + q + 'button' + q + ',{type:' + q + 'button' + q
    + ',onClick:e=>{e.stopPropagation();const v=e.currentTarget.parentElement.querySelector(' + q + 'video' + q + ');'
    + 'if(v.webkitEnterFullscreen){v.webkitEnterFullscreen();}'
    + 'else if(v.requestFullscreen){'
    + 'v.controls=!0;v.requestFullscreen();'
    + 'document.addEventListener(' + q + 'fullscreenchange' + q + ',()=>{if(!document.fullscreenElement)v.controls=!1;},{once:!0});}}'
    + ',style:{position:' + q + 'absolute' + q + ',top:8,left:8,zIndex:10,'
    + 'background:' + q + 'rgba(0,0,0,0.55)' + q + ',border:' + q + 'none' + q + ','
    + 'color:' + q + 'white' + q + ',borderRadius:6,padding:' + q + '5px 7px' + q + ','
    + 'cursor:' + q + 'pointer' + q + ',fontSize:15,lineHeight:1,backdropFilter:' + q + 'blur(4px)' + q + '},'
    + 'children:' + q + '⛶' + q + '})'
)

patch(
    '5,2 16,9 5,16' + q + '})})})})]})}return',
    '5,2 16,9 5,16' + q + '})})})})' + fs_btn + ']})}return',
    'add fullscreen button top-left'
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
