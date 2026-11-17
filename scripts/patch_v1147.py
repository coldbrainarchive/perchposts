#!/usr/bin/env python3
"""Patch v1146 -> v1147: the chirp preview menu's "Reactions" is now "Flaps & worms" (purple flap icon), first in
the menu with a divider under it; the chirp views (Highlights, Top, Most replied, Latest, Media) follow."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1146.js'
dst = '_deploy/assets/index-DUcNPOLc-v1147.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch("const _CPL={hl:`✨ Highlights`,top:`🔥 Top`,rep:`↩️ Most replied`,latest:`🕒 Latest`,media:`🖼️ Media`,react:`😀 Reactions`};",
      "const _CPL={react:`🪽 Flaps & worms`,hl:`✨ Highlights`,top:`🔥 Top`,rep:`↩️ Most replied`,latest:`🕒 Latest`,media:`🖼️ Media`};", 'renamed, first')
patch("const _PPE={\"😀\":`SMILE`,", "const _PPE={\"🪽\":`BIRD`,\"😀\":`SMILE`,", 'flap icon for the label')
patch("  b.onclick=e=>{e.stopPropagation();set(k);close()};m.append(b)});",
      "  b.dataset.k=k;b.onclick=e=>{e.stopPropagation();set(k);close()};m.append(b);if(k===`react`){const d=document.createElement(`div`);d.className=`cp-sep`;m.append(d)}});", 'divider after it')
patch("body .lb-ic{", "body .cp-sep{height:1px;margin:4px 8px;background:rgba(148,163,184,.18)}body .cp-opt[data-k=react] .lb-ic,body .cp-filter[data-k=react] .lb-ic{color:#c084fc}body .lb-ic{", 'styles')
patch("className:`cp-filter`,\"aria-label\":", "className:`cp-filter`,\"data-k\":_cpm,\"aria-label\":", 'menu button knows the view')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
