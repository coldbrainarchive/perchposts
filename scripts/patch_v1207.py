#!/usr/bin/env python3
"""Patch v1206 -> v1207 : on photo / video slides the flaps / chirps / share bar grows into a panel that
holds the name + tags + time, the title and VIEW POST ↗ above the buttons. Swiping onto a media post the panel opens
out of the bar; on text / link posts it folds back to the plain bar. The slide itself shows only the media."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1206.js'
dst = '_deploy/assets/index-DUcNPOLc-v1207.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("const dock=document.createElement(`div`);dock.className=`reel-dock`;ov.appendChild(dock);",
      "const dock=document.createElement(`div`);dock.className=`reel-dock`;const rpan=document.createElement(`div`);rpan.className=`reel-panel`;const rpw=document.createElement(`div`);rpw.className=`reel-pinfo-w`;const rpi=document.createElement(`div`);rpi.className=`reel-pinfo`;rpw.appendChild(rpi);rpan.append(rpw,dock);ov.appendChild(rpan);"
      "rpi.addEventListener(`click`,e=>{const a=e.target.closest&&e.target.closest(`.reel-site`);if(!a)return;e.preventDefault();e.stopPropagation();const o2=slides[i]&&slides[i].querySelector(`a.reel-site`);o2&&o2.click()});"
      "let rpCur=null;const panelSync=()=>{const s=slides[i];if(!s)return;const m=s.classList.contains(`reel-m`);if(!m){rpan.classList.remove(`open`);rpCur=null;return}if(rpCur===s.dataset.post){rpan.classList.add(`open`);return}rpCur=s.dataset.post;"
      "const box=document.createElement(`div`);box.className=`reel-pinfo-in`;[`.reel-head`,`.reel-title`,`a.reel-site`].forEach(q=>{const x=s.querySelector(q);if(!x)return;const k=x.cloneNode(!0);if(!k.classList.contains(`reel-head`))k.removeAttribute(`style`);box.appendChild(k)});rpi.replaceChildren(box);requestAnimationFrame(()=>rpan.classList.add(`open`))};", 'panel around the bar')
patch("const label=()=>{try{dockBind()}catch(e){}", "const label=()=>{try{dockBind()}catch(e){}try{panelSync()}catch(e){}", 'sync panel per slide')
css = ("body .reel .reel-m .reel-inner>:not(.reel-media){display:none!important}"
       "body .reel-panel{position:absolute;left:50%;transform:translateX(-50%);bottom:calc(28px + env(safe-area-inset-bottom));width:min(calc(100% - 32px),520px);z-index:7;box-sizing:border-box;border:1.5px solid #94a3b8;border-radius:17px;background:rgba(11,12,16,.62);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);overflow:hidden}"
       "body .reel .reel-panel .reel-dock{position:static!important;transform:none!important;left:auto!important;bottom:auto!important;width:100%!important;border:0!important;border-radius:0!important;background:transparent!important;-webkit-backdrop-filter:none!important;backdrop-filter:none!important;box-shadow:none!important}"
       "body .reel-pinfo-w{display:grid;grid-template-rows:0fr;transition:grid-template-rows .34s cubic-bezier(.22,.8,.24,1)}"
       "body .reel-panel.open .reel-pinfo-w{grid-template-rows:1fr}"
       "body .reel-pinfo{overflow:hidden;min-height:0}"
       "body .reel-pinfo-in{padding:14px 14px 13px;border-bottom:1px solid rgba(148,163,184,.3);animation:rpIn .28s ease-out}"
       "@keyframes rpIn{from{opacity:0}to{opacity:1}}"
       "body .reel-pinfo-in .reel-head{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px;position:relative;padding-right:50px}"
       "body .reel-pinfo-in .reel-head .reel-tags.flat{flex:0 1 auto;min-width:0;margin:0}"
       "body .reel-pinfo-in .reel-head .reel-time{position:absolute;right:0;top:0}"
       "body .reel-pinfo-in .reel-title{color:#f1f5f9;font-size:20px;font-weight:800;line-height:1.25;margin:0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;text-align:left}"
       "body .reel-pinfo-in a.reel-site{display:inline-flex;align-items:center;gap:5px;margin-top:10px;color:#c084fc;font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.04em;text-decoration:none}"
       "@media (prefers-reduced-motion: reduce){body .reel-pinfo-w{transition:none}body .reel-pinfo-in{animation:none}}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
