#!/usr/bin/env python3
"""Patch v975 -> v976: letting go of the scrubber, the date pill fades out where it is (above the handle)
instead of jumping to the top of the chat for its fade."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v975.js'
dst = '_deploy/assets/index-DUcNPOLc-v976.js'
c = open(src, encoding='utf-8').read()
old = 'else{pill.style.left=(r.left+r.width/2)+`px`;pill.style.top=(r.top+10)+`px`;pill.classList.remove(`by`)}'
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, 'else{}')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
