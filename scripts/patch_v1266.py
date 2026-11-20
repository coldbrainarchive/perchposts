#!/usr/bin/env python3
"""Patch v1265 -> v1266: signed-out taps.
- Post scroller (reel): flap / chirp buttons no longer close the scroller; they show a pill "Sign in to flap" / "Sign in to chirp".
- Any sign-in nudge (like-no-auth) while the header Sign In button is hidden (scroller, full chat, sheets) shows the pill;
  on the feed / post page it keeps flashing Sign In.
- "Write the first chirp" signed out: flashes Sign In instead of opening an empty chat. Chat box says "Sign in to chirp".
- Link posts in the scroller get a "View post" link under the site link (user posts already had one)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1265.js'
dst = '_deploy/assets/index-DUcNPOLc-v1266.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
NA = "window.dispatchEvent(new CustomEvent(`like-no-auth`))"
NAC = "window.dispatchEvent(new CustomEvent(`like-no-auth`,{detail:{w:`chirp`}}))"
patch("const flap=(s,id)=>{if(!localStorage.getItem(`auth_token`)){pendingNoAuth=!0;close();return}",
      "const flap=(s,id)=>{if(!localStorage.getItem(`auth_token`)){window._ppSignPill&&window._ppSignPill(`flap`);return}", 'reel flap')
patch("ch.onclick=e=>{e.stopPropagation();goChat(d.post)}",
      "ch.onclick=e=>{e.stopPropagation();if(!localStorage.getItem(`auth_token`)){window._ppSignPill&&window._ppSignPill(`chirp`);return}goChat(d.post)}", 'reel chirp')
patch("inner.appendChild(site);",
      "inner.appendChild(site);if(d.kind!==`u`&&d.post){const vp=document.createElement(`a`);vp.className=`reel-site reel-vp`;vp.href=`/post/${d.post}`;vp.innerHTML=`<span>View post</span><span class=\"reel-site-ar\">${_RI.ARROW}</span>`;vp.addEventListener(`click`,e=>{e.preventDefault();e.stopPropagation();goPost(d.post)});inner.appendChild(vp)}", 'reel link View post')
patch("`Sign in to comment`", "`Sign in to chirp`", 'chat placeholder')
patch("onClick:e?void 0:()=>" + NA, "onClick:e?void 0:()=>" + NAC, 'chat box nudge')
patch(NA + ";return}_cMR.current?.click()", NAC + ";return}_cMR.current?.click()", 'chat + nudge')
patch(NA + ";return}s&&s(e)", NAC + ";return}s&&s(e)", 'chat reply nudge')
patch("function D(){y(!1);if(!localStorage.getItem(`auth_token`)){" + NA + ";return}",
      "function D(){y(!1);if(!localStorage.getItem(`auth_token`)){" + NAC + ";return}", 'chat D nudge')
c += r"""
;(()=>{try{
  const st=document.createElement(`style`);st.textContent=`body .reel-vp{margin-top:8px}.pp-signpill{position:fixed;left:50%;top:calc(env(safe-area-inset-top) + 64px);transform:translate(-50%,-6px);z-index:2147483000;padding:10px 18px;border-radius:999px;background:#c084fc;color:#14081d;font:800 14px/1 system-ui,-apple-system,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.5);opacity:0;transition:opacity .18s,transform .18s;pointer-events:none;white-space:nowrap}.pp-signpill.on{opacity:1;transform:translate(-50%,0)}`;document.head.appendChild(st);
  let el,tm;
  const chipShown=()=>{const ch=[...document.querySelectorAll(`.app-chip`)].find(x=>x.textContent.trim()===`Sign In`);if(!ch)return!1;const r=ch.getBoundingClientRect();if(!r.width||r.bottom<=0||r.top>=innerHeight)return!1;const h=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return!!h&&(h===ch||ch.contains(h))};
  window._ppSignPill=w=>{if(!el){el=document.createElement(`div`);el.className=`pp-signpill`;el.setAttribute(`role`,`status`);document.body.appendChild(el)}el.textContent=w===`flap`?`Sign in to flap`:w===`chirp`?`Sign in to chirp`:`Sign in first`;el.classList.add(`on`);clearTimeout(tm);tm=setTimeout(()=>el.classList.remove(`on`),1800)};
  window.addEventListener(`like-no-auth`,e=>{if(document.documentElement.classList.contains(`reel-shown`)||!chipShown())window._ppSignPill(e.detail&&e.detail.w)});
  document.addEventListener(`click`,e=>{if(localStorage.getItem(`auth_token`))return;const b=e.target.closest&&e.target.closest(`.chat-view-all`);if(b&&b.textContent.trim()===`Write the first chirp`){e.preventDefault();e.stopPropagation();window.dispatchEvent(new CustomEvent(`like-no-auth`,{detail:{w:`chirp`}}))}},!0);
}catch(e){console.error(e)}})();
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
