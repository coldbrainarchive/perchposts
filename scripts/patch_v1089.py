#!/usr/bin/env python3
"""Patch v1088 -> v1089: the name box on profile cards is filled with the bird colour, like the username pill
(dark name text; the rank badge gets a dark chip so it still reads on the colour)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1088.js'
dst = '_deploy/assets/index-DUcNPOLc-v1089.js'
c = open(src, encoding='utf-8').read()
css = ("/*ppcardfill*/;(()=>{try{const s=document.createElement(`style`);s.textContent=`"
       ".bc-card.bc-card .bc-head.bc-rbox{background:var(--rc)!important;border:1.5px solid var(--rc)!important}"
       ".bc-card.bc-card .bc-rbox .bc-name{color:#0a0a0a!important}"
       ".bc-card.bc-card .bc-rbox .bc-rank{background:#15171d}"
       "`;document.head.appendChild(s)}catch(e){}})();/*/ppcardfill*/")
if c.count('/*ppnest*/') != 1: print('FAIL anchor'); sys.exit(1)
c = c.replace('/*ppnest*/', css + '/*ppnest*/'); print('OK: card name box filled')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
