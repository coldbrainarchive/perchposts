#!/usr/bin/env python3
"""Patch v1047 -> v1048: the full-screen link view's action bar becomes one dock that stays put while posts swipe
underneath it; its counts switch to whichever post you're on.
- Thinner pill (46px), "liquid glass" look: strong blur + saturation, light gradient, bright top edge, sheen.
- Each post still builds its own (now hidden) buttons; the dock mirrors the current post's buttons (MutationObserver)
  and its taps press them, so flaps/chat/share logic is unchanged.
- Counts do a small slide-in when the post changes.
- Share arrow has a shorter head."""
import sys, json
src = '_deploy/assets/index-DUcNPOLc-v1047.js'
dst = '_deploy/assets/index-DUcNPOLc-v1048.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('M7 17L17 7M8.5 7H17v8.5', 'M7 17L17 7M11 7h6v6', 'shorter arrow head')
# dock element
patch('ov.appendChild(hint);',
 'ov.appendChild(hint);'
 'const dock=document.createElement(`div`);dock.className=`reel-dock`;ov.appendChild(dock);let dockMo=null,dockPost=null;'
 'const dockBind=()=>{const s=slides[i];if(!s)return;const src=s.querySelector(`.reel-btns`);if(!src)return;const changed=dockPost!==s.dataset.post;dockPost=s.dataset.post;'
 'if(!dock.childElementCount){for(const b of src.children){const d=document.createElement(`button`);d.type=`button`;d.dataset.k=[...b.classList].find(x=>/^reel-(flap|chat|share)$/.test(x))||``;d.className=`reel-dbtn `+d.dataset.k;'
 'd.setAttribute(`aria-label`,b.getAttribute(`aria-label`)||``);d.addEventListener(`click`,e=>{e.stopPropagation();const t=slides[i]&&slides[i].querySelector(`.reel-btns .`+d.dataset.k);t&&t.click()});dock.appendChild(d)}}'
 'const mirror=()=>{for(const d of dock.children){const b=src.querySelector(`.`+d.dataset.k);if(!b)continue;d.hidden=b.hidden;d.classList.toggle(`on`,b.classList.contains(`on`));d.classList.toggle(`done`,b.classList.contains(`done`));'
 'const bi=b.querySelector(`.i`),bn=b.querySelector(`.n`);'
 'if(d.dataset.k===`reel-share`){if(d.innerHTML!==b.innerHTML)d.innerHTML=b.innerHTML}else{if(!d.querySelector(`.i`)){d.innerHTML=`<span class="i"></span><span class="n"></span>`;d.querySelector(`.i`).innerHTML=bi?bi.innerHTML:``}d.querySelector(`.n`).textContent=bn?bn.textContent:``}}};'
 'mirror();if(changed){dock.classList.remove(`swap`);void dock.offsetWidth;dock.classList.add(`swap`)}'
 'dockMo&&dockMo.disconnect();dockMo=new MutationObserver(mirror);dockMo.observe(src,{subtree:!0,childList:!0,characterData:!0,attributes:!0,attributeFilter:[`class`,`hidden`]})};',
 'dock')
patch('const label=()=>{const last=i>=items.length-1;', 'const label=()=>{try{dockBind()}catch(e){}const last=i>=items.length-1;', 'rebind dock on post change')
# wing beat on the dock's bird too
patch('if(!wasOn)_ppFlapAnim(fb);', 'if(!wasOn){_ppFlapAnim(fb);_ppFlapAnim(dock)}', 'dock wing beat')
patch('if(e.target.closest(`.reel-btn,.reel-site,.reel-btns`))return;close()', 'if(e.target.closest(`.reel-btn,.reel-site,.reel-btns,.reel-dock`))return;close()', 'dock taps do not close')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel .reel-slide .reel-btns{display:none!important}
.reel .reel-slide{padding-bottom:calc(100px + env(safe-area-inset-bottom))}
.reel-dock{position:absolute;z-index:3;left:50%;transform:translateX(-50%);bottom:calc(36px + env(safe-area-inset-bottom));width:min(calc(100% - 56px),400px);height:46px;box-sizing:border-box;padding:0 4px;display:flex;align-items:stretch;border-radius:999px;overflow:hidden;
 background:linear-gradient(180deg,rgba(255,255,255,.14),rgba(255,255,255,.03) 55%,rgba(255,255,255,.07)),rgba(16,19,26,.5);
 -webkit-backdrop-filter:blur(16px) saturate(1.9) brightness(1.08);backdrop-filter:blur(16px) saturate(1.9) brightness(1.08);
 border:1px solid rgba(255,255,255,.16);
 box-shadow:inset 0 1px 0 rgba(255,255,255,.32),inset 0 -1px 0 rgba(255,255,255,.06),inset 0 0 18px rgba(255,255,255,.04),0 8px 28px rgba(0,0,0,.45)}
.reel-dock::before{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;background:radial-gradient(120% 90% at 18% -20%,rgba(255,255,255,.22),transparent 45%),radial-gradient(90% 80% at 100% 130%,rgba(192,132,252,.12),transparent 60%)}
.reel-dbtn{position:relative;flex:1 1 0;display:inline-flex;align-items:center;justify-content:center;gap:7px;background:transparent;border:0;margin:0;padding:0;color:#e2e8f0;font-family:inherit;font-weight:700;font-size:14px;line-height:1;cursor:pointer;-webkit-tap-highlight-color:transparent;border-radius:999px;transition:color .15s,background .15s}
.reel-dbtn[hidden]{display:none}
.reel-dbtn:active{background:rgba(255,255,255,.08)}
.reel-dbtn + .reel-dbtn::before{content:"";position:absolute;left:0;top:14px;bottom:14px;width:1px;background:rgba(255,255,255,.12)}
.reel-dbtn .i{display:inline-flex}
.reel-dbtn .ri{display:block}
.reel-dbtn.reel-flap .ri{width:22px;height:22px;stroke-width:2.1}
.reel-dbtn.reel-chat .ri{width:17px;height:17px}
.reel-dbtn.reel-share{gap:6px}
.reel-dbtn.reel-share .ri{width:12px;height:12px}
.reel .reel-dock .reel-dbtn.on{color:#c084fc;background:transparent;border:0}
.reel .reel-dock .reel-dbtn.on:active{background:rgba(255,255,255,.08)}
.reel-dbtn.on .ri{filter:drop-shadow(0 0 6px rgba(192,132,252,.75))}
.reel-dbtn.on .n{color:#ede9fe}
.reel-dbtn.done{color:#c084fc}
.reel-dock.swap .n{animation:reelNum .28s cubic-bezier(.2,.8,.2,1)}
@keyframes reelNum{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.reel-dock{background:rgba(30,35,46,.92)}}
@media (prefers-reduced-motion: reduce){.reel-dock.swap .n{animation:none}}
.reel .reel-hint{bottom:calc(12px + env(safe-area-inset-bottom))}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
