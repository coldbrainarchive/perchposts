#!/usr/bin/env python3
"""Patch v1307 -> v1308: one remembered sound setting for every video.
Videos start muted unless you've turned sound on before (localStorage pp_reel_sound, which the post scroller already
used). Turning sound on/off on any post/chirp/scroller video (its own controls or the scroller's speaker button) is
remembered for all videos. Composer tray thumbnails (always muted) are ignored."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1307.js'
dst = '_deploy/assets/index-DUcNPOLc-v1308.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("(0,L.jsx)(`video`,{src:n,controls:!0,playsInline:!0,loop:!0,preload:`metadata`,poster:_vpost,",
      "(0,L.jsx)(`video`,{src:n,controls:!0,playsInline:!0,loop:!0,preload:`metadata`,poster:_vpost,\"data-snd\":``,ref:_el=>{if(_el&&!_el._sndInit){_el._sndInit=1;const m=!_ppSnd();_el.defaultMuted=m;_el.muted=m}},", 'post/chirp video starts with the setting')
patch("v.muted=!_ppSnd();v.defaultMuted=v.muted;if(v.muted)v.setAttribute(`muted`,``);",
      "v.muted=!_ppSnd();v.defaultMuted=v.muted;if(v.muted)v.setAttribute(`muted`,``);v.dataset.snd=``;", 'scroller video tagged')
c += r"""
;document.addEventListener(`volumechange`,e=>{const v=e.target;if(!v||v.tagName!==`VIDEO`||v.dataset.snd==null)return;try{localStorage.setItem(`pp_reel_sound`,v.muted||v.volume===0?`0`:`1`)}catch(_){}},!0);
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
