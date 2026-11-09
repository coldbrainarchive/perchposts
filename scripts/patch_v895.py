#!/usr/bin/env python3
"""Patch v894 -> v895: TEMPORARY experiment switch for the remaining search-cursor glitch (deleting "et" -> "e"
grows the suggestions box from one row to the full Boards/Regions list, past its 380px max-height, and the
cursor is misdrawn for ~0.2s). /?sdx=<mode> (kept in localStorage), /?sdx=0 off. Modes:
  ovh - suggestions box never scrolls (overflow hidden)       -> tests the "scroll layer created" theory
  tz  - suggestions box always on its own layer (translateZ)
  scr - suggestions box always scroll-capable (overflow-y: scroll)
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v894.js'
dst = '_deploy/assets/index-DUcNPOLc-v895.js'
content = open(src, encoding='utf-8').read()
X = r'''
;(()=>{try{const q=new URLSearchParams(location.search).get('sdx');if(q==='0')localStorage.removeItem('sdx');else if(q)localStorage.setItem('sdx',q);
const m=localStorage.getItem('sdx');if(!m)return;
const css={ovh:'.search-dropdown{overflow:hidden!important}',tz:'.search-dropdown{transform:translateZ(0);will-change:transform}',scr:'.search-dropdown{overflow-y:scroll!important}'}[m];
if(!css)return;const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
const b=document.createElement('div');b.textContent='sdx:'+m;b.style.cssText='position:fixed;right:4px;bottom:120px;font:9px monospace;color:#7CFC9A;z-index:9;pointer-events:none';document.body.appendChild(b);
}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(content + X)
print('Wrote ' + dst)
