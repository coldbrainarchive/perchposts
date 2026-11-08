#!/usr/bin/env python3
"""Patch v883 -> v889: v887's search-dropdown fix without the typing recorder (v884-v888 were test builds).

While the search panel is open, the tags dropdown stays on the page and is hidden with visibility:hidden when it
has nothing to show, instead of being removed. Removing it (and opacity:0, tried in v888) made iOS draw the
search box's cursor 2-3 characters off after a pause; with visibility:hidden the typing case was clean in 2/2
filmed runs on the user's iPhone. A brief (~100ms) misdraw can remain when deleting back into a word that brings
tags back.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v883.js'
dst = '_deploy/assets/index-DUcNPOLc-v889.js'
content = open(src, encoding='utf-8').read()
old = '(E&&(S||C||P||w||T||UR.length>0))&&(0,L.jsxs)(`div`,{className:`search-dropdown`,id:`_urd`,children:'
new = 'E&&(0,L.jsxs)(`div`,{className:`search-dropdown`,id:`_urd`,style:(S||C||P||w||T||UR.length>0)?void 0:{visibility:`hidden`,pointerEvents:`none`},children:'
if content.count(old) != 1:
    print('FAIL: found ' + str(content.count(old))); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content.replace(old, new))
print('Wrote ' + dst)
