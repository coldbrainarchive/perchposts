#!/usr/bin/env python3
"""Patch v1064 -> v1065: on phones the stuck search bar sits 6px lower, giving the same ~14px gap under the header
line as desktop. The search area's own background fills the gap so posts don't show through."""
src = '_deploy/assets/index-DUcNPOLc-v1064.js'
dst = '_deploy/assets/index-DUcNPOLc-v1065.js'
c = open(src, encoding='utf-8').read()
c += r''';(()=>{try{const s=document.createElement(`style`);s.textContent=`
@media (max-width:900px){html body .search-shell{top:calc(var(--pp-hdr,65px) + 6px)}html body .search-shell::before{top:-18px;height:18px}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
