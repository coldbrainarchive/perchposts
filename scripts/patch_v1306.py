#!/usr/bin/env python3
"""Patch v1305 -> v1306: giving worms makes the worm icon wiggle (body bends back and forth via an SVG path morph,
plus a little hop/sway) in every pill/bar showing that post's or chirp's count: feed card, post page, chirp pills,
scroller bar. Starts ~280ms after the gift so it plays as the wallet closes."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1305.js'
dst = '_deploy/assets/index-DUcNPOLc-v1306.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
P = "M5.3 2.4C3.9 4.5 4 7.6 6.6 7.8C9.4 8 12.6 4.3 16.3 3.9C19.3 3.6 20.6 6.7 18.3 8.7C15.9 10.6 10.6 10.9 8.1 13.2C5.9 15.4 7.4 19.3 11 19.4C14.5 19.5 18 17.6 20.7 15.8"
B = "M4.6 3.2C3.4 5.4 4.3 8.4 6.9 8.3C9.6 8.2 12.4 4.9 16 4.6C19.2 4.3 20.3 7.4 17.9 9.2C15.5 11 10.9 11.3 8.6 13.6C6.4 15.8 7.9 19.5 11.4 19.2C14.8 18.9 17.6 16.4 20 14.2"
C = "M6 2C4.3 3.8 3.8 7.1 6.3 7.4C9 7.8 12.9 3.6 16.6 3.3C19.4 3.1 21 6 18.7 8.2C16.4 10.3 10.3 10.5 7.7 12.8C5.4 15 6.9 19.2 10.6 19.6C14.2 20 18.3 18.6 21.2 17.3"
ANIM = '<animate attributeName=\\"d\\" dur=\\".95s\\" begin=\\"indefinite\\" fill=\\"remove\\" calcMode=\\"spline\\" keyTimes=\\"0;.18;.36;.54;.72;1\\" keySplines=\\".4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1\\" values=\\"' + ';'.join([P, B, C, B, C, P]) + '\\"/>'
patch('<path d=\\"' + P + '\\"/></svg>", "WORMEMO"', '<path d=\\"' + P + '\\">' + ANIM + '</path></svg>", "WORMEMO"', 'animate in icon')
# tag worm icons with their post/chirp key
patch("children:[(0,L.jsx)(`span`,{className:`pp-ic pp-worm`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),(0,L.jsx)(`span`,{children:n})]},`worm`);",
      "children:[(0,L.jsx)(`span`,{className:`pp-ic pp-worm`,\"data-wk\":K,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),(0,L.jsx)(`span`,{children:n})]},`worm`);", 'pill key')
patch("_ppWalletNext.add(id)},children:[(0,L.jsx)(`span`,{className:`pp-ic pp-worm`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),(0,L.jsx)(`span`,{children:_ppWorm.n(K)})]})}",
      "_ppWalletNext.add(id)},children:[(0,L.jsx)(`span`,{className:`pp-ic pp-worm`,\"data-wk\":K,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),(0,L.jsx)(`span`,{children:_ppWorm.n(K)})]})}", 'card key')
patch("(0,L.jsxs)(`span`,{className:`pr-w`,children:[(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),nw]})",
      "(0,L.jsxs)(`span`,{className:`pr-w`,children:[(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,\"data-wk\":`p:`+id,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),nw]})", 'post page key')
patch("const wm=mk(`reel-worm`,_ppIco(`WORM`),`Worms`);", "const wm=mk(`reel-worm`,_ppIco(`WORM`),`Worms`);wm.dataset.wk=_ppWorm.key(`p`,d.post);", 'reel key')
# fire it when a gift goes out
patch("pend.set(K,(pend.get(K)||0)+1);emit(K);", "pend.set(K,(pend.get(K)||0)+1);emit(K);setTimeout(()=>{try{window._ppWormWiggle&&window._ppWormWiggle(K)}catch(e){}},280);", 'trigger')
patch("body .lb-ic{", "@keyframes ppWormHop{0%{transform:scale(.85) rotate(0)}14%{transform:scale(1.12) translate(-1px,-1.5px) rotate(-12deg)}30%{transform:scale(1.06) translate(1px,0) rotate(10deg)}46%{transform:scale(1.04) translate(-1px,-.5px) rotate(-8deg)}62%{transform:scale(1) translate(.5px,0) rotate(6deg)}80%{transform:scale(.9) rotate(-2deg)}100%{transform:scale(.85) rotate(0)}}"
      "body .ri.wline.wig{animation:ppWormHop .95s cubic-bezier(.3,.7,.4,1)}@media (prefers-reduced-motion: reduce){body .ri.wline.wig{animation:none}}body .lb-ic{", 'css')
c += r"""
;window._ppWormWiggle=K=>{try{if(matchMedia(`(prefers-reduced-motion: reduce)`).matches)return;const els=[...document.querySelectorAll(`[data-wk="${CSS.escape(K)}"] .ri.wline,.ri.wline[data-wk="${CSS.escape(K)}"]`)];
 if(document.documentElement.classList.contains(`reel-shown`))els.push(...document.querySelectorAll(`.reel-dock .reel-worm .ri.wline`));
 for(const s of new Set(els)){const a=s.querySelector(`animate`);try{a&&a.beginElement()}catch(e){}s.classList.remove(`wig`);void s.getBoundingClientRect();s.classList.add(`wig`);clearTimeout(s._wt);s._wt=setTimeout(()=>s.classList.remove(`wig`),1000)}}catch(e){}};
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
