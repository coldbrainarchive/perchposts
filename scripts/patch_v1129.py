#!/usr/bin/env python3
"""Patch v1128 -> v1129: worms are like awards.
- The 🪱 pill (feed cards, next to the bird on the post page, the 🪱 tab in a chirp's sheet) only shows once a worm has
  been given. Posts still get worms through the preview's Reactions menu (🪱 tab, folded Give worms).
- Bot posts can't get worms (the worker already refuses): no 🪱 tab or Give row in their Reactions."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1128.js'
dst = '_deploy/assets/index-DUcNPOLc-v1129.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# cards: no pill until a worm is given
patch("children:[(0,L.jsx)(`span`,{className:`pp-ic pp-worm`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),(0,L.jsx)(`span`,{children:_ppWorm.n(K)})]})}",
      "children:[(0,L.jsx)(`span`,{className:`pp-ic pp-worm`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),(0,L.jsx)(`span`,{children:_ppWorm.n(K)})]})}",
      'card pill (anchor check)')
patch("function _CardWorm({id}){const K=_ppWorm.key(`p`,id),[,f]=(0,_.useState)(0);(0,_.useEffect)(()=>{_ppWorm.want(`p`,id);return _ppWorm.sub(K,()=>f(x=>x+1))},[K]);\n return(",
      "function _CardWorm({id}){const K=_ppWorm.key(`p`,id),[,f]=(0,_.useState)(0);(0,_.useEffect)(()=>{_ppWorm.want(`p`,id);return _ppWorm.sub(K,()=>f(x=>x+1))},[K]);\n if(!_ppWorm.n(K))return null;return(",
      'card pill only with worms')
# post page pill: only with worms
patch("const sheet=open?", "if(!nw&&!open)return null;const sheet=open?", 'post pill only with worms')
# bot posts: no worm tab
patch("function _PostReactions({id}){", "const _ppIsBot=p=>!!p&&(fr.includes(p.username)||String(p.browser_id||``).startsWith(`bot-`));\nfunction _PostReactions({id,bot}){", 'reactions know bot posts')
patch("T(`all`,`All ${list.length}`),T(`flap`,[ic(`BIRD`),nf]),T(`worm`,[ic(`WORM`),nw])",
      "T(`all`,`All ${list.length}`),T(`flap`,[ic(`BIRD`),nf]),bot?null:T(`worm`,[ic(`WORM`),nw])", 'no worm tab on bot posts')
patch("tab===`worm`?(0,L.jsx)(_WormGivers,", "tab===`worm`&&!bot?(0,L.jsx)(_WormGivers,", 'bot posts never show the give row')
patch("(0,L.jsx)(_PostReactions,{id:r},`prx`)", "(0,L.jsx)(_PostReactions,{id:r,bot:_ppIsBot(c)},`prx`)", 'post page passes bot')
# chirp sheet: 🪱 tab only when the chirp has worms
patch("cid?tab(`🪱`,", "cid&&_ppWorm.n(_ppWorm.key(`c`,cid))?tab(`🪱`,", 'chirp 🪱 tab only with worms')
# the preview menu opens upward when there's no room below (it used to land off screen)
patch("m.style.top=(r.bottom+6)+`px`;", "m.style.top=(r.bottom+6+m.offsetHeight>innerHeight-8&&r.top-6-m.offsetHeight>8?r.top-6-m.offsetHeight:r.bottom+6)+`px`;", 'menu flips up')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
