#!/usr/bin/env python3
"""Patch v1171 -> v1172: + Invite turns the Members sheet into just a search panel (members and invites hide).
After inviting someone it goes back to the member list, with them under "Invited"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1171.js'
dst = '_deploy/assets/index-DUcNPOLc-v1172.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch("window._hxAct=c.is_huddle&&!c.frozen?{id:c.id,", "window._hxAct=c.is_huddle&&!c.frozen?{id:c.id,get:()=>c,", 'page shares the fresh post')
patch("function _HxInvite({post,all,boss,close}){", "function _HxInvite({post,all,boss,close,done}){", 'invite gets done')
patch("const ok=await a.invite(u);setBusy(null);if(ok)close()};", "const ok=await a.invite(u);setBusy(null);if(ok)done(u)};", 'back to members after invite')
patch("inv&&act?(0,L.jsx)(_HxInvite,{post,all,boss,close}):null,",
      "inv&&act?(0,L.jsx)(_HxInvite,{post,all,boss,close,done:u=>{setInv(!1);const nm=u.username.toLowerCase();setPend(p=>p.some(x=>(x.target||``).toLowerCase()===nm)?p:[...p,{target:u.username,from_user:me}]);"
      "setTimeout(()=>{const a=window._hxAct,np=a&&a.id===post.id&&a.get?a.get():null;if(np&&Array.isArray(np.huddle_pending)&&np.huddle_pending.some(x=>(x.target||``).toLowerCase()===nm)){post.huddle_pending=np.huddle_pending;setPend(np.huddle_pending)}},1800)}}):null,",
      'done handler')
patch("(0,L.jsx)(`div`,{className:`hx-list`,children:all.map(m=>row(m,[", "inv?null:(0,L.jsx)(`div`,{className:`hx-list`,children:all.map(m=>row(m,[", 'hide members while searching')
patch("pend.length?(0,L.jsxs)(`div`,{className:`hx-sh hx-sh2`", "!inv&&pend.length?(0,L.jsxs)(`div`,{className:`hx-sh hx-sh2`", 'hide invited header')
patch("pend.length?(0,L.jsx)(`div`,{className:`hx-list`,children:pend.map", "!inv&&pend.length?(0,L.jsx)(`div`,{className:`hx-list`,children:pend.map", 'hide invited list')
patch("boss||me===(q.from_user||``).toLowerCase()?(0,L.jsx)(`button`,{type:`button`,className:`hx-cancel`",
      "q.id&&(boss||me===(q.from_user||``).toLowerCase())?(0,L.jsx)(`button`,{type:`button`,className:`hx-cancel`", 'cancel only once it has an id')
patch("children:[`Members`,(0,L.jsx)(`span`,{children:all.length}),act&&amIn", "children:[inv?`Invite birds`:`Members`,inv?null:(0,L.jsx)(`span`,{children:all.length}),act&&amIn", 'search heading')
patch("body .lb-ic{", "body .hx-sheet .hx-inv{min-height:min(46vh,360px)}body .lb-ic{", 'search panel keeps some height')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
