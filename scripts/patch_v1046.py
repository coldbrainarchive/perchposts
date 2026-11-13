#!/usr/bin/env python3
"""Patch v1045 -> v1046: share icon goes back to the ↗ arrow (drawn to fill its box, so there's no blank space
around it), with a tighter icon-to-word gap on the post cards. Same arrow in the full-screen view."""
import sys, json
src = '_deploy/assets/index-DUcNPOLc-v1045.js'
dst = '_deploy/assets/index-DUcNPOLc-v1046.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
SV = '<svg class="ri" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
old = SV + '<path d="M12 14.5V3.5M8 7.5l4-4 4 4"/><path d="M8.5 10.5H7a2 2 0 0 0-2 2V19a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6.5a2 2 0 0 0-2-2h-1.5"/></svg>'
new = '<svg class="ri ri-arrow" viewBox="5 5 14 14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M8.5 7H17v8.5"/></svg>'
patch(json.dumps(old)[1:-1], json.dumps(new)[1:-1], 'share icon -> arrow')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.feed-post-action-pill .pp-ic.pp-share .ri{width:10px;height:10px}
.feed-post-action-pill:has(.pp-share){gap:4px}
.reel .reel-share .ri{width:13px;height:13px}
.reel .reel-share{gap:6px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
