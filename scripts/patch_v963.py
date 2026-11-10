#!/usr/bin/env python3
"""Patch v962 -> v963: emoji picker fixes + full-screen react view.
1. The "↓ N new" pill sits under sheets (emoji picker, who-reacted, Bird card) instead of on top of them.
2. Safari freeze after typing in "Search Emoji" and closing the keyboard: the chat's own keyboard handling
   no longer reacts to the picker's search box (focus events stop at the picker, and its "keyboard open"
   mode ignores focus inside the picker); the picker is sized to the visible screen (visual viewport
   top + height) at all times, and any scroll Safari leaves behind is reset when the keyboard closes.
3. React opens full screen like iMessage: the chat dims and blurs, a copy of the chirp you're reacting
   to sits above the emoji keyboard (long text clamped, photos shortened). Tap the dim area to close."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v962.js'
dst = '_deploy/assets/index-DUcNPOLc-v963.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# Chat keyboard mode ignores the picker's search box
patch('_h.classList.toggle(`chat-kb`,/^(TEXTAREA|INPUT)$/.test(document.activeElement?.tagName||``))',
      '_h.classList.toggle(`chat-kb`,/^(TEXTAREA|INPUT)$/.test(document.activeElement?.tagName||``)&&!document.activeElement.closest(`.ri-ov`))',
      'chat-kb ignores picker')

# React: grab the chirp before the menu closes, pass a copy to the picker
patch('function _rxOpen(id,react,E,me,close){close();',
      'function _rxOpen(id,react,E,me,close){const _src=_rxSrc(id);close();', 'find chirp')
patch('\n _rxIos(q=>{if((E[q]||[]).includes(me))return;react(id,q);_rxPop(id,q,null)})}',
      '\n _rxIos(q=>{if((E[q]||[]).includes(me))return;react(id,q);_rxPop(id,q,null)},_src)}', 'pass chirp')
patch('function _rxIos(cb){', 'function _rxIos(cb,_src){', 'picker takes chirp')

# Picker sized to the visible screen; focus stays inside; reset Safari scroll when the keyboard closes
patch('const vv=window.visualViewport,fit=()=>{if(!vv)return;ov.style.bottom=Math.max(0,window.innerHeight-vv.height-vv.offsetTop)+`px`};',
      'const vv=window.visualViewport,fit=()=>{if(!vv)return;ov.style.top=vv.offsetTop+`px`;ov.style.height=vv.height+`px`;ov.style.bottom=`auto`};',
      'fit to visual viewport')
patch('let shut=!1,all=null,secs=[];',
      'let shut=!1,all=null,secs=[];'
      'const top=document.createElement(`div`);top.className=`ri-top`;ov.insertBefore(top,sh);'
      'if(_src){const k=_src.cloneNode(!0);k.querySelectorAll(`.chat-action-sheet,.rx-who,.chat-emoji-picker-row,.rx-more,.pin-more`).forEach(x=>x.remove());'
      'k.querySelectorAll(`[id]`).forEach(x=>x.removeAttribute(`id`));const wr=document.createElement(`div`);wr.className=`ri-chirp`;'
      'wr.style.width=Math.min(_src.getBoundingClientRect().width||320,window.innerWidth-32)+`px`;wr.append(k);top.append(wr)}'
      'ov.addEventListener(`focusin`,e=>e.stopPropagation());'
      'ov.addEventListener(`focusout`,e=>{e.stopPropagation();[60,320].forEach(d=>setTimeout(()=>{if(shut)return;if(window.scrollY||document.documentElement.scrollTop)window.scrollTo(0,0);fit()},d))});',
      'chirp copy + focus isolation')
patch('ov.addEventListener(`click`,e=>{if(e.target===ov)close()});',
      'ov.addEventListener(`click`,e=>{if(e.target===ov||e.target.closest(`.ri-top`))close()});', 'tap dim area closes')

c += r'''
function _rxSrc(id){const q=CSS.escape(String(id));const els=[...document.querySelectorAll(`.chat-msg[data-comment-id="${q}"] .chat-msg-body, .chat-msg[data-pin-of="${q}"] .chat-msg-body`)];
 const vis=els.find(e=>{const r=e.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight&&r.width>0});return vis||els[0]||null}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.rd-pill{z-index:900!important}
.ri-ov{flex-direction:column;align-items:stretch;justify-content:flex-end}
.ri-ov.in{background:rgba(6,7,10,.78);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.ri-ov .ri-sheet{align-self:center;flex-shrink:0}
.ri-top{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:flex-end;align-items:flex-start;padding:16px 16px 14px;box-sizing:border-box;overflow:hidden;width:100%;max-width:520px;align-self:center}
.ri-chirp{max-width:100%;max-height:100%;overflow:hidden;pointer-events:none;opacity:0;transform:translateY(10px) scale(.97);transition:opacity .22s,transform .26s cubic-bezier(.2,.8,.3,1)}
.ri-ov.in .ri-chirp{opacity:1;transform:none}
.ri-chirp>.chat-msg-body{box-shadow:0 10px 34px rgba(0,0,0,.55)}
.ri-chirp .chat-msg-body{width:100%!important;max-width:100%!important}
.ri-chirp .chat-bubble-text{display:-webkit-box;-webkit-line-clamp:6;-webkit-box-orient:vertical;overflow:hidden}
.ri-chirp img,.ri-chirp video{max-height:150px!important;object-fit:cover}
@media (prefers-reduced-motion: reduce){.ri-chirp{transition:none}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
