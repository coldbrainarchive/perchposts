#!/usr/bin/env python3
"""Patch v1041 -> v1042: full-screen link view drops the Open Link and Open Post buttons.
- The website name under the text (e.g. FT.COM ↗) is now the link to the article.
- 💬 already goes into the post's chat, so Open Post isn't needed.
The row is three equal pills: 🪽 · 💬 · ↗ Share."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1041.js'
dst = '_deploy/assets/index-DUcNPOLc-v1042.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('const site=document.createElement(`div`);site.className=`reel-site`;site.textContent=host(d.url);inner.appendChild(site);',
 'const site=document.createElement(`a`);site.className=`reel-site`;site.href=d.url;site.target=`_blank`;site.rel=`noopener noreferrer`;'
 'const sn=document.createElement(`span`);sn.textContent=host(d.url);const sa=document.createElement(`span`);sa.className=`reel-site-ar`;sa.textContent=`↗`;site.append(sn,sa);'
 'site.addEventListener(`click`,e=>e.stopPropagation());inner.appendChild(site);', 'site is the link')
patch('btns.append(open,fl,ch,sh,post);', 'btns.append(fl,ch,sh);', 'row without open buttons')
patch('sh.textContent=`↗`;sh.onclick', 'sh.textContent=`↗ Share`;sh.onclick', 'share label')
patch('sh.textContent=`✓`;sh.classList.add(`done`);setTimeout(()=>{sh.textContent=`↗`;', 'sh.textContent=`✓ Shared`;sh.classList.add(`done`);setTimeout(()=>{sh.textContent=`↗ Share`;', 'share done label')
patch('if(e.target.closest(`.reel-btn`))return;close()', 'if(e.target.closest(`.reel-btn,.reel-site`))return;close()', 'tap on site does not close')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel a.reel-site{display:inline-flex;align-self:flex-start;align-items:center;gap:5px;text-decoration:none;padding:6px 0;margin-top:6px;-webkit-tap-highlight-color:transparent}
.reel a.reel-site:active{opacity:.6}
.reel .reel-site-ar{font-size:13px;line-height:1}
.reel .reel-btns .reel-btn.reel-mini{flex:1 1 0}
.reel .reel-share{width:auto;font-size:13px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
