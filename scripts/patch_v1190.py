#!/usr/bin/env python3
"""Patch v1189 -> v1190: the link-preview scroller also includes people's posts, in feed order.
A person's slide: their name pill + tags at the top, the photo if any, the title and text, and a big "View chirps"
button (opens the post's chat). The flap / chirps / share dock works the same. Huddles are left out.
Each person's post card carries data-rp (its title / text / picture) and data-lp-id (so the dock finds its buttons)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1189.js'
dst = '_deploy/assets/index-DUcNPOLc-v1190.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# person's card carries its data
patch("return(0,L.jsxs)(`div`,{className:`content-card feed-post-card`,style:{marginBottom:16},onClick:_ce=>{",
      "const _rpOk=!(e.browser_id&&String(e.browser_id).startsWith(`bot-`))&&!fr.includes(e.username)&&!!e.username;"
      "return(0,L.jsxs)(`div`,{className:`content-card feed-post-card`,\"data-rp\":_rpOk?JSON.stringify({post:e.id,title:e.title||``,desc:(f||``).trim(),image:_pAtts&&_pAtts[0]?_mtPrev(_pAtts[0]):p?.type===`image`?_mtThumbOf(p):p?.type===`video`?p.poster||null:null,n:_pAtts?_pAtts.length:0}):void 0,\"data-lp-id\":_rpOk?e.id:void 0,style:{marginBottom:16},onClick:_ce=>{",
      'card data')
# collect both kinds, in page order
patch("""function _reelCollect(){const seen=new Set(),out=[];
 for(const el of document.querySelectorAll(`[data-lp]`)){if(!el.getClientRects().length)continue;let d;try{d=JSON.parse(el.dataset.lp)}catch(e){continue}""",
      """function _reelCollect(){const seen=new Set(),out=[];
 for(const el of document.querySelectorAll(`[data-lp],[data-rp]`)){if(!el.getClientRects().length)continue;let d;
  if(el.dataset.rp!==void 0){if(el.querySelector(`[data-lp]`))continue;try{d=JSON.parse(el.dataset.rp)}catch(e){continue}d.kind=`u`;const up=el.querySelector(`.user-pill`);d.pill=up?up.outerHTML:``}
  else{try{d=JSON.parse(el.dataset.lp)}catch(e){continue}const cd=el.closest(`.feed-post-card`),up=cd&&cd.querySelector(`.feed-post-board-row .user-pill`);if(up)d.pill=up.outerHTML}""", 'collect people posts')
# a person's slide
patch("  if(d.title){const t=document.createElement(`div`);t.className=`reel-title`;t.textContent=d.title;inner.appendChild(t)}",
      "  if(d.kind===`u`||d.pill){if(d.kind===`u`)s.classList.add(`reel-u`);const hd=inner.querySelector(`.reel-head`)||(()=>{const h=document.createElement(`div`);h.className=`reel-head`;inner.insertBefore(h,inner.firstChild);return h})();if(d.pill){const pw=document.createElement(`span`);pw.className=`reel-who`;pw.innerHTML=d.pill;hd.insertBefore(pw,hd.firstChild)}if(d.n>1){const med=inner.querySelector(`.reel-media`);if(med){const ct=document.createElement(`span`);ct.className=`reel-count`;ct.textContent=`1 / ${d.n}`;med.appendChild(ct)}}}\n"
      "  if(d.title){const t=document.createElement(`div`);t.className=`reel-title`;t.textContent=d.title;inner.appendChild(t)}", 'person slide head')
patch("  const site=document.createElement(`a`);site.className=`reel-site`;site.href=d.url;",
      "  if(d.kind===`u`){const vc=document.createElement(`button`);vc.type=`button`;vc.className=`reel-viewchirps`;vc.innerHTML=_ppIco(`CHAT`)+`<span>View chirps</span>`;vc.onclick=e=>{e.stopPropagation();goChat(d.post)};inner.appendChild(vc)}\n"
      "  const site=document.createElement(`a`);site.className=`reel-site`;if(d.kind===`u`)site.style.display=`none`;site.href=d.url;", 'view chirps button')
patch("ov.setAttribute(`aria-label`,`Link posts`);", "ov.setAttribute(`aria-label`,`Posts`);", 'label')
css = ("body .reel-who{display:inline-flex;flex-shrink:0}body .reel-who .user-pill{height:22px}"
       "body .reel-u .reel-head{flex-wrap:wrap;row-gap:6px}"
       "body .reel-u .reel-title{margin-top:2px}"
       "body .reel-u:not(:has(.reel-media)) .reel-title{font-size:24px}"
       "body .reel-u:not(:has(.reel-media)) .reel-desc{font-size:17px;color:#cbd5e1}"
       "body .reel-count{position:absolute;top:10px;right:10px;padding:3px 9px;border-radius:999px;background:rgba(0,0,0,.6);color:#fff;font-size:12px;font-weight:700}"
       "body .reel-viewchirps{display:inline-flex;align-items:center;justify-content:center;gap:8px;align-self:flex-start;margin-top:16px;height:40px;padding:0 18px;border-radius:999px;border:1px solid rgba(192,132,252,.5);background:rgba(192,132,252,.14);color:#e9d5ff;font:inherit;font-size:14.5px;font-weight:800;cursor:pointer;flex-shrink:0}"
       "body .reel-viewchirps svg{width:17px!important;height:17px!important}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
