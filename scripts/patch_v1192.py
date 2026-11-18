#!/usr/bin/env python3
"""Patch v1191 -> v1192: the scroller becomes the post viewer / lightbox for people's posts.
- Tapping a person's post card (its title, text, photo or video; not the name/tags row or the buttons) opens the
  scroller at that post. Tapping a video starts it with sound.
- Media posts show just the media, title, name and tags; if there's body text a "More" button opens it in the slide
  (the media shrinks), "Less" closes it. VIEW POST ↗ still opens the post page.
- Several photos: swipe left / right through them in the slide (1 / 3 counter); tap one for full screen.
- Videos autoplay (muted) when you reach them and pause when you move on.
- The "Swipe up · Tap to close" hint only shows on the first post; after that it's hidden (the end-of-list message
  still shows)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1191.js'
dst = '_deploy/assets/index-DUcNPOLc-v1192.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# open from people's cards
patch("function _reelOpen(card){try{", "function _reelOpen(card,o){o=o||{};try{", 'options')
patch("const startId=(()=>{try{return JSON.parse(card.dataset.lp).post}catch(e){return null}})();",
      "const startId=(()=>{try{return JSON.parse(card.dataset.lp||card.dataset.rp).post}catch(e){return null}})();", 'start from a person card')
patch("\"data-lp-id\":_rpOk?e.id:void 0,",
      "\"data-lp-id\":_rpOk?e.id:void 0,onClickCapture:_rpOk?_ev=>{const _t=_ev.target,_cd=_ev.currentTarget;if(!_t||!_t.closest||_t===_cd||_t.closest(`.feed-post-actions,.feed-post-board-row,.post-badges,[data-lp],.cu,.user-pill`))return;_ev.preventDefault();_ev.stopPropagation();_reelOpen(_cd,{sound:!0})}:void 0,", 'card taps open the scroller')
# slide: media-first layout, carousel, autoplay video
OLD_U = "if(d.kind===`u`){if((d.desc||``).length<=220)s.classList.add(`reel-big`);const med=inner.querySelector(`.reel-media`),im=med&&med.querySelector(`img`);if(med&&d.vid){const v=document.createElement(`video`);v.className=`reel-img reel-vid`;v.controls=!0;v.playsInline=!0;v.setAttribute(`playsinline`,``);v.preload=`none`;if(d.image)v.poster=d.image;v.src=d.vid;v.addEventListener(`click`,e=>e.stopPropagation());im&&im.remove();med.insertBefore(v,med.firstChild)}else if(im){im.classList.add(`reel-zoom`);im.addEventListener(`click`,e=>{e.stopPropagation();_photoView(d.full&&d.full.length?d.full:[d.image],0)})}}"
NEW_U = ("if(d.kind===`u`){const med=inner.querySelector(`.reel-media`),im=med&&med.querySelector(`img`),hasM=!!(med&&(d.vid||im));"
 "if(hasM)s.classList.add(`reel-big`,`reel-m`);else if((d.desc||``).length<=220)s.classList.add(`reel-big`);"
 "if(med&&d.vid){const v=document.createElement(`video`);v.className=`reel-img reel-vid`;v.controls=!0;v.playsInline=!0;v.setAttribute(`playsinline`,``);v.muted=!0;v.defaultMuted=!0;v.setAttribute(`muted`,``);v.loop=!0;v.preload=`metadata`;if(d.image)v.poster=d.image;v.src=d.vid;v.addEventListener(`click`,e=>e.stopPropagation());im&&im.remove();med.insertBefore(v,med.firstChild)}"
 "else if(im&&d.full&&d.full.length>1){const car=document.createElement(`div`);car.className=`reel-car`;d.full.forEach((u,k)=>{const ci=document.createElement(`img`);ci.className=`reel-img reel-zoom`;ci.alt=``;ci.decoding=`async`;ci.dataset.src=k===0&&d.image?d.image:u;ci.addEventListener(`click`,e=>{e.stopPropagation();_photoView(d.full,k)});car.appendChild(ci)});im.remove();med.insertBefore(car,med.firstChild);"
 "car.addEventListener(`scroll`,()=>{const k=Math.round(car.scrollLeft/Math.max(1,car.clientWidth)),ct=med.querySelector(`.reel-count`);if(ct)ct.textContent=`${k+1} / ${d.full.length}`},{passive:!0})}"
 "else if(im){im.classList.add(`reel-zoom`);im.addEventListener(`click`,e=>{e.stopPropagation();_photoView(d.full&&d.full.length?d.full:[d.image],0)})}"
 "if(hasM){s._fit=()=>{try{const md=s.querySelector(`.reel-media`),inn=s.querySelector(`.reel-inner`);if(!md||!inn||!s.clientHeight)return;const cs=getComputedStyle(s),Hh=s.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom);let other=0;for(const x of inn.children){if(x===md)continue;const st=getComputedStyle(x);if(st.display===`none`||st.position===`absolute`)continue;other+=x.offsetHeight+parseFloat(st.marginTop)+parseFloat(st.marginBottom)}other+=parseFloat(getComputedStyle(md).marginBottom)||0;const av=Math.max(140,Math.floor(Hh-other-2)),cr=md.querySelector(`.reel-car`);if(cr)cr.style.height=av+`px`;else md.querySelectorAll(`.reel-img`).forEach(x=>x.style.maxHeight=av+`px`)}catch(e){}};const fs=()=>requestAnimationFrame(()=>s._fit&&s._fit());med.querySelectorAll(`img`).forEach(x=>x.addEventListener(`load`,fs));const vv=med.querySelector(`video`);vv&&vv.addEventListener(`loadedmetadata`,fs)}}")
patch(OLD_U, NEW_U, 'media-first slide')
# More / Less for media posts with text
patch("if(d.kind===`u`){sn.textContent=`View post`;",
      "if(d.kind===`u`&&s.classList.contains(`reel-m`)&&d.desc){const mb=document.createElement(`button`);mb.type=`button`;mb.className=`reel-more`;mb.textContent=`More`;mb.addEventListener(`click`,e=>{e.stopPropagation();const on=s.classList.toggle(`reel-txt`);mb.textContent=on?`Less`:`More`;const ds=s.querySelector(`.reel-desc`);ds&&_reelFade(ds);s._fit&&s._fit()});inner.appendChild(mb)}\n"
      "  if(d.kind===`u`){sn.textContent=`View post`;", 'More button')
# load every carousel picture of nearby slides
patch("const im=slides[k]&&slides[k].querySelector(`img[data-src]`);if(im&&!im.src)im.src=im.dataset.src;",
      "slides[k]&&slides[k].querySelectorAll(`img[data-src]`).forEach(im=>{if(!im.src)im.src=im.dataset.src});slides[k]&&slides[k]._fit&&slides[k]._fit();", 'load carousel pictures')
patch("const rs=()=>place(0,!1);\n let sy=0,sx=0,st=0,dy=0,axis=null,moved=!1,txt=null;", "const rs=()=>{place(0,!1);slides.forEach(x=>x._fit&&x._fit())};\n let sy=0,sx=0,st=0,dy=0,axis=null,moved=!1,txt=null;", 'refit on resize')
# sideways swipes inside a carousel scroll it, not the scroller
patch("let sy=0,sx=0,st=0,dy=0,axis=null,moved=!1,txt=null;", "let sy=0,sx=0,st=0,dy=0,axis=null,moved=!1,txt=null,car=null;", 'car var')
patch("txt=(()=>{const d=e.target.closest&&e.target.closest(`.reel-desc`)", "car=e.target.closest&&e.target.closest(`.reel-car`);txt=(()=>{const d=e.target.closest&&e.target.closest(`.reel-desc`)", 'car at touchstart')
patch("if(axis===`text`)return;", "if(axis===`text`||(axis===`h`&&car))return;", 'car scrolls natively')
# hint only on the first post; autoplay the current video
patch("hint.className=`reel-hint`+(swiped?` small`:``)+(last&&ended?` end`:``);",
      "hint.className=`reel-hint`+(swiped?` small`:``)+(last&&ended?` end`:``);hint.style.display=swiped&&!(last&&ended)?`none`:``;"
      "try{const cv=slides[i]&&slides[i].querySelector(`video`);if(cv&&cv.paused&&!cv._ppUserPaused){const pr=cv.play();pr&&pr.catch(()=>{})}}catch(e){}", 'hint + autoplay')
patch("build();label();loadNear();\n history.pushState",
      "build();if(o.sound){try{const sv=slides[i]&&slides[i].querySelector(`video`);if(sv){sv.muted=!1;const pr=sv.play();pr&&pr.catch(()=>{sv.muted=!0;sv.play().catch(()=>{})})}}catch(e){}}label();loadNear();\n history.pushState", 'sound when opened from a video')
css = ("body .reel-m:not(.reel-txt) .reel-descw{display:none!important}"
       "body .reel-car{display:flex;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;scrollbar-width:none;overscroll-behavior-x:contain}"
       "body .reel-car::-webkit-scrollbar{display:none}"
       "body .reel .reel-car .reel-img{flex:0 0 100%;width:100%;scroll-snap-align:center;margin:0;border-radius:12px;aspect-ratio:auto!important;height:100%!important;max-height:none!important;object-fit:contain;background:none!important}"
       "body .reel .reel-m .reel-media{display:flex;justify-content:center;background:none}"
       "body .reel .reel-m .reel-media>.reel-img{width:auto!important;max-width:100%;height:auto!important;aspect-ratio:auto!important;object-fit:contain;background:none!important;border-radius:16px}"
       "body .reel .reel-m .reel-car{width:100%;background:none;height:52vh}"
       "body .reel-m.reel-txt .reel-descw{max-height:38vh}"
       "body .reel-more{align-self:flex-start;margin-top:8px;padding:4px 0;border:0;background:none;color:#94a3b8;font:inherit;font-size:13.5px;font-weight:700;cursor:pointer;flex-shrink:0}"
       "body .reel-m .reel-descw{margin-top:6px}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
