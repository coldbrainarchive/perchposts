#!/usr/bin/env python3
"""Patch v1299 -> v1300: closing the Share sheet no longer leaves the post scroller blank.
The View-post gap fix (v1290/1291) ran on the keyboard's resize, measured the bar against a shrunken screen and
pushed slide padding up until the post vanished (it never shrinks back). Now it skips while the Share sheet is open,
an input has focus or the keyboard is up, and can add at most 120px to a slide's original padding."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1299.js'
dst = '_deploy/assets/index-DUcNPOLc-v1300.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("const gap=dr.top-(vr.bottom-sr.top);if(gap>=NEED-1)return!1;\n    const pb=parseFloat(getComputedStyle(s).paddingBottom)||0;s.style.setProperty(`padding-bottom`,(pb+Math.ceil(NEED-gap))+`px`,`important`);return!0};",
      "const gap=dr.top-(vr.bottom-sr.top);if(gap>=NEED-1)return!1;\n    const pb=parseFloat(getComputedStyle(s).paddingBottom)||0;if(s._pb0==null)s._pb0=pb;const nx=pb+Math.ceil(NEED-gap);if(nx-s._pb0>120)return!1;s.style.setProperty(`padding-bottom`,nx+`px`,`important`);return!0};", 'cap')
patch("const all=()=>{for(const s of document.querySelectorAll(`.reel .reel-slide`))settle(s)};",
      "const busy=()=>{try{if(document.querySelector(`.ps-ov`))return!0;const a=document.activeElement;if(a&&(a.tagName===`INPUT`||a.tagName===`TEXTAREA`))return!0;const vv=window.visualViewport;return!!(vv&&vv.height<innerHeight-120)}catch(e){return!1}};"
      "const all=()=>{if(busy())return;for(const s of document.querySelectorAll(`.reel .reel-slide`))settle(s)};", 'skip while sheet/keyboard')
patch("const settle=s=>{let n=0;", "const settle=s=>{if(busy())return;let n=0;", 'skip in settle too')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
