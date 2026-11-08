#!/usr/bin/env python3
"""Patch v648 -> v652:
Fix listener accumulation: each fullscreen session adds fullscreenchange +
webkitendfullscreen listeners, but if only one fires (swipe fires webkitendfullscreen,
not fullscreenchange), the other stays attached. Next session adds more.
After N sessions, N stale _onFsExit calls fire simultaneously.

Fix: store a _fsCln cleanup fn on the video element. Before adding new listeners,
call _fsCln to remove any stale ones from a previous session.
Also call _fsCln at the start of _onFsExit so whichever event fires first
cleans up the other listener.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v648.js'
dst = '_deploy/assets/index-DUcNPOLc-v652.js'

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

# 1. Before defining _onFsExit, clean up any stale listeners from a previous session.
#    Inside _onFsExit, call _fsCln immediately so whichever event fires first
#    removes the other listener (preventing double-fire).
patch(
    'const _onFsExit=()=>{',
    'if(v._fsCln)v._fsCln();const _onFsExit=()=>{if(v._fsCln)v._fsCln();',
    'add _fsCln guard before and inside _onFsExit'
)

# 2. Replace the bare addEventListener calls with named handler refs + store _fsCln
patch(
    ('document.addEventListener(' + q + 'fullscreenchange' + q + ',()=>{if(!document.fullscreenElement)_onFsExit();},{once:!0});'
     + 'v.addEventListener(' + q + 'webkitendfullscreen' + q + ',_onFsExit,{once:!0});'),
    ('const _fsDL=()=>{if(!document.fullscreenElement)_onFsExit();};'
     + 'document.addEventListener(' + q + 'fullscreenchange' + q + ',_fsDL,{once:!0});'
     + 'v.addEventListener(' + q + 'webkitendfullscreen' + q + ',_onFsExit,{once:!0});'
     + 'v._fsCln=()=>{document.removeEventListener(' + q + 'fullscreenchange' + q + ',_fsDL);'
     + 'v.removeEventListener(' + q + 'webkitendfullscreen' + q + ',_onFsExit);v._fsCln=null;};'),
    'store named handler refs and _fsCln cleanup on video element'
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
