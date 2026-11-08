#!/usr/bin/env python3
"""Patch v647 -> v648:
Move v.setAttribute('playsinline') and v.controls=false to run immediately on
fullscreen exit (outside the timeout) so the native fullscreen UI doesn't flash
on the inline video. Pause + play bubble still happen after 300ms.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v647.js'
dst = '_deploy/assets/index-DUcNPOLc-v648.js'

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

patch(
    ('v._exitingFs=!0;setTimeout(()=>{v._exitingFs=!1;v.setAttribute(' + q + 'playsinline' + q + ',' + q + q + ');'
     + 'v.controls=!1;if(!v.paused)v.pause();'
     + 'const _pb=v.nextElementSibling&&v.nextElementSibling.nextElementSibling;'
     + 'if(_pb&&v.paused){_pb.style.display=' + q + 'flex' + q + ';_pb.style.pointerEvents=' + q + 'auto' + q + ';'
     + '_pb.onclick=()=>{_pb.style.display=' + q + 'none' + q + ';_pb.style.pointerEvents=' + q + 'none' + q + ';v.play();};}},300)'),
    ('v._exitingFs=!0;v.setAttribute(' + q + 'playsinline' + q + ',' + q + q + ');v.controls=!1;'
     + 'setTimeout(()=>{v._exitingFs=!1;if(!v.paused)v.pause();'
     + 'const _pb=v.nextElementSibling&&v.nextElementSibling.nextElementSibling;'
     + 'if(_pb&&v.paused){_pb.style.display=' + q + 'flex' + q + ';_pb.style.pointerEvents=' + q + 'auto' + q + ';'
     + '_pb.onclick=()=>{_pb.style.display=' + q + 'none' + q + ';_pb.style.pointerEvents=' + q + 'none' + q + ';v.play();};}},300)'),
    'apply playsinline+controls=false immediately, delay only pause+bubble'
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
