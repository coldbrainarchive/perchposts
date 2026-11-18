#!/usr/bin/env python3
"""Patch v1203 -> v1204 (scroller):
- The flaps / chirps / share bar sits lower, near the bottom edge (keeping the 15px gap above it).
- The top and bottom of the screen fade to black with fades that stay fixed while you swipe (they used to belong to
  each slide and slid along with it, showing hard edges between posts).
- The ✕, the photo counter and the sound button live on that fixed layer too, so they stay put and bright.
- Titles get their exact spacing the moment a slide is made (from font measurements cached once), so they no longer
  shift into place when a slide comes on screen."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1203.js'
dst = '_deploy/assets/index-DUcNPOLc-v1204.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
# cached title metrics, applied straight away
patch("function _reelCollect(){",
      "let _ppTTc=null;function _ppTTM(){if(_ppTTc)return _ppTTc;try{const cx=document.createElement(`canvas`).getContext(`2d`),ff=getComputedStyle(document.body).fontFamily;cx.font=`800 22px ${ff}`;const m=cx.measureText(`H`),asc=m.fontBoundingBoxAscent,dsc=m.fontBoundingBoxDescent,cap=m.actualBoundingBoxAscent;if(!asc||!cap)return null;const lh=22*1.28,hl=(lh-(asc+dsc))/2,r={t:hl+asc-cap,b:hl+dsc};if(!document.fonts||document.fonts.status===`loaded`)_ppTTc=r;return r}catch(e){return null}}\n"
      "try{document.fonts&&document.fonts.ready.then(()=>{_ppTTc=null;_ppTTM()})}catch(e){}\n"
      "function _reelCollect(){", 'title metrics cache')
patch("s._tt=()=>{try{if(!s.classList.contains(`reel-m`)||!t.isConnected)return;",
      "s._tt=()=>{try{if(!s.classList.contains(`reel-m`))return;const M=_ppTTM();if(M){t.style.setProperty(`margin-top`,-M.t+`px`,`important`);t.style.setProperty(`margin-bottom`,-M.b+`px`,`important`);return}if(!t.isConnected)return;", 'use cached metrics')
patch("-(hl+dsc)+`px`,`important`)}catch(e){}}}", "-(hl+dsc)+`px`,`important`)}catch(e){}};s._tt()}", 'apply at once')
# fixed chrome: fades, counter, sound
patch("ov.appendChild(xb);",
      "ov.appendChild(xb);"
      "const fdt=document.createElement(`div`);fdt.className=`reel-fade-t`;const fdb=document.createElement(`div`);fdb.className=`reel-fade-b`;ov.append(fdt,fdb);"
      "const gct=document.createElement(`div`);gct.className=`reel-gct`;gct.hidden=!0;ov.appendChild(gct);"
      "const gmu=document.createElement(`button`);gmu.type=`button`;gmu.className=`reel-gmu`;gmu.hidden=!0;ov.appendChild(gmu);"
      "gmu.addEventListener(`click`,e=>{e.stopPropagation();const m=slides[i]&&slides[i].querySelector(`.reel-mute`);m&&m.click();chrome()});"
      "let chMo=null;const chromeUpd=()=>{const s=slides[i],cc=s&&s.querySelector(`.reel-count`),mm=s&&s.querySelector(`.reel-mute`);gct.hidden=!cc;if(cc)gct.textContent=cc.textContent;gmu.hidden=!mm;if(mm){gmu.innerHTML=mm.innerHTML;gmu.setAttribute(`aria-label`,mm.getAttribute(`aria-label`)||``)}};"
      "const chrome=()=>{chromeUpd();try{chMo&&chMo.disconnect();chMo=new MutationObserver(chromeUpd);const s=slides[i];[s&&s.querySelector(`.reel-count`),s&&s.querySelector(`.reel-mute`)].forEach(x=>x&&chMo.observe(x,{childList:!0,characterData:!0,subtree:!0,attributes:!0}))}catch(e){}};", 'fixed fades + counter + sound')
patch("const label=()=>{try{dockBind()}catch(e){}", "const label=()=>{try{dockBind()}catch(e){}try{chrome()}catch(e){}", 'update fixed chrome per slide')
css = ("body .reel .reel-dock{bottom:calc(6px + env(safe-area-inset-bottom))!important;z-index:7}"
       "body .reel .reel-slide.reel-m{padding-bottom:calc(55px + env(safe-area-inset-bottom))!important}"
       "body .reel .reel-m::after{background:linear-gradient(to top,#000 0%,rgba(0,0,0,.82) 9%,rgba(0,0,0,.55) 24%,rgba(0,0,0,0) 48%),linear-gradient(to bottom,#000 0%,rgba(0,0,0,.65) 7%,rgba(0,0,0,0) 20%)!important}"
       "body .reel-fade-t,body .reel-fade-b{position:absolute;left:0;right:0;pointer-events:none;z-index:4}"
       "body .reel-fade-t{top:0;height:calc(96px + env(safe-area-inset-top));background:linear-gradient(to bottom,#000 0%,rgba(0,0,0,.75) 28%,rgba(0,0,0,.3) 65%,rgba(0,0,0,0) 100%)}"
       "body .reel-fade-b{bottom:0;height:calc(52px + env(safe-area-inset-bottom));background:linear-gradient(to top,#000 0%,rgba(0,0,0,.85) 45%,rgba(0,0,0,0) 100%)}"
       "body .reel .reel-track{z-index:1}"
       "body .reel .reel-slide .reel-count,body .reel .reel-slide .reel-mute{display:none!important}"
       "body .reel-gct,body .reel-gmu{position:absolute;top:calc(10px + env(safe-area-inset-top));right:12px;height:38px;min-width:38px;box-sizing:border-box;border-radius:999px;border:0;background:rgba(0,0,0,.45);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);color:#fff;display:flex;align-items:center;justify-content:center;z-index:7;-webkit-tap-highlight-color:transparent}"
       "body .reel-gct{padding:0 14px;font-size:14px;font-weight:700;line-height:1;pointer-events:none}body .reel-gmu{width:38px;cursor:pointer}"
       "body .reel-gct[hidden],body .reel-gmu[hidden]{display:none!important}"
       "body .reel .reel-x,body .reel .reel-hint{z-index:7}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
