#!/usr/bin/env python3
"""Patch v889 -> v890: don't show the flying-bird loader for a keyword search while the search box is focused.

The user noticed the remaining cursor glitch only happens for keyword searches, never for tag matches. A keyword
search fetches from the server and shows the bird loader (_Bd, endlessly animated) while it waits, then removes it
when results arrive. That's another animated layer coming and going near the focused search box, the same kind
of change that made iOS misdraw the cursor when the tags dropdown came and went (v887/v889). Tag matches filter
on the phone with no loader. While typing, the feed now just updates when the results arrive; the bird still
shows in every other case.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v889.js'
dst = '_deploy/assets/index-DUcNPOLc-v890.js'
content = open(src, encoding='utf-8').read()
old = '(m?SRLoading:qT?_tmL:(u||d||f||p)?_tgL:_hL)&&(0,L.jsx)(_Bd,{})'
new = '(m?(SRLoading&&!(document.activeElement&&document.activeElement.classList&&document.activeElement.classList.contains(`search-input`))):qT?_tmL:(u||d||f||p)?_tgL:_hL)&&(0,L.jsx)(_Bd,{})'
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old))); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
