#!/usr/bin/env python3
"""Patch v1017 -> v1018: sending from the chat only puts the cursor back in the message box if you were typing.
On iPhone, sending a photo with the keyboard closed used to pop the keyboard open mid-animation; the chat shifted
and resized under the flying photo, which shot off past the top and the chat went blank for a moment.
Text chirps keep the keyboard up as before (it was already open)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1017.js'
dst = '_deploy/assets/index-DUcNPOLc-v1018.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('onClick:()=>{if(!e||_cUL||(!f.trim()&&!_cA))return;let _txt=f',
      'onClick:()=>{if(!e||_cUL||(!f.trim()&&!_cA))return;const _wasF=!!(document.activeElement&&document.activeElement.classList&&document.activeElement.classList.contains(`chat-input`));let _txt=f', 'remember if typing')
patch('F(_txt,t,_ca2),document.querySelector(`.comments-shell .chat-input`)?.focus()',
      'F(_txt,t,_ca2),_wasF&&document.querySelector(`.comments-shell .chat-input`)?.focus()', 'only refocus if typing')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
