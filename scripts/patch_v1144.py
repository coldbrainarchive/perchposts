#!/usr/bin/env python3
"""Patch v1143 -> v1144: flapping your own post in the phone preview (reel) said nothing and still played the flap
animation, because the "You can't flap your own post" toast sat under the preview (z 3000 vs 9500).
- Toasts sit above everything (z 10000).
- Feed cards mark their bird on your own posts (data-own); the preview's flap checks it first: no animation, just
  the toast."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1143.js'
dst = '_deploy/assets/index-DUcNPOLc-v1144.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch(".hx-toast{position:fixed;left:50%;bottom:calc(28px + env(safe-area-inset-bottom));transform:translate(-50%,12px);z-index:3000;",
      ".hx-toast{position:fixed;left:50%;bottom:calc(28px + env(safe-area-inset-bottom));transform:translate(-50%,12px);z-index:10000;", 'toast above the preview')
patch("!(e.is_huddle||e.community_id===`feedback`)&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,style:r===1&&i?",
      "!(e.is_huddle||e.community_id===`feedback`)&&(0,L.jsxs)(`button`,{type:`button`,\"data-own\":_ppOwn(e.username)?`1`:void 0,className:`feed-post-action-pill`,style:r===1&&i?", 'card marks own posts')
patch("const flap=(s,id)=>{if(!localStorage.getItem(`auth_token`)){pendingNoAuth=!0;close();return}const b=_reelFlapBtn(id);if(!b)return;",
      "const flap=(s,id)=>{if(!localStorage.getItem(`auth_token`)){pendingNoAuth=!0;close();return}const b=_reelFlapBtn(id);if(!b)return;if(b.dataset.own){_ppOwnMsg();return}", 'preview: no animation on own posts')
patch("body .lb-ic{", "body:has(.reel) .hx-toast{bottom:calc(104px + env(safe-area-inset-bottom))}body .hx-toast{white-space:nowrap}body .lb-ic{", 'toast clears the preview bar')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
