#!/usr/bin/env python3
"""Patch v1029 -> v1030: full-screen link posts show the whole description and the post's tags.
- Description is no longer cut off: long ones scroll inside the text area (soft fade at the bottom when there's
  more). A swipe that starts on the text scrolls it first; at the end of the text the next swipe changes post.
  Very long descriptions get a slightly smaller photo.
- The post's tags (board, country…) sit in the photo's top-left corner as mini outline pills in each tag's own
  colour (above the title when there's no photo)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1029.js'
dst = '_deploy/assets/index-DUcNPOLc-v1030.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# tags read off the card when collecting
patch("if(!d||!d.post||seen.has(d.post))continue;seen.add(d.post);out.push(d)}return out}",
      "if(!d||!d.post||seen.has(d.post))continue;seen.add(d.post);d.tags=_reelTags(el);out.push(d)}return out}",
      'collect tags')
# slide: tags over the photo, full description
patch("if(d.image){const im=document.createElement(`img`);im.className=`reel-img`;im.alt=``;im.decoding=`async`;im.dataset.src=d.image;im.onerror=()=>im.remove();inner.appendChild(im)}",
      "const tagRow=()=>{const tr=document.createElement(`div`);tr.className=`reel-tags`;for(const g of d.tags||[]){const sp=document.createElement(`span`);sp.className=`reel-tag`;sp.textContent=g.t;sp.style.color=g.c;sp.style.borderColor=g.c;tr.appendChild(sp)}return tr};"
      "if((d.desc||``).length>400)s.classList.add(`long`);"
      "if(d.image){const med=document.createElement(`div`);med.className=`reel-media`;const im=document.createElement(`img`);im.className=`reel-img`;im.alt=``;im.decoding=`async`;im.dataset.src=d.image;im.onerror=()=>{im.remove();med.classList.add(`noimg`)};med.appendChild(im);if((d.tags||[]).length)med.appendChild(tagRow());inner.appendChild(med)}"
      "else if((d.tags||[]).length){const tr=tagRow();tr.classList.add(`flat`);inner.appendChild(tr)}",
      'tags over the photo')
patch("if(d.desc){const t=document.createElement(`div`);t.className=`reel-desc`;t.textContent=d.desc;inner.appendChild(t)}",
      "if(d.desc){const t=document.createElement(`div`);t.className=`reel-desc`;t.textContent=d.desc;t.addEventListener(`scroll`,()=>_reelFade(t),{passive:!0});inner.appendChild(t)}",
      'full description')
patch("const loadNear=()=>{[i-1,i,i+1,i+2].forEach(k=>{const im=slides[k]&&slides[k].querySelector(`img[data-src]`);if(im&&!im.src)im.src=im.dataset.src})};",
      "const loadNear=()=>{[i-1,i,i+1,i+2].forEach(k=>{const im=slides[k]&&slides[k].querySelector(`img[data-src]`);if(im&&!im.src)im.src=im.dataset.src;const ds=slides[k]&&slides[k].querySelector(`.reel-desc`);ds&&_reelFade(ds)})};",
      'fade when there is more text')
# swipes that start on scrollable text scroll the text first
patch("body.overflow=`hidden`;document.body.appendChild(ov);place(0,!1);requestAnimationFrame(()=>requestAnimationFrame(()=>ov.classList.add(`in`)));\n if(i>=items.length-2)more();",
      "body.overflow=`hidden`;document.body.appendChild(ov);place(0,!1);requestAnimationFrame(()=>requestAnimationFrame(()=>{ov.classList.add(`in`);loadNear()}));\n if(i>=items.length-2)more();",
      'check the fade once on screen')
patch("let sy=0,sx=0,st=0,dy=0,axis=null,moved=!1;", "let sy=0,sx=0,st=0,dy=0,axis=null,moved=!1,txt=null;", 'text scroll state')
patch("ov.addEventListener(`touchstart`,e=>{if(e.touches.length>1)return;sy=e.touches[0].clientY;sx=e.touches[0].clientX;st=Date.now();dy=0;axis=null;moved=!1;",
      "ov.addEventListener(`touchstart`,e=>{if(e.touches.length>1)return;sy=e.touches[0].clientY;sx=e.touches[0].clientX;st=Date.now();dy=0;axis=null;moved=!1;txt=(()=>{const d=e.target.closest&&e.target.closest(`.reel-desc`);return d&&d.scrollHeight>d.clientHeight+2?d:null})();",
      'touch starts on text?')
patch("if(!axis&&Math.hypot(x-sx,(y-sy))>8){axis=Math.abs(dy)>Math.abs(x-sx)?`v`:`h`;moved=!0}\n  if(axis===`v`)",
      "if(!axis&&Math.hypot(x-sx,(y-sy))>8){axis=Math.abs(dy)>Math.abs(x-sx)?`v`:`h`;moved=!0;"
      "if(axis===`v`&&txt&&(dy<0?txt.scrollTop+txt.clientHeight<txt.scrollHeight-1:txt.scrollTop>0))axis=`text`}\n  if(axis===`text`)return;\n  if(axis===`v`)",
      'scroll the text first')
c += r'''
function _reelTags(el){try{const card=el.closest(`.feed-post-card`);if(!card)return[];const out=[];
 for(const x of card.querySelectorAll(`span`)){if(out.length>=3)break;if(x.closest(`[data-lp]`)||x.closest(`.feed-post-actions`)||x.closest(`.user-pill`))continue;
  const cs=getComputedStyle(x),bg=cs.backgroundColor;if(!bg||bg===`rgba(0, 0, 0, 0)`||bg===`transparent`||cs.borderRadius===`0px`)continue;
  const r=x.getBoundingClientRect();if(r.height<12||r.height>40||r.width>220)continue;const t=x.textContent.trim();if(!t||t.length>28)continue;
  if(out.some(o=>o.t===t))continue;out.push({t,c:bg})}return out}catch(e){return[]}}
function _reelFade(d){d.classList.toggle(`more`,d.scrollTop+d.clientHeight<d.scrollHeight-2)}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel-desc{display:block!important;-webkit-line-clamp:unset!important;overflow-y:auto!important;flex:0 1 auto;min-height:0;touch-action:pan-y;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.reel-desc::-webkit-scrollbar{display:none}
.reel-desc.more{-webkit-mask-image:linear-gradient(#000 78%,transparent);mask-image:linear-gradient(#000 78%,transparent)}
.reel-title{-webkit-line-clamp:5!important}
.reel-media{position:relative;flex-shrink:0;margin-bottom:18px}
.reel-media .reel-img{margin-bottom:0}
.reel-media.noimg{min-height:0}
.reel-slide.long .reel-img{max-height:30vh}
.reel-tags{display:flex;flex-wrap:wrap;gap:6px}
.reel-media .reel-tags{position:absolute;top:10px;left:10px;right:10px}
.reel-tags.flat{margin-bottom:12px}
.reel-tag{display:inline-flex;align-items:center;gap:3px;height:20px;padding:0 8px;border-radius:999px;border:1.5px solid;background:rgba(11,12,16,.62);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);font-size:10px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap;line-height:1}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
