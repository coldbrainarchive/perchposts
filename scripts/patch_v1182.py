#!/usr/bin/env python3
"""Patch v1181 -> v1182: an opened name pill no longer eats the tap that closes the Bird ID card.
iOS Safari drops a tap when the page changes on touch-down; the pill folded on pointerdown, so a tap/swipe on the
Bird ID sheet folded the pill and the sheet never got it. Now: taps on the Bird ID sheet (or any sheet) don't fold
the pill, and elsewhere it folds on click (after the tap) instead of on pointerdown."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1181.js'
dst = '_deploy/assets/index-DUcNPOLc-v1182.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("const out=ev=>{if(box.current&&!box.current.contains(ev.target))setOpen(!1)};",
      "const out=ev=>{const t=ev.target;if(t&&t.closest&&t.closest(`.bc-sheet,.hx-back,.ri-ov,.reel,[role=dialog]`))return;if(document.querySelector(`.bc-sheet`))return;if(box.current&&!box.current.contains(t))setOpen(!1)};", 'ignore sheet taps')
patch("document.addEventListener(`pointerdown`,out,!0);addEventListener(`pp-cu-open`,other);", "document.addEventListener(`click`,out,!0);addEventListener(`pp-cu-open`,other);", 'fold on click')
patch("document.removeEventListener(`pointerdown`,out,!0);removeEventListener(`pp-cu-open`,other)", "document.removeEventListener(`click`,out,!0);removeEventListener(`pp-cu-open`,other)", 'cleanup')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
