#!/usr/bin/env python3
"""Patch v1293 -> v1294: the tag pills at the top of the post scroller show their line icons again, in the pill's
own colour (on the black background); copied from the feed card pill's svg. Flags were already there."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1293.js'
dst = '_deploy/assets/index-DUcNPOLc-v1294.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("if(out.some(o=>o.t===t))continue;out.push({t,c:bg,el:x})}return out}catch(e){return[]}}",
      "if(out.some(o=>o.t===t))continue;const sv=x.querySelector(`svg`);out.push({t,c:bg,el:x,ic:sv?sv.outerHTML:``})}return out}catch(e){return[]}}", 'copy icon')
patch("sp.className=`reel-tag`;sp.textContent=g.t;sp.style.color=g.c;sp.style.borderColor=g.c;",
      "sp.className=`reel-tag`;sp.textContent=g.t;sp.style.color=g.c;sp.style.borderColor=g.c;if(g.ic){const ti=document.createElement(`span`);ti.className=`reel-tic`;ti.setAttribute(`aria-hidden`,`true`);ti.innerHTML=g.ic;sp.prepend(ti)}", 'show icon')
patch("body .lb-ic{", "body .reel .reel-tic{display:inline-flex;width:12px!important;height:12px!important;margin-right:5px;flex-shrink:0;color:inherit}body .reel .reel-tic svg{width:12px!important;height:12px!important;stroke:currentColor;stroke-width:2.5}body .reel-tag:has(.reel-tic){display:inline-flex;align-items:center}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
