#!/usr/bin/env python3
"""Patch v1245 -> v1246: tapping an AI-check flag notification opens Mod Panel → Flagged (where you review it)
instead of the hidden post. /mod?tab=flagged opens the panel on that tab, and if the panel is already open it
switches to it. Works for flag notifications already sent too (they're the ones with the shield)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1245.js'
dst = '_deploy/assets/index-DUcNPOLc-v1246.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("return(0,L.jsxs)(I,{to:e.postId?`/post/${e.postId}",
      "return(0,L.jsxs)(I,{to:e.icon===`SHIELD`?`/mod?tab=flagged`:e.postId?`/post/${e.postId}",
      'flag notifications link to the Flagged tab')
patch("_nTap(_ev);_nMark(e);a()}",
      "e.icon===`SHIELD`&&setTimeout(()=>dispatchEvent(new CustomEvent(`pp-mod-flagged`)),60);_nTap(_ev);_nMark(e);a()}",
      'switch tab if the panel is already open')
patch("[_tb,_setTb]=(0,_.useState)(`flock`),",
      "[_tb,_setTb]=(0,_.useState)(()=>{try{return new URLSearchParams(location.search).get(`tab`)===`flagged`?`flagged`:`flock`}catch(e){return`flock`}}),_tbFl=(0,_.useEffect)(()=>{const show=()=>setTimeout(()=>{try{const t=[...document.querySelectorAll(`button`)].find(x=>x.textContent.trim().startsWith(`Flagged`));t&&t.scrollIntoView({inline:`center`,block:`nearest`})}catch(e){}},80);const f=()=>{_setTb(`flagged`);show()};if(new URLSearchParams(location.search).get(`tab`)===`flagged`)show();addEventListener(`pp-mod-flagged`,f);return()=>removeEventListener(`pp-mod-flagged`,f)},[]),",
      'panel opens on Flagged from the link')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
