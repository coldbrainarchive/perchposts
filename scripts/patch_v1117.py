#!/usr/bin/env python3
"""Patch v1116 -> v1117: the post card flap animation survives the card being re-drawn mid-flap (on iPhone the server's
answer arrives during the animation and the redraw cut it off after the first wing lift). For a second after the tap,
whenever the icon is replaced, the animation carries on on the new icon from where it had got to."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1116.js'
dst = '_deploy/assets/index-DUcNPOLc-v1117.js'
c = open(src, encoding='utf-8').read()
old = "requestAnimationFrame(()=>requestAnimationFrame(()=>_ppFlapAnim(b)))}catch(er){}},!0)"
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
new = ("const t0=performance.now(),kick=()=>{const a=b.querySelector(`.pp-bird animate`);if(!a||a._ppK===t0)return;const el=(performance.now()-t0)/1000;if(el>.74)return;a._ppK=t0;"
       "try{a.endElement&&a.endElement();el>.02&&a.beginElementAt?a.beginElementAt(-el):a.beginElement()}catch(e){}};"
       "kick();const mo=new MutationObserver(kick);mo.observe(b,{childList:!0,subtree:!0});setTimeout(()=>mo.disconnect(),900)}catch(er){}},!0)")
c = c.replace(old, new); print('OK: animation carries on through re-draws')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
