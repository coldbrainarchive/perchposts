#!/usr/bin/env python3
"""Patch v1063 -> v1064: the sticky search bar sits under the header using the header's measured height (--pp-hdr)
instead of fixed numbers. The bigger logo made the phone header 65px, so the old 62px slid under it."""
src = '_deploy/assets/index-DUcNPOLc-v1063.js'
dst = '_deploy/assets/index-DUcNPOLc-v1064.js'
c = open(src, encoding='utf-8').read()
c += r''';(()=>{try{const s=document.createElement(`style`);s.textContent=`
html body .search-shell{top:calc(var(--pp-hdr,69px) + 4px)}
@media (max-width:900px){html body .search-shell{top:var(--pp-hdr,65px)}}
`;document.head.appendChild(s);
let ro=null,seen=null;const set=h=>{if(h>0)document.documentElement.style.setProperty(`--pp-hdr`,Math.round(h)+`px`)};
const hook=()=>{const b=document.querySelector(`.app-topbar`);if(!b||b===seen)return;seen=b;set(b.getBoundingClientRect().height);ro&&ro.disconnect();
 if(window.ResizeObserver){ro=new ResizeObserver(()=>set(b.getBoundingClientRect().height));ro.observe(b)}};
new MutationObserver(hook).observe(document.documentElement,{childList:!0,subtree:!0});hook();
}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
