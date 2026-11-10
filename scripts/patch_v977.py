#!/usr/bin/env python3
"""Patch v976 -> v977: Find / reply jumps to a chirp taller than the chat show it from its top (8px below the
top edge) instead of centring it, which put the middle of a long chirp on screen. Short chirps still centre."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v976.js'
dst = '_deploy/assets/index-DUcNPOLc-v977.js'
c = open(src, encoding='utf-8').read()
old = 't.scrollTop+=_a.top-_w.top-(t.clientHeight-_a.height)/2;'
n = c.count(old)
if n != 2: print('FAIL', n); sys.exit(1)
c = c.replace(old, 't.scrollTop+=_a.top-_w.top-Math.max(8,(t.clientHeight-_a.height)/2);')
old2 = '_w.scrollTop+=_a.top-_b.top-(_pp?6:Math.max(0,(_w.clientHeight-_a.height)/2))'
if c.count(old2) != 1: print('FAIL2'); sys.exit(1)
c = c.replace(old2, '_w.scrollTop+=_a.top-_b.top-(_pp?6:Math.max(8,(_w.clientHeight-_a.height)/2))')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst, '(replaced', n, '+1)')
