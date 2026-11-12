#!/usr/bin/env python3
"""Patch v1034 -> v1035: while the full-screen link view is open, the phone's top bar (time, battery) uses the same
black as the view; it goes back to normal when you close it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1034.js'
dst = '_deploy/assets/index-DUcNPOLc-v1035.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('const body=document.body.style,prevOv=body.overflow;let gone=!1,pendingPost=null;',
      'const body=document.body.style,prevOv=body.overflow;let gone=!1,pendingPost=null;'
      'const tcm=document.querySelector(`meta[name="theme-color"]`),prevTc=tcm&&tcm.getAttribute(`content`);tcm&&tcm.setAttribute(`content`,`#0b0c10`);',
      'top bar goes black')
patch('setTimeout(()=>{ov.remove();body.overflow=prevOv;const el=cur&&',
      'tcm&&prevTc&&tcm.setAttribute(`content`,prevTc);setTimeout(()=>{ov.remove();body.overflow=prevOv;const el=cur&&',
      'and back on close')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
