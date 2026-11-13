#!/usr/bin/env python3
"""Patch v1037 -> v1038: the post time in the full-screen link view is an outline pill like the tags beside it
(same size and border, in grey). It keeps lowercase so "48m ago" doesn't read as "48M AGO"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1037.js'
dst = '_deploy/assets/index-DUcNPOLc-v1038.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('tm.className=`reel-time`;', 'tm.className=`reel-tag reel-time`;', 'time as pill')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel-head .reel-tag.reel-time{color:#94a3b8;border-color:#94a3b8;background:transparent;-webkit-backdrop-filter:none;backdrop-filter:none;text-transform:none;letter-spacing:.02em;line-height:1;font-size:10px;font-weight:800;height:20px;margin-top:0}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
