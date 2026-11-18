#!/usr/bin/env python3
"""Patch v1192 -> v1193 (scroller, people's media posts go full screen, TikTok style):
- The photo / video fills the whole slide. Tall ones fill edge to edge; wide ones sit centred on a blurred copy of
  themselves (no black bars).
- Name, tags, time, title, More and VIEW POST ↗ sit over the bottom on a dark fade; More opens the text there.
- Videos: tap to pause / play (no native control bar), a sound button top right; still autoplay muted as you reach
  them. Photos: tap for full-screen zoom. Several photos still swipe sideways.
- A ✕ button top left closes the scroller (tapping a full-screen photo / video no longer closes it)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1192.js'
dst = '_deploy/assets/index-DUcNPOLc-v1193.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
MUTED = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H3v6h3l5 4z"/><path d="m22 9-6 6M16 9l6 6"/></svg>'
SOUND = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H3v6h3l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/></svg>'
patch("if(hasM){s._fit=()=>{",
      "if(hasM){const bgu=d.image||(d.full&&d.full[0]);if(bgu){const bl=document.createElement(`img`);bl.className=`reel-blur`;bl.alt=``;bl.setAttribute(`aria-hidden`,`true`);bl.dataset.src=bgu;med.insertBefore(bl,med.firstChild)}"
      "const shape=x=>{const w=x.naturalWidth||x.videoWidth,h=x.naturalHeight||x.videoHeight;if(w&&h)x.classList.toggle(`reel-cover`,w/h<.8)};"
      "med.querySelectorAll(`img.reel-img,video`).forEach(x=>{x.addEventListener(`load`,()=>shape(x));x.addEventListener(`loadedmetadata`,()=>shape(x));shape(x)});"
      "const vv=med.querySelector(`video`);if(vv){vv.controls=!1;vv.addEventListener(`click`,e=>{e.stopPropagation();if(vv.paused){vv._ppUserPaused=!1;vv.play().catch(()=>{})}else{vv._ppUserPaused=!0;vv.pause()}s.classList.toggle(`reel-paused`,vv.paused)});"
      "vv.addEventListener(`play`,()=>s.classList.remove(`reel-paused`));vv.addEventListener(`pause`,()=>s.classList.add(`reel-paused`));"
      "const mu=document.createElement(`button`);mu.type=`button`;mu.className=`reel-mute`;const mup=()=>{mu.innerHTML=vv.muted?`" + MUTED + "`:`" + SOUND + "`;mu.setAttribute(`aria-label`,vv.muted?`Turn sound on`:`Mute`)};"
      "mu.addEventListener(`click`,e=>{e.stopPropagation();vv.muted=!vv.muted;if(!vv.muted&&vv.paused)vv.play().catch(()=>{});mup()});vv.addEventListener(`volumechange`,mup);mup();s.appendChild(mu);"
      "const pl=document.createElement(`span`);pl.className=`reel-playic`;pl.setAttribute(`aria-hidden`,`true`);s.appendChild(pl)}}"
      "if(hasM&&!1){s._fit=()=>{", 'full-screen media pieces')
patch("top.textContent=`Tap to close`;ov.appendChild(top);",
      "top.textContent=`Tap to close`;ov.appendChild(top);const xb=document.createElement(`button`);xb.type=`button`;xb.className=`reel-x`;xb.setAttribute(`aria-label`,`Close`);xb.innerHTML=`<svg viewBox=\"0 0 24 24\" width=\"18\" height=\"18\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.4\" stroke-linecap=\"round\"><path d=\"M6 6l12 12M18 6 6 18\"/></svg>`;xb.addEventListener(`click`,e=>{e.stopPropagation();close()});ov.appendChild(xb);", 'close button')
patch("tx.textContent=last&&ended?`You're all caught up`:last&&loading?`Loading more…`:`Swipe up for the next post · Tap to close`;",
      "tx.textContent=last&&ended?`You're all caught up`:last&&loading?`Loading more…`:slides[i]&&slides[i].classList.contains(`reel-m`)?`Swipe up for the next post`:`Swipe up for the next post · Tap to close`;", 'hint wording on full-screen slides')
css = ("body .reel-hint{text-shadow:0 1px 6px rgba(0,0,0,.7)}body .reel .reel-m .reel-inner{position:static;height:100%;max-height:100%;justify-content:flex-end;max-width:560px}"
       "body .reel .reel-m .reel-inner>:not(.reel-media){position:relative;z-index:2}"
       "body .reel .reel-m .reel-head.has-who{position:relative}"
       "body .reel .reel-m .reel-media{position:absolute!important;inset:0;margin:0!important;z-index:0;overflow:hidden;background:#000;display:block!important;width:auto}"
       "body .reel .reel-m .reel-media>.reel-img,body .reel .reel-m .reel-media>.reel-vid{position:absolute;inset:0;width:100%!important;height:100%!important;max-width:none!important;max-height:none!important;object-fit:contain;border-radius:0!important;background:none!important;z-index:1}"
       "body .reel .reel-m .reel-cover{object-fit:cover!important}"
       "body .reel-blur{position:absolute;inset:-60px;width:calc(100% + 120px);height:calc(100% + 120px);object-fit:cover;filter:blur(30px) brightness(.42);z-index:0;pointer-events:none}"
       "body .reel .reel-m .reel-car{position:absolute;inset:0;width:100%;height:100%!important;z-index:1}"
       "body .reel .reel-m .reel-car .reel-img{border-radius:0!important;height:100%!important;object-fit:contain}"
       "body .reel .reel-m .reel-car .reel-img.reel-cover{object-fit:cover!important}"
       "body .reel .reel-m::after{content:'';position:absolute;inset:0;pointer-events:none;z-index:1;background:linear-gradient(to top,rgba(0,0,0,.85) 0%,rgba(0,0,0,.6) 20%,rgba(0,0,0,0) 46%),linear-gradient(to bottom,rgba(0,0,0,.5),rgba(0,0,0,0) 14%)}"
       "body .reel .reel-m .reel-title{text-shadow:0 1px 10px rgba(0,0,0,.65)}"
       "body .reel .reel-m .reel-desc{color:#e2e8f0}"
       "body .reel .reel-m .reel-more{color:#e2e8f0}"
       "body .reel .reel-m .reel-count{position:absolute;top:calc(58px + env(safe-area-inset-top));right:14px;z-index:3}"
       "body .reel-x,body .reel-mute{position:absolute;top:calc(10px + env(safe-area-inset-top));width:38px;height:38px;border-radius:999px;border:0;background:rgba(0,0,0,.45);color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;-webkit-tap-highlight-color:transparent;-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}"
       "body .reel-x{left:12px;z-index:6}body .reel-mute{right:12px;z-index:4}"
       "body .reel-playic{position:absolute;left:50%;top:45%;width:72px;height:72px;margin:-36px 0 0 -36px;border-radius:999px;background:rgba(0,0,0,.45);z-index:3;pointer-events:none;opacity:0;transition:opacity .15s}"
       "body .reel-playic::before{content:'';position:absolute;left:29px;top:22px;border-style:solid;border-width:14px 0 14px 22px;border-color:transparent transparent transparent #fff}"
       "body .reel-paused .reel-playic{opacity:1}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
