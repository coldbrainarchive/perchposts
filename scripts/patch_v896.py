#!/usr/bin/env python3
"""NOT KEPT (scroll mode still switched mid-typing; replaced by v897). Patch v894 -> v896: fix the last iPhone search-cursor glitch (v895 was a temporary experiment switch).
Filmed on the user's iPhone: deleting "et" -> "e" swaps the suggestions box from the one-row "Search posts for"
to the Boards/Regions list, and the cursor was drawn two letters too far right for ~0.2s. The box is a scroll
container (overflow-y:auto); with overflow hidden the glitch was gone in 2/2 runs, while the normal box and an
always-scrollable box (overflow-y:scroll) both glitched. So the box is now only scrollable while its list is
taller than the box (e.g. a long country list); short lists never make it a scroll container.
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v894.js'
dst = '_deploy/assets/index-DUcNPOLc-v896.js'
content = open(src, encoding='utf-8').read()
old = 'max-height: 380px;\n        overflow-y: auto;\n        scrollbar-width: thin;\n        padding: 6px 0;'
new = 'max-height: 380px;\n        overflow-y: hidden;\n        scrollbar-width: thin;\n        padding: 6px 0;'
if content.count(old) != 1:
    print('FAIL css', content.count(old)); sys.exit(1)
content = content.replace(old, new)
FIX = r'''
;(()=>{try{
const fit=()=>{const d=document.getElementById('_urd');if(!d)return;const o=d.scrollHeight>d.clientHeight+1?'auto':'hidden';if(d.style.overflowY!==o)d.style.overflowY=o};
let q=0;new MutationObserver(()=>{if(q)return;q=1;requestAnimationFrame(()=>{q=0;fit()})}).observe(document.body,{childList:true,subtree:true});
}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(content + FIX)
print('Wrote ' + dst)
