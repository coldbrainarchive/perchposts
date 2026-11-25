#!/usr/bin/env python3
"""Patch v1394 -> v1395: chirp filter improvements (user's ideas).
- Picking a filter starts you at the TOP of the list, and the list reads top-down: Top / Most replied best first,
  Media / Pinned newest first. Going back to All chirps returns to the newest chirps at the bottom.
- Find (on a reply) works inside a filter: if the chirp it points to isn't in the filtered list, the filter switches
  back to All chirps and it jumps there (loading older chirps if needed).
- Tapping the filter pill while a filter is on goes straight back to All chirps (no menu)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1394.js'
dst = '_deploy/assets/index-DUcNPOLc-v1395.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

# 1) every filtered list reads top-down (the chat window stacks from the bottom, so reverse each list)
patch("_rev=_cff===`top`||_cff===`rep`?[..._src].reverse():_src}", "_rev=[..._src].reverse()}", 'top-down lists')
# ...and switching filter scrolls: to the top for a filter, back to the newest end for All chirps (only on a real change)
patch("(0,_.useEffect)(()=>{let _id=_jmp.current,t=D.current;if(!_id||!t)return;",
      "(0,_.useEffect)(()=>{const pf=_cffR.current;_cffR.current=_cff;if(pf===void 0||pf===_cff||!_cf||_jmp.current)return;const go=()=>{const w=D.current;if(!w)return;if(_cff===`all`){_sbJump(w,0);x(!0)}else{_sbJump(w,1);x(!1)}};requestAnimationFrame(()=>requestAnimationFrame(go));setTimeout(go,350)},[_cff]);"
      "(0,_.useEffect)(()=>{let _id=_jmp.current,t=D.current;if(!_id||!t)return;", 'scroll on filter change')
patch("[_cff,_setCff]=(0,_.useState)(`all`),", "[_cff,_setCff]=(0,_.useState)(`all`),_cffR=(0,_.useRef)(void 0),", 'prev filter ref')
# 2) Find inside a filter
patch("onFindParent:e=>{let t=D.current,n=t?.querySelector(`[data-comment-id=\"${e}\"]`);if(t&&!n){_jmp.current=e;_older(`to=${encodeURIComponent(e)}`)}",
      "onFindParent:e=>{let t=D.current,n=t?.querySelector(`[data-comment-id=\"${e}\"]`);if(t&&!n&&_cff!==`all`){_jmp.current=e;_setCff(`all`);setTimeout(()=>{const w=D.current;if(w&&!w.querySelector(`[data-comment-id=\"${e}\"]`))_older(`to=${encodeURIComponent(e)}`)},60);return}if(t&&!n){_jmp.current=e;_older(`to=${encodeURIComponent(e)}`)}", 'find leaves the filter')
patch("_glow(n.querySelector(`.chat-msg-body`)||n)})},[u])", "_glow(n.querySelector(`.chat-msg-body`)||n)})},[u,_cff])", 'jump re-runs after filter change')
# 3) tapping the pill while a filter is on -> All chirps
patch("const open=ev=>{ev.stopPropagation();const ex=document.querySelector(`.chf-menu`);if(ex){ex.remove();return}",
      "const open=ev=>{ev.stopPropagation();const ex=document.querySelector(`.chf-menu`);if(ex){ex.remove();return}if(v!==`all`){set(`all`);return}", 'pill resets')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
