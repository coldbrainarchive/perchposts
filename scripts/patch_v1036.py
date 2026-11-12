#!/usr/bin/env python3
"""Patch v1035 -> v1036: the phone's top bar really goes black with the full-screen link view.
iPhone Safari tints the top bar from the page background (the full chat already does this), so while the view is
open the page background switches to the view's black (html.reel-open), and the view no longer fades in from
see-through (Safari could sample the colour mid-fade). Everything goes back on close."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1035.js'
dst = '_deploy/assets/index-DUcNPOLc-v1036.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('tcm&&tcm.setAttribute(`content`,`#0b0c10`);', 'tcm&&tcm.setAttribute(`content`,`#0b0c10`);document.documentElement.classList.add(`reel-open`);', 'page background black')
patch('tcm&&prevTc&&tcm.setAttribute(`content`,prevTc);', 'tcm&&prevTc&&tcm.setAttribute(`content`,prevTc);document.documentElement.classList.remove(`reel-open`);', 'and back on close')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
html.reel-open,html.reel-open body{background:#0b0c10!important}
.reel{opacity:1!important;transition:none!important}
.reel .reel-track{opacity:0;transition:opacity .18s}
.reel.in .reel-track{opacity:1}
@media (prefers-reduced-motion: reduce){.reel .reel-track{transition:none}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
