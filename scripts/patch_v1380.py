#!/usr/bin/env python3
"""Patch v1379 -> v1380: the open post's action row = the scroller's: flaps | chirps | worms | share.
- Chirps button (with the count) closes the open post. The "· N chirps" is gone from the small header.
- Same behaviour as the scroller: flap pops + wings flap + purple; share opens the huddle sheet (signed in) or shows
  ✓ Shared for 1.8s; worms open the worm wallet and wiggle; signed-out taps give the sign-in nudge."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1379.js'
dst = '_deploy/assets/index-DUcNPOLc-v1380.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

patch(",(0,L.jsx)(`span`,{children:`· ${n} chirp${n===1?``:`s`}`})]})]})}", "]})]})}", 'no count in header')
patch("dock:{post:c,score:re.score,mine:re.myVote===1,onFlap:", "dock:{post:c,n:_cn,score:re.score,mine:re.myVote===1,onFlap:", 'pass chirp count')
patch("(0,L.jsx)(_ChDock,{...dock,grab:", "(0,L.jsx)(_ChDock,{...dock,chat:shut,grab:", 'chirps closes')

# the row itself, rebuilt to mirror the scroller dock
i = c.index("function _ChDock({post:c,score,mine,onFlap,grab})")
j = c.index("\n", c.index("  grab]})}", i)) + 1
TICK = '<svg class=\\"ri\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"1.9\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" aria-hidden=\\"true\\"><path d=\\"M5 12.5l4.5 4.5L19 7.5\\"/></svg>'
c = c[:i] + r"""function _ChDock({post:c,n,score,mine,onFlap,chat,grab}){const[,f]=(0,_.useState)(0),[pop,setPop]=(0,_.useState)(!1),[done,setDone]=(0,_.useState)(!1);
 const hu=!!c.username&&!_ppIsBot(c)&&!/^Anon #/.test(c.username),K=_ppWorm.key(`p`,c.id);
 (0,_.useEffect)(()=>{if(!hu)return;_ppWorm.want(`p`,c.id);return _ppWorm.sub(K,()=>f(x=>x+1))},[K,hu]);
 (0,_.useEffect)(()=>{const h=ev=>{ev.detail&&ev.detail.id===c.id&&f(x=>x+1)};addEventListener(`pp-sharen`,h);return()=>removeEventListener(`pp-sharen`,h)},[c.id]);
 const shn=_ppShN(c.id,c.share_count),auth=()=>!!localStorage.getItem(`auth_token`),noAuth=()=>window.dispatchEvent(new CustomEvent(`like-no-auth`));
 const flap=ev=>{ev.stopPropagation();if(!auth()){noAuth();return}if(_ppOwn(c.username)){_ppOwnMsg();return}const b=ev.currentTarget;if(!mine)_ppFlapAnim(b);setPop(!0);setTimeout(()=>setPop(!1),260);onFlap(ev)};
 const share=async ev=>{ev.stopPropagation();if(window._ppShare&&window._ppShare(c.id))return;const u=`${location.origin}/post/${c.id}`;let ok=!1;try{if(navigator.share){await navigator.share({url:u});ok=!0}else if(navigator.clipboard&&navigator.clipboard.writeText){await navigator.clipboard.writeText(u);ok=!0}}catch(er){}if(ok){setDone(!0);setTimeout(()=>setDone(!1),1800)}};
 const worm=ev=>{ev.stopPropagation();if(!auth()){noAuth();return}const me=(localStorage.getItem(`_myUsername`)||``).toLowerCase();_wormWallet(c.id,!!me&&me===c.username.toLowerCase(),1)};
 const B=(cls,lbl,ic,num,on,click,extra)=>(0,L.jsxs)(`button`,{type:`button`,className:`ch-db `+cls+(on?` on`:``)+(extra||``),"aria-label":lbl,onClick:click,children:[ic,(0,L.jsx)(`span`,{className:`n`,children:num})]},cls);
 return(0,L.jsxs)(`div`,{className:`ch-dock`,onClick:ev=>ev.stopPropagation(),children:[(0,L.jsxs)(`div`,{className:`ch-dock-row`,children:[
  B(`ch-fl`,`Flap this post`,(0,L.jsx)(`span`,{className:`i pp-ic pp-bird`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}),score,mine,flap,pop?` pop`:``),
  B(`ch-ch`,`Back to the chirps`,(0,L.jsx)(`span`,{className:`i pp-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`CHAT`)}}),n,!1,ev=>{ev.stopPropagation();chat&&chat()}),
  hu?B(`ch-wm`,`Worms`,(0,L.jsx)(`span`,{className:`i pp-ic pp-worm`,"data-wk":K,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),_ppWorm.n(K)||0,!1,worm):null,
  done?B(`ch-sh`,`Share`,(0,L.jsx)(`span`,{className:`i pp-ic`,dangerouslySetInnerHTML:{__html:`""" + TICK + r"""`}}),`Shared`,!1,share,` done`)
      :B(`ch-sh`,`Share`,(0,L.jsx)(`span`,{className:`i pp-ic pp-share`,dangerouslySetInnerHTML:{__html:_ppIco(`SHARE`)}}),shn>0?shn:`Share`,!1,share)]}),
  grab]})}
""" + c[j:]

patch("body .lb-ic{",
 "body .ch-db .i{display:inline-flex;transition:transform .12s}body .ch-db.pop .i{transform:scale(1.3)}"
 "body .ch-db.on .n{color:#c084fc}body .ch-db.done{color:#c084fc}"
 "body .ch-db.ch-ch .pp-ic .ri{width:16px;height:16px}body .ch-db.ch-sh.done .pp-ic .ri{width:16px;height:16px}"
 "body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
