#!/usr/bin/env python3
"""Patch v884 -> v887: stop the search box's cursor being drawn 1-3 characters off for a moment while typing on
iPhone. (v885's defaultValue change made no difference and is not carried over; v886 was a recorder-only build.)

Filmed on the user's iPhone and lined up with v886's recorder: the misdrawn cursor happens exactly when the tags
dropdown (#_urd) is added to or removed from the page, e.g. "ireland" -> "ireland i" removes it (no matches),
deleting back to "ireland " adds it again. When the dropdown only changes its contents there's no glitch, and
nothing writes to the search box. The dropdown is its own scrolling layer right under the box, and adding or
removing it makes iOS redraw the cursor from stale layout.

Fix: while the search panel is open, keep the dropdown on the page and only hide it (visibility hidden, no
pointer events) when it has nothing to show, so the layer never comes and goes while typing. Keeps v884's
recorder for testing.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v884.js'
dst = '_deploy/assets/index-DUcNPOLc-v887.js'
content = open(src, encoding='utf-8').read()
old = '(E&&(S||C||P||w||T||UR.length>0))&&(0,L.jsxs)(`div`,{className:`search-dropdown`,id:`_urd`,children:'
new = 'E&&(0,L.jsxs)(`div`,{className:`search-dropdown`,id:`_urd`,style:(S||C||P||w||T||UR.length>0)?void 0:{visibility:`hidden`,pointerEvents:`none`},children:'
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old))); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
