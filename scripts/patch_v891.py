#!/usr/bin/env python3
"""Patch v890 -> v891: collapse the empty search dropdown to zero height instead of hiding it.

Filmed on the user's iPhone: with v889/v890 the cursor still misdrew for ~100ms when deleting back into a word
that brings the tags back (the dropdown going from visibility:hidden to visible). The dropdown changing size
because its contents change never misdraws, so an empty dropdown is now a zero-height, borderless, clipped box
that grows back like any other content change. It stays on the page the whole time the search panel is open.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v890.js'
dst = '_deploy/assets/index-DUcNPOLc-v891.js'
content = open(src, encoding='utf-8').read()
old = '{visibility:`hidden`,pointerEvents:`none`}'
new = '{maxHeight:0,padding:0,border:`none`,boxShadow:`none`,overflow:`hidden`,pointerEvents:`none`}'
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old))); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
