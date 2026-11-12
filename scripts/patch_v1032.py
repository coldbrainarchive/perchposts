#!/usr/bin/env python3
"""Patch v1030 -> v1032 (v1031's Read more is dropped at the user's request).
Back to the v1030 description: the whole text, scrollable with your finger inside the text area (soft fade when
there's more; a swipe on the text scrolls it first, then changes post at the end).
Kept from v1031: the tags sit above the photo at its top-left corner (mini outline pills), not on the photo."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1030.js'
dst = '_deploy/assets/index-DUcNPOLc-v1032.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("if(d.image){const med=document.createElement(`div`);med.className=`reel-media`;",
      "if((d.tags||[]).length){const tr=tagRow();tr.classList.add(`flat`);inner.appendChild(tr)}if(d.image){const med=document.createElement(`div`);med.className=`reel-media`;",
      'tags row above the photo')
patch("if((d.tags||[]).length)med.appendChild(tagRow());inner.appendChild(med)}else if((d.tags||[]).length){const tr=tagRow();tr.classList.add(`flat`);inner.appendChild(tr)}",
      "inner.appendChild(med)}", 'no tags on the photo')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel-tags.flat{margin-bottom:10px}
.reel-tags.flat .reel-tag{background:transparent;-webkit-backdrop-filter:none;backdrop-filter:none}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
