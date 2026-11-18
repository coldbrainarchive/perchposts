#!/usr/bin/env python3
"""Patch v1204 -> v1205 (scroller fades):
- One permanent fade fixed to the screen: the scrolling area itself fades to black at the top and bottom edges
  (a mask on a still wrapper around the moving track), so nothing moves or pops when you swipe. Nothing is painted
  onto the photos/videos any more (the per-slide shading and the v1204 overlay strips are gone).
- Everything around it is the same pure black: the scroller background, Safari's bar colour (theme-color) and the
  page behind, so Safari's top and bottom bars blend into the fade.
- Text over photos/videos gets a soft shadow so it stays readable without shading on the picture.
- The title / name / VIEW POST layer is drawn on its own layer above the video, so it's already there as a video
  slide comes on screen (iPhones could draw it late, popping in on arrival)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1204.js'
dst = '_deploy/assets/index-DUcNPOLc-v1205.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("const track=document.createElement(`div`);track.className=`reel-track`;ov.appendChild(track);",
      "const track=document.createElement(`div`);track.className=`reel-track`;const rview=document.createElement(`div`);rview.className=`reel-view`;rview.appendChild(track);ov.appendChild(rview);", 'still wrapper for the fade')
patch("tcm&&tcm.setAttribute(`content`,`#0b0c10`);", "tcm&&tcm.setAttribute(`content`,`#000000`);", 'Safari bar colour')
css = ("html.reel-shown.reel-shown,html.reel-shown.reel-shown body{background:#000!important}"
       "body .reel{background:#000!important}"
       "body .reel-view{position:absolute;inset:0;overflow:hidden;"
       "-webkit-mask-image:linear-gradient(to bottom,transparent 0,rgba(0,0,0,.35) calc(30px + env(safe-area-inset-top)),#000 calc(110px + env(safe-area-inset-top)),#000 calc(100% - 52px - env(safe-area-inset-bottom)),rgba(0,0,0,.35) calc(100% - 18px - env(safe-area-inset-bottom)),transparent 100%);"
       "mask-image:linear-gradient(to bottom,transparent 0,rgba(0,0,0,.35) calc(30px + env(safe-area-inset-top)),#000 calc(110px + env(safe-area-inset-top)),#000 calc(100% - 52px - env(safe-area-inset-bottom)),rgba(0,0,0,.35) calc(100% - 18px - env(safe-area-inset-bottom)),transparent 100%)}"
       "body .reel-fade-t,body .reel-fade-b{display:none!important}"
       "body .reel .reel-m::after{display:none!important}"
       "body .reel .reel-m .reel-media{background:#000!important}"
       "body .reel .reel-m .reel-inner>:not(.reel-media){transform:translateZ(0);will-change:transform}"
       "body .reel .reel-m .reel-title{text-shadow:0 1px 3px rgba(0,0,0,.85),0 0 18px rgba(0,0,0,.55)!important}"
       "body .reel .reel-m .reel-head .reel-tag,body .reel .reel-m a.reel-site{text-shadow:0 1px 3px rgba(0,0,0,.9),0 0 12px rgba(0,0,0,.6)}"
       "body .reel .reel-m .reel-head .reel-tag{background:rgba(0,0,0,.18)!important}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
