#!/usr/bin/env python3
"""Patch v1039 -> v1040: the full-screen link view gets a flaps (🪽) button and a comment (💬) button beside Open
Link, so the row is Open Link · 🪽 · 💬 · Open Post.
- 🪽 presses the post card's own flaps button (same sign-in prompt, same vote code) and copies its count/lit state.
- 💬 closes the view and follows the card's own chat link (/post/<id>?chat=1), straight into the chat.
Also renames the page class used while the view is open (reel-open -> reel-shown): it clashed with the Open Link
button's class name."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1039.js'
dst = '_deploy/assets/index-DUcNPOLc-v1040.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('document.documentElement.classList.add(`reel-open`)', 'document.documentElement.classList.add(`reel-shown`)', 'page class on')
patch('document.documentElement.classList.remove(`reel-open`)', 'document.documentElement.classList.remove(`reel-shown`)', 'page class off')
patch('html.reel-open,html.reel-open body{background:#0b0c10!important}', 'html.reel-shown,html.reel-shown body{background:#0b0c10!important}', 'page class css')
# helpers: find the live card's flaps button and chat link
patch('function _reelCollect(){',
 'function _reelCard(id){const a=id&&document.querySelector(`[data-lp-id="${CSS.escape(id)}"]`);return a&&a.closest(`.feed-post-card`)}\n'
 'function _reelFlapBtn(id){const c=_reelCard(id);if(!c)return null;for(const b of c.querySelectorAll(`.feed-post-actions button`))if((b.textContent||``).includes(`🪽`))return b;return null}\n'
 'function _reelChatA(id){const c=_reelCard(id);return c&&c.querySelector(`.feed-post-actions a[href*="chat=1"]`)}\n'
 'function _reelSync(s){try{const id=s.dataset.post,fb=s.querySelector(`.reel-flap`),cb=s.querySelector(`.reel-chat`);const b=_reelFlapBtn(id);'
 'if(fb){if(b){fb.hidden=!1;const sp=b.querySelectorAll(`span`);fb.querySelector(`.n`).textContent=(sp[sp.length-1]||{}).textContent||`0`;fb.classList.toggle(`on`,/192,\\s*132,\\s*252/.test(b.getAttribute(`style`)||``))}else fb.hidden=!0}'
 'const a=_reelChatA(id);if(cb&&a){const sp=a.querySelectorAll(`span`);cb.querySelector(`.n`).textContent=(sp[sp.length-1]||{}).textContent||`0`}}catch(e){}}\n'
 'function _reelCollect(){', 'helpers')
patch('let gone=!1,pendingPost=null;', 'let gone=!1,pendingPost=null,pendingChat=null,pendingNoAuth=!1;', 'state')
patch('if(pendingPost){const t=document.querySelector(`[data-lp-id="${CSS.escape(pendingPost)}"]`);',
 'if(pendingNoAuth){window.dispatchEvent(new CustomEvent(`like-no-auth`))}else if(pendingChat){const a=_reelChatA(pendingChat);if(a)a.click();else location.href=`/post/${pendingChat}?chat=1&via=card`}else if(pendingPost){const t=document.querySelector(`[data-lp-id="${CSS.escape(pendingPost)}"]`);',
 'teardown targets')
patch('const goPost=id=>{pendingPost=id;close()};',
 'const goPost=id=>{pendingPost=id;close()};const goChat=id=>{pendingChat=id;close()};'
 'const flap=(s,id)=>{const b=_reelFlapBtn(id);if(!b)return;let na=!1;const h=()=>{na=!0};window.addEventListener(`like-no-auth`,h);try{b.click()}finally{window.removeEventListener(`like-no-auth`,h)}'
 'if(na){pendingNoAuth=!0;close();return}const fb=s.querySelector(`.reel-flap`);fb&&(fb.classList.add(`pop`),setTimeout(()=>fb.classList.remove(`pop`),260));[30,350,1200].forEach(t=>setTimeout(()=>_reelSync(s),t))};',
 'goChat + flap')
patch('btns.append(open,post);inner.appendChild(btns);return s};',
 'const mk=(cls,ic,lbl)=>{const b=document.createElement(`button`);b.type=`button`;b.className=`reel-btn reel-mini `+cls;b.setAttribute(`aria-label`,lbl);const i=document.createElement(`span`);i.className=`i`;i.textContent=ic;const n=document.createElement(`span`);n.className=`n`;n.textContent=`0`;b.append(i,n);return b};'
 'const fl=mk(`reel-flap`,`🪽`,`Flap this post`);fl.onclick=e=>{e.stopPropagation();flap(s,d.post)};'
 'const ch=mk(`reel-chat`,`💬`,`Open the chat`);ch.onclick=e=>{e.stopPropagation();goChat(d.post)};'
 'btns.append(open,fl,ch,post);inner.appendChild(btns);_reelSync(s);return s};', 'buttons')
patch('const ds=slides[k]&&slides[k].querySelector(`.reel-desc`);ds&&_reelFade(ds)',
      'const ds=slides[k]&&slides[k].querySelector(`.reel-desc`);ds&&_reelFade(ds);slides[k]&&_reelSync(slides[k])', 'resync near slides')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel-btns{gap:8px}
.reel-btns .reel-btn{padding:12px 6px;white-space:nowrap}
.reel-btn.reel-mini{flex:0 0 auto;min-width:58px;display:inline-flex;align-items:center;justify-content:center;gap:3px;padding:12px 10px;background:#1e293b;color:#e2e8f0;border-color:#334155;font-size:14px}
.reel-btn.reel-mini[hidden]{display:none}
.reel-mini .i{font-size:16px;line-height:1}
.reel-flap .i{margin-right:-2px}
.reel-flap.on{border-color:#c084fc;background:rgba(192,132,252,.18);color:#f3e8ff}
.reel-flap.pop .i{transform:scale(1.3);transition:transform .12s}
.reel-mini .i{transition:transform .12s}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
