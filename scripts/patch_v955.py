#!/usr/bin/env python3
"""Patch v954 -> v955: tapping "📌 +N more pinned" in the post preview opens the chat scrolled to the pinned
area (top aligned), where the extra (older) pins are."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v954.js'
dst = '_deploy/assets/index-DUcNPOLc-v955.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('_fid.current=_tg.closest(`.chat-msg`)?.dataset.commentId||',
      '_fid.current=_tg.closest(`.pin-more-note`)?`__pins__`:_tg.closest(`.chat-msg`)?.dataset.commentId||', 'note click target')
patch('let _go=()=>{let _n=_w.querySelector(`[data-comment-id="${_id}"]`);if(!_n)return;let _a=_n.getBoundingClientRect(),_b=_w.getBoundingClientRect();_w.scrollTop+=_a.top-_b.top-Math.max(0,(_w.clientHeight-_a.height)/2)}',
      'let _go=()=>{let _pp=_id===`__pins__`,_n=_pp?[..._w.querySelectorAll(`.chat-section-title`)].find(x=>x.textContent.includes(`Pinned`)):_w.querySelector(`[data-comment-id="${_id}"]`);if(!_n)return;let _a=_n.getBoundingClientRect(),_b=_w.getBoundingClientRect();_w.scrollTop+=_a.top-_b.top-(_pp?6:Math.max(0,(_w.clientHeight-_a.height)/2))}',
      'scroll to pinned area')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
