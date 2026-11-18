#!/usr/bin/env python3
"""Patch v1190 -> v1191 (scroller, people's posts - preview round 2):
- Name: an outlined pill in the person's colour (bird + name), like the tags. Tags sit beside it when they fit; if
  not, the whole tag group drops to the line under the name. The time stays top right.
- "View chirps" button replaced by "VIEW POST ↗" styled like the article link; it opens the post page.
- Media: big when the post has little text (fills most of the slide); with a lot of text it stays smaller.
  Tap a photo to see it full screen (all its photos); videos play right in the slide (paused when you swipe on)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1190.js'
dst = '_deploy/assets/index-DUcNPOLc-v1191.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# card: video + full photo urls
patch(",n:_pAtts?_pAtts.length:0}):void 0,",
      ",n:_pAtts?_pAtts.length:0,vid:p?.type===`video`?p.url||null:null,full:_pAtts?_pAtts.map(_a=>_a&&_a.url).filter(Boolean):p?.type===`image`&&p.url?[p.url]:[]}):void 0,", 'card media data')
# collect: who = colour + bird + name
patch("d.kind=`u`;const up=el.querySelector(`.user-pill`);d.pill=up?up.outerHTML:``}",
      "d.kind=`u`;d.who=_reelWho(el.querySelector(`.feed-post-board-row .user-pill`))}", 'who (people)')
patch("const cd=el.closest(`.feed-post-card`),up=cd&&cd.querySelector(`.feed-post-board-row .user-pill`);if(up)d.pill=up.outerHTML}",
      "const cd=el.closest(`.feed-post-card`);d.who=_reelWho(cd&&cd.querySelector(`.feed-post-board-row .user-pill`))}", 'who (link posts)')
patch("function _reelCollect(){",
      "function _reelWho(up){try{if(!up)return null;const nm=up.querySelector(`.user-pill-name`),bd=up.querySelector(`.user-pill-badge`);return{c:getComputedStyle(up).backgroundColor,n:(nm?nm.textContent:up.textContent).trim(),ic:bd?bd.outerHTML:``}}catch(e){return null}}\nfunction _reelCollect(){", 'who helper')
# slide head + media
patch("if(d.kind===`u`||d.pill){if(d.kind===`u`)s.classList.add(`reel-u`);const hd=",
      "if(d.kind===`u`||d.who){if(d.kind===`u`)s.classList.add(`reel-u`);const hd=", 'head condition')
patch("if(d.pill){const pw=document.createElement(`span`);pw.className=`reel-who`;pw.innerHTML=d.pill;hd.insertBefore(pw,hd.firstChild)}",
      "if(d.who){hd.classList.add(`has-who`);const w=document.createElement(`span`);w.className=`reel-tag reel-whotag`;w.style.color=d.who.c;w.style.borderColor=d.who.c;w.innerHTML=d.who.ic||``;w.append(d.who.n);hd.insertBefore(w,hd.firstChild)}"
      "if(d.kind===`u`){if((d.desc||``).length<=220)s.classList.add(`reel-big`);const med=inner.querySelector(`.reel-media`),im=med&&med.querySelector(`img`);"
      "if(med&&d.vid){const v=document.createElement(`video`);v.className=`reel-img reel-vid`;v.controls=!0;v.playsInline=!0;v.setAttribute(`playsinline`,``);v.preload=`none`;if(d.image)v.poster=d.image;v.src=d.vid;v.addEventListener(`click`,e=>e.stopPropagation());im&&im.remove();med.insertBefore(v,med.firstChild)}"
      "else if(im){im.classList.add(`reel-zoom`);im.addEventListener(`click`,e=>{e.stopPropagation();_photoView(d.full&&d.full.length?d.full:[d.image],0)})}}", 'who pill + media')
# View post link instead of View chirps
patch("  if(d.kind===`u`){const vc=document.createElement(`button`);vc.type=`button`;vc.className=`reel-viewchirps`;vc.innerHTML=_ppIco(`CHAT`)+`<span>View chirps</span>`;vc.onclick=e=>{e.stopPropagation();goChat(d.post)};inner.appendChild(vc)}\n", "", 'no View chirps button')
patch("if(d.kind===`u`)site.style.display=`none`;", "", 'site link stays')
patch("site.addEventListener(`click`,e=>e.stopPropagation());inner.appendChild(site);",
      "if(d.kind===`u`){sn.textContent=`View post`;site.href=`/post/${d.post}`;site.removeAttribute(`target`);site.removeAttribute(`rel`);site.addEventListener(`click`,e=>{e.preventDefault();e.stopPropagation();goPost(d.post)})}else site.addEventListener(`click`,e=>e.stopPropagation());inner.appendChild(site);", 'View post link')
# pause videos on other slides
patch("const label=()=>{try{dockBind()}catch(e){}", "const label=()=>{try{dockBind()}catch(e){}try{track.querySelectorAll(`video`).forEach(v=>{if(!slides[i]||!slides[i].contains(v))v.pause()})}catch(e){}", 'pause off-screen videos')
patch("const key=e=>{if(e.key===`Escape`){e.preventDefault();e.stopPropagation();close()}else if(e.key===`ArrowDown`",
      "const key=e=>{if(document.querySelector(`.pv`))return;if(e.key===`Escape`){e.preventDefault();e.stopPropagation();close()}else if(e.key===`ArrowDown`", 'photo viewer keeps its keys')
patch("else if(pendingPost){const t=document.querySelector(`[data-lp-id=\"${CSS.escape(pendingPost)}\"]`);if(t){window._reelBypass=!0;t.click()}else location.href=`/post/${pendingPost}`}",
      "else if(pendingPost){const t=document.querySelector(`[data-lp-id=\"${CSS.escape(pendingPost)}\"]`);if(t&&!t.classList.contains(`feed-post-card`)){window._reelBypass=!0;t.click()}else{try{history.pushState({},``,`/post/${pendingPost}`);dispatchEvent(new PopStateEvent(`popstate`,{state:{}}))}catch(e){location.href=`/post/${pendingPost}`}}}", 'View post opens the post')
css = ("body .reel-head.has-who{position:relative;flex-wrap:wrap;gap:6px;padding-right:50px}"
       "body .reel-head.has-who .reel-tags.flat{flex:0 1 auto;min-width:0}"
       "body .reel-head.has-who .reel-time{position:absolute;right:0;top:0}"
       "body .reel-whotag{gap:4px!important;text-transform:none!important;letter-spacing:.01em!important;font-size:11px!important;padding-left:5px!important}"
       "body .reel-whotag .user-pill-badge{width:15px!important;height:15px!important}"
       "body .reel-big .reel-media .reel-img{aspect-ratio:auto!important;height:auto;max-height:58vh;object-fit:contain;background:#000}"
       "body .reel-vid{width:100%;max-height:42vh;border-radius:16px;background:#000;display:block;aspect-ratio:auto!important}"
       "body .reel-big .reel-vid{max-height:58vh}"
       "body .reel-zoom{cursor:zoom-in}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
