#!/usr/bin/env python3
"""Patch v1247 -> v1248: Flock's icon is a bird's head (was a feather), and the search 🔍 emoji
becomes a line magnifier: the search bar, the "Search posts for …" row and the no-results screen."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1247.js'
dst = '_deploy/assets/index-DUcNPOLc-v1248.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
HEAD = '<svg class="ri" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
ICONS = {
 'BIRDHEAD': '<path d="M16.5 7A6 6 0 0 0 5 9.5c0 2.2 1 4 2.5 5L6 21h9.5c0-3 1-5 1-8.5"/><path d="M16.5 7 21.5 9.5l-5 1.5"/><path d="M12.5 8h.01"/>',
 'SEARCH': '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
}
add = ''.join('"%s": "%s", ' % (k, (HEAD + v + '</svg>').replace('"', '\\"')) for k, v in ICONS.items())
patch('function _ppIco(k){return ({', 'function _ppIco(k){return ({' + add, 'new icons')
patch('const _SPK={activity:`FEATHER`,', 'const _SPK={activity:`BIRDHEAD`,', 'Flock = bird head')
patch("(0,L.jsx)(`span`,{className:`search-icon`,children:`🔍`})",
      "(0,L.jsx)(`span`,{className:`search-icon pp-srch-ic`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{__html:_ppIco(`SEARCH`)}})", 'search bar')
patch("children:[(0,L.jsx)(`span`,{children:`🔍`}),(0,L.jsx)(`span`,{style:{whiteSpace:`nowrap`",
      "children:[(0,L.jsx)(`span`,{className:`pp-srch-ic`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{__html:_ppIco(`SEARCH`)}}),(0,L.jsx)(`span`,{style:{whiteSpace:`nowrap`", 'search posts row')
patch("(0,L.jsx)(`div`,{style:{fontSize:32,marginBottom:8},children:`🔍`})",
      "(0,L.jsx)(`div`,{className:`pp-big-ic`,style:{width:32,height:32,margin:`0 auto 8px`,color:`#64748b`},dangerouslySetInnerHTML:{__html:_ppIco(`SEARCH`)}})", 'no results')
patch("body .lb-ic{", "body .pp-srch-ic{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;flex-shrink:0;color:#94a3b8}body .pp-srch-ic svg{width:100%!important;height:100%!important;display:block;stroke-width:2.4}body .lb-ic{", 'search icon style')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
