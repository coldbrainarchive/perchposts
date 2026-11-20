#!/usr/bin/env python3
"""Patch v1267 -> v1268: signed-out visitors don't see Reply / React in the chirp drop-down (only Bird, and Find on replies).
An empty drop-down bar is hidden."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1267.js'
dst = '_deploy/assets/index-DUcNPOLc-v1268.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
SIGNED = "!!localStorage.getItem(`auth_token`)"
patch("children:[s&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1);if(!localStorage.getItem(`auth_token`))",
      "children:[s&&" + SIGNED + "&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1);if(!localStorage.getItem(`auth_token`))", 'Reply: signed in only')
patch("c&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:ev=>{ev.stopPropagation();_rxOpen(",
      "c&&" + SIGNED + "&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:ev=>{ev.stopPropagation();_rxOpen(", 'React: signed in only')
patch("body .lb-ic{", "body .chat-action-sheet:empty{display:none}body .lb-ic{", "css empty sheet")
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
