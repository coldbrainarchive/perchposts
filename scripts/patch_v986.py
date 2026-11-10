#!/usr/bin/env python3
"""Patch v985 -> v986: tapping a pinned chirp in the post page preview opens the chat at that pin in the
pinned area at the top (not at the original chirp further down the timeline)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v985.js'
dst = '_deploy/assets/index-DUcNPOLc-v986.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('_fid.current=_tg.closest(`.pin-more-note`)?`__pins__`:_tg.closest(`.chat-msg`)?.dataset.commentId||_tg.closest(`.chat-msg`)?.dataset.pinOf||null',
      '_fid.current=_tg.closest(`.pin-more-note`)?`__pins__`:_tg.closest(`.chat-msg`)?.dataset.pinOf?`__pin__`+_tg.closest(`.chat-msg`).dataset.pinOf:_tg.closest(`.chat-msg`)?.dataset.commentId||null',
      'preview pin tap target')
patch('let _ft=0,_go=()=>{let _pp=_id===`__pins__`,_n=_pp?[..._w.querySelectorAll(`.chat-section-title`)].find(x=>x.textContent.includes(`Pinned`)):_w.querySelector(`[data-comment-id="${_id}"]`);if(!_n){if(!_pp&&!_ft)',
      'let _ft=0,_go=()=>{let _pp=_id===`__pins__`,_pc=String(_id).startsWith(`__pin__`),_pi=_pc?CSS.escape(_id.slice(7)):``,_n=_pp?[..._w.querySelectorAll(`.chat-section-title`)].find(x=>x.textContent.includes(`Pinned`)):_pc?(_w.querySelector(`.chat-msg[data-pin-of="${_pi}"]`)||_w.querySelector(`.chat-msg[data-comment-id="${_pi}"]`)):_w.querySelector(`[data-comment-id="${_id}"]`);if(!_n){if(!_pp&&!_pc&&!_ft)',
      'scroll to the pin copy')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
