#!/usr/bin/env python3
"""Patch v1046 -> v1047: full-screen link view gets a fixed frosted action bar.
- 🪽/💬/↗ sit in one frosted-glass bar pinned near the bottom of every post (same spot on every post), as plain
  icons + counts with no boxes. Flapped = purple bird with a soft glow.
- The swipe hint is a quiet line (arrow + text, then just the arrow once you've swiped) under the bar.
- The post's content keeps clear of the bar; tapping the bar's empty space doesn't close the view."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1046.js'
dst = '_deploy/assets/index-DUcNPOLc-v1047.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('if(e.target.closest(`.reel-btn,.reel-site`))return;close()', 'if(e.target.closest(`.reel-btn,.reel-site,.reel-btns`))return;close()', 'bar taps do not close')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel .reel-slide{position:relative;padding-bottom:calc(112px + env(safe-area-inset-bottom))}
.reel .reel-btns{position:absolute;left:50%;transform:translateX(-50%);bottom:calc(38px + env(safe-area-inset-bottom));width:min(calc(100% - 32px),520px);margin:0;height:56px;box-sizing:border-box;padding:0 6px;gap:0;display:flex;align-items:stretch;
 border-radius:20px;background:rgba(30,35,46,.55);-webkit-backdrop-filter:blur(18px) saturate(1.4);backdrop-filter:blur(18px) saturate(1.4);border:1px solid rgba(255,255,255,.08);box-shadow:0 10px 30px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.05)}
.reel .reel-btns .reel-btn.reel-mini{flex:1 1 0;height:100%;background:transparent;border:0;border-radius:14px;color:#cbd5e1;font-size:14px;font-weight:700;gap:8px;padding:0;-webkit-tap-highlight-color:transparent;transition:color .15s,background .15s}
.reel .reel-btns .reel-btn.reel-mini:active{background:rgba(255,255,255,.06)}
.reel .reel-btns .reel-btn.reel-mini + .reel-btn.reel-mini{position:relative}
.reel .reel-btns .reel-btn.reel-mini + .reel-btn.reel-mini::before{content:"";position:absolute;left:0;top:18px;bottom:18px;width:1px;background:rgba(255,255,255,.07)}
.reel .reel-btns .reel-btn.reel-mini.reel-flap.on{background:transparent;border:0;color:#c084fc}
.reel .reel-flap.on .ri{filter:drop-shadow(0 0 6px rgba(192,132,252,.7))}
.reel .reel-flap.on .n{color:#e9d5ff}
.reel .reel-flap .ri{width:24px;height:24px}
.reel .reel-chat .ri{width:19px;height:19px}
.reel .reel-share .ri{width:13px;height:13px}
.reel .reel-btns .reel-btn.reel-mini.reel-share.done{color:#c084fc;border:0}
.reel .reel-hint{bottom:calc(12px + env(safe-area-inset-bottom));padding:0;background:transparent;color:#64748b;font-size:11px;font-weight:600;gap:6px;letter-spacing:.02em}
.reel .reel-hint.small{padding:0;background:transparent}
.reel .reel-hint .reel-arrow{font-size:13px}
.reel .reel-hint.end{background:transparent;color:#86efac}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
