#!/usr/bin/env python3
"""Patch v1083 -> v1084: the bot check (Turnstile) moves to the bottom of the sign-up form, under the buttons."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1083.js'
dst = '_deploy/assets/index-DUcNPOLc-v1084.js'
c = open(src, encoding='utf-8').read()
TS = "C&&(0,L.jsx)(`div`,{ref:_tsR,style:{minHeight:65}}),"
BTN_END = "children:C?`Log In instead`:`Sign Up`})]})"
if c.count(TS) != 1 or c.count(BTN_END) != 1: print('FAIL', c.count(TS), c.count(BTN_END)); sys.exit(1)
i = c.index(TS); j = c.index(BTN_END) + len(BTN_END)
assert i < j and j - i < 1500
c = c[:i] + c[i + len(TS):j] + "," + TS[:-1] + c[j:]; print('OK: bot check moved below the buttons')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
