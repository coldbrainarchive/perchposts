#!/usr/bin/env python3
"""Patch v1303 -> v1304: our own worm icon + worms in the post scroller.
- _ppIco(`WORM`) is now a line traced from the 🪱 emoji (option D), in the emoji's red. Used everywhere small: card and
  post pills, chirp pills, tabs, who-gave rows, give buttons, notification badges, the scroller bar.
- Big spots keep the emoji (_ppIco(`WORMEMO`)): the Worm wallet header, the picker's "Worm wallet" row, the emoji sheet's
  worm button, the big worm in the chirp quick-react row. Bird ID rows keep 🪱 like their other emoji rows.
- Post scroller bar: birds' posts get a worm slot (flap | chirp | worm N | Share), live count; tap opens the Worm wallet
  above the scroller (no lifted card). News/bot posts keep the 3-part bar."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1303.js'
dst = '_deploy/assets/index-DUcNPOLc-v1304.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
P = "M5.3 2.4C3.9 4.5 4 7.6 6.6 7.8C9.4 8 12.6 4.3 16.3 3.9C19.3 3.6 20.6 6.7 18.3 8.7C15.9 10.6 10.6 10.9 8.1 13.2C5.9 15.4 7.4 19.3 11 19.4C14.5 19.5 18 17.6 20.7 15.8"
LINE = '<svg class=\\"ri wline\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2.2\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" style=\\"color:#e8555c\\" aria-hidden=\\"true\\"><path d=\\"' + P + '\\"/></svg>'
patch('"WORM": "<span class=\\"ri wemo\\" aria-hidden=\\"true\\">🪱</span>",',
      '"WORM": "' + LINE + '", "WORMEMO": "<span class=\\"ri wemo\\" aria-hidden=\\"true\\">🪱</span>",', 'icon')
# big spots keep the emoji
patch('<span class="ww-ic">${_ppIco(`WORM`)}</span>', '<span class="ww-ic">${_ppIco(`WORMEMO`)}</span>', 'wallet header')
patch('<span class="pp-ic pp-worm">${_ppIco(`WORM`)}</span><span class="pp-pick-wl">Worm wallet</span>', '<span class="pp-ic pp-worm">${_ppIco(`WORMEMO`)}</span><span class="pp-pick-wl">Worm wallet</span>', 'picker wallet row')
patch("wb.innerHTML=_ppIco(`WORM`);nav.prepend(wb)", "wb.innerHTML=_ppIco(`WORMEMO`);nav.prepend(wb)", 'emoji sheet worm button')
patch("_ppPicker(b,`c`,id)},dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}", "_ppPicker(b,`c`,id)},dangerouslySetInnerHTML:{__html:_ppIco(`WORMEMO`)}}", 'quick-react worm')
# notification badge
patch("e.icon===`AT`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#c084fc`},dangerouslySetInnerHTML:{__html:_ppIco(`AT`)}}):e.icon",
      "e.icon===`AT`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#c084fc`},dangerouslySetInnerHTML:{__html:_ppIco(`AT`)}}):e.icon===`🪱`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}):e.icon", 'notif badge')
# wallet can open without the lifted card (post scroller)
patch("function _wormWallet(id,own){if(document.querySelector(`.ww-ov`))return;\n const src=document.querySelector(`.feed-post-card`);",
      "function _wormWallet(id,own,bare){if(document.querySelector(`.ww-ov`))return;\n const src=bare?null:document.querySelector(`.feed-post-card`);", 'wallet bare')
# scroller worm slot
patch("const ch=mk(`reel-chat`,_ppIco(`CHAT`),`Open the chat`);ch.onclick=e=>{e.stopPropagation();",
      "const wm=mk(`reel-worm`,_ppIco(`WORM`),`Worms`);{const wn=d.who&&d.who.n,ok=!!wn&&!/^Anon #/.test(wn)&&!_ppIsBot({username:wn});wm.hidden=!ok;if(ok){const K=_ppWorm.key(`p`,d.post),up=()=>{wm.querySelector(`.n`).textContent=_ppWorm.n(K)};_ppWorm.sub(K,up);_ppWorm.want(`p`,d.post);up();"
      "wm.onclick=e=>{e.stopPropagation();if(!localStorage.getItem(`auth_token`)){pendingNoAuth=!0;close();return}const me=(localStorage.getItem(`_myUsername`)||``).toLowerCase();_wormWallet(d.post,!!me&&me===wn.toLowerCase(),1)}}}"
      "const ch=mk(`reel-chat`,_ppIco(`CHAT`),`Open the chat`);ch.onclick=e=>{e.stopPropagation();", 'worm button')
patch("btns.append(fl,ch,sh);inner.appendChild(btns);", "btns.append(fl,ch,wm,sh);inner.appendChild(btns);", 'append worm')
patch("d.dataset.k=[...b.classList].find(x=>/^reel-(flap|chat|share)$/.test(x))||``;", "d.dataset.k=[...b.classList].find(x=>/^reel-(flap|chat|worm|share)$/.test(x))||``;", 'dock key')
patch("body .lb-ic{", "html.reel-shown .ww-ov{z-index:9800!important}body .reel-dbtn.reel-worm .ri,body .reel-btn.reel-worm .ri{width:17px;height:17px}body .reel-dbtn[hidden]{display:none!important}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
