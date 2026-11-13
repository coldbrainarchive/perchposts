#!/usr/bin/env python3
"""Patch v1040 -> v1041: full-screen link view button row is one line of pills:
Open Link · 🪽 · 💬 · ↗ Share · Open Post. The middle three use the feed card's bubble colours; Open Link stays filled
purple and Open Post outlined, so the two main actions still stand out. Share works like the card's Share
(phone share sheet, or copies the link) and briefly shows ✓. On narrow phones the word "Open" is dropped."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1040.js'
dst = '_deploy/assets/index-DUcNPOLc-v1041.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('open.textContent=`Open Link`;', 'open.innerHTML=`<span class="w">Open</span><span>Link</span>`;', 'open link label')
patch('post.textContent=`Open Post`;', 'post.innerHTML=`<span class="w">Open</span><span>Post</span>`;', 'open post label')
patch('btns.append(open,fl,ch,post);',
 'const sh=document.createElement(`button`);sh.type=`button`;sh.className=`reel-btn reel-mini reel-share`;sh.setAttribute(`aria-label`,`Share`);sh.textContent=`↗`;'
 'sh.onclick=async e=>{e.stopPropagation();const u=`${location.origin}/post/${d.post}`;let ok=!1;'
 'try{if(navigator.share){await navigator.share({title:d.title||``,text:d.title||``,url:u});ok=!0}else if(navigator.clipboard&&navigator.clipboard.writeText){await navigator.clipboard.writeText(u);ok=!0}}catch(er){}'
 'if(ok){sh.textContent=`✓`;sh.classList.add(`done`);setTimeout(()=>{sh.textContent=`↗`;sh.classList.remove(`done`)},1800)}};'
 'btns.append(open,fl,ch,sh,post);', 'share button')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel .reel-btns{gap:6px;align-items:center}
.reel .reel-btns .reel-btn{height:38px;padding:0 10px;border-radius:999px;font-size:13px;line-height:1;display:inline-flex;align-items:center;justify-content:center;white-space:nowrap;min-width:0;box-sizing:border-box;gap:4px}
.reel .reel-btns .reel-open,.reel .reel-btns .reel-post{flex:1 1 0}
.reel .reel-btn.reel-mini{flex:0 0 auto;min-width:0;gap:4px;background:#1d242d;border:1px solid #323b48;color:#e5edf6;font-weight:700}
.reel .reel-mini .i{font-size:14px}
.reel .reel-share{font-size:15px;width:38px;padding:0}
.reel .reel-share.done{color:#c084fc;border-color:#c084fc}
.reel .reel-flap.on{border-color:#c084fc;background:rgba(192,132,252,.15);color:#f3e8ff}
@media (max-width:359px){.reel .reel-btns .w{display:none}.reel .reel-btns .reel-btn{padding:0 8px}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
