#!/usr/bin/env python3
"""Patch v995 -> v996: huddle cards include you. Your circle goes last (after the birds who chirped since you
last read and everyone else) and never lights up."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v995.js'
dst = '_deploy/assets/index-DUcNPOLc-v996.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('const others=_hxAll(e,mm).filter(m=>m.username.toLowerCase()!==me);\n others.sort(',
      'const _all=_hxAll(e,mm),others=_all.filter(m=>m.username.toLowerCase()!==me),_self=_all.find(m=>m.username.toLowerCase()===me);\n others.sort(', 'keep self')
patch('const shown=others.slice(0,7),extra=others.length-shown.length;',
      'const shown=others.slice(0,_self?6:7);_self&&shown.push(_self);const extra=others.length+(_self?1:0)-shown.length;', 'self last')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
