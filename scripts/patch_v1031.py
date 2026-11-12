#!/usr/bin/env python3
"""Patch v1030 -> v1031: Read more, and tags above the photo.
- Full-screen link posts show ~6 lines of description; when there's more, a "Read more" button appears. Tapping it
  smoothly expands the text (everything below slides down); "Show less" folds it back. If the opened post is taller
  than the screen it scrolls, and a swipe on it scrolls first, then changes post at the end.
- The tags sit above the photo at its top-left corner (mini outline pills in each tag's colour), not on the photo."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1030.js'
dst = '_deploy/assets/index-DUcNPOLc-v1031.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
# tags above the photo
patch("if(d.image){const med=document.createElement(`div`);med.className=`reel-media`;",
      "if((d.tags||[]).length){const tr=tagRow();tr.classList.add(`flat`);inner.appendChild(tr)}if(d.image){const med=document.createElement(`div`);med.className=`reel-media`;",
      'tags row first')
patch("if((d.tags||[]).length)med.appendChild(tagRow());inner.appendChild(med)}else if((d.tags||[]).length){const tr=tagRow();tr.classList.add(`flat`);inner.appendChild(tr)}",
      "inner.appendChild(med)}", 'no tags on the photo')
# Read more / Show less
patch("t.addEventListener(`scroll`,()=>_reelFade(t),{passive:!0});inner.appendChild(t)}",
      "inner.appendChild(t);const rm=document.createElement(`button`);rm.type=`button`;rm.className=`reel-more`;rm.textContent=`Read more`;rm.hidden=!0;"
      "rm.onclick=e=>{e.stopPropagation();_reelToggle(t,rm,inner)};inner.appendChild(rm)}", 'read more button')
patch("function _reelFade(d){d.classList.toggle(`more`,d.scrollTop+d.clientHeight<d.scrollHeight-2)}",
      "function _reelFade(d){const rm=d.nextElementSibling;if(!rm||!rm.classList.contains(`reel-more`)||d.classList.contains(`open`))return;rm.hidden=!(d.scrollHeight>d.clientHeight+2)}\n"
      "function _reelToggle(d,rm,inner){const open=!d.classList.contains(`open`);const h0=d.getBoundingClientRect().height;"
      "d.classList.toggle(`open`,open);inner.classList.toggle(`open`,open);const h1=open?d.scrollHeight:(()=>{d.style.height=``;return d.getBoundingClientRect().height})();"
      "rm.textContent=open?`Show less`:`Read more`;if(!open)inner.scrollTop=0;"
      "if(matchMedia(`(prefers-reduced-motion: reduce)`).matches)return;d.style.height=h0+`px`;d.style.overflow=`hidden`;void d.offsetHeight;d.style.transition=`height .32s cubic-bezier(.3,.7,.2,1)`;d.style.height=h1+`px`;"
      "setTimeout(()=>{d.style.transition=``;d.style.height=``;d.style.overflow=``},340)}",
      'expand / fold')
# swipes on an opened post that is taller than the screen scroll it first
patch("txt=(()=>{const d=e.target.closest&&e.target.closest(`.reel-desc`);return d&&d.scrollHeight>d.clientHeight+2?d:null})();",
      "txt=(()=>{const d=e.target.closest&&e.target.closest(`.reel-inner.open`);return d&&d.scrollHeight>d.clientHeight+2?d:null})();",
      'scroll the opened post first')
patch("if(e.target.closest(`.reel-btn`))return;close()", "if(e.target.closest(`.reel-btn,.reel-more`))return;close()", 'Read more does not close')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel-desc{display:-webkit-box!important;-webkit-line-clamp:6!important;-webkit-box-orient:vertical;overflow:hidden!important;touch-action:auto;-webkit-mask-image:none!important;mask-image:none!important;flex-shrink:0}
.reel-desc.open{display:block!important;-webkit-line-clamp:unset!important}
.reel-more{align-self:flex-start;margin-top:8px;padding:6px 14px;border-radius:999px;border:1.5px solid rgba(192,132,252,.5);background:rgba(192,132,252,.1);color:#c084fc;font-size:13px;font-weight:800;font-family:inherit;cursor:pointer;flex-shrink:0;-webkit-tap-highlight-color:transparent}
.reel-more[hidden]{display:none}
.reel-inner.open{overflow-y:auto;touch-action:pan-y;overscroll-behavior:contain;scrollbar-width:none;padding-bottom:4px}
.reel-inner.open::-webkit-scrollbar{display:none}
.reel-tags.flat{margin-bottom:10px}
.reel-tags.flat .reel-tag{background:transparent;-webkit-backdrop-filter:none;backdrop-filter:none}
.reel-slide.long .reel-img{max-height:42vh}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
