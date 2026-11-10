#!/usr/bin/env python3
"""Patch v949 -> v950: tapping a pinned copy acts like any chirp (opens the menu). Its Find button jumps to
the original in the chat; on the original, Find (for replies) goes to the chirp it replied to, as before."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v949.js'
dst = '_deploy/assets/index-DUcNPOLc-v950.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('onClick:()=>{if(_pc&&d){y(!1);d(e.id);return}!p&&y(e=>!e)},', 'onClick:()=>!p&&y(e=>!e),', 'copy bubble opens menu')
patch('w&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1),d&&d(e.parent_comment_id)},children:`Find`})',
      '(_pc||w)&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1),d&&d(_pc?e.id:e.parent_comment_id)},children:`Find`})',
      'Find on pinned copy')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
