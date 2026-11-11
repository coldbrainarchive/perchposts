#!/usr/bin/env python3
"""Patch v1002 -> v1003: huddle invitations.
- Invites: the owner's (and mods') invites, and the birds picked when making a huddle, arrive as a notification
  with Accept / Decline. Nobody is in until they accept. Accepting or declining shows as a system line in the chat.
- Members who aren't the owner can still use Invite and Remove: it becomes "Ask to invite / Ask to remove" and
  the owner gets Approve / Deny in their notifications (a no only goes back to the bird who asked).
- Notifications show the buttons right in the panel; once answered they show the outcome. Tapping an invite you
  haven't accepted doesn't try to open the huddle.
- Members sheet: an "Invited" section lists pending invites; the owner (or whoever sent it) can cancel one.
- A small message confirms "Invite sent to …" / "Asked … to …"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1002.js'
dst = '_deploy/assets/index-DUcNPOLc-v1003.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# Invite / remove flows: requests come back pending
patch('if(_ij.post)l(Cr(_ij.post));',
      'if(_ij.post)l(Cr(_ij.post));if(_ij.pending){_hxToast(_ij.message||`Invite sent`);_hxRefresh();_setWpInvR([]);_setWpInvQ(``);_setWpInvOpen(!1);_setWpInvP(null);return;}',
      'invite pending')
patch('if(_rj.post)l(Cr(_rj.post));',
      'if(_rj.post)l(Cr(_rj.post));if(_rj.pending){_hxToast(_rj.message||`Request sent`);_setWpRemOpen(!1);_setWpRemP(null);return;}',
      'remove pending')
# Every member can use Remove (non-owners ask the owner)
patch('return c?.is_huddle&&!c.frozen&&(_rIsOp||_rIsAdm||_rIsMod)?', 'return c?.is_huddle&&!c.frozen?', 'remove for all members')
patch('if(_rIsOp2&&!_rIsAdm2&&!_rIsMod2&&(_m.r===`admin`||_m.r===`mod`))return !1;',
      'if(!_rIsAdm2&&!_rIsMod2&&(_m.r===`admin`||_m.r===`mod`||_adminUsers.has(_m.u.toLowerCase())||_modUsers.has(_m.u.toLowerCase())))return !1;', 'no mods/admins in remove list')
patch('children:`Remove `+_wpRemP.u', 'children:(_hxBoss(c)?`Remove `:`Ask to remove `)+_wpRemP.u', 'remove label')
patch('children:`Invite `+_wpInvP.username', 'children:(_hxBoss(c)?`Invite `:`Ask to invite `)+_wpInvP.username', 'invite label')
# Notifications: buttons for invitations / requests
patch('return[avatar,txt,time]}',
      'return[avatar,e.req?(0,L.jsxs)(`div`,{style:{flex:1,minWidth:0,display:`flex`,flexDirection:`column`,gap:8},children:[txt,(0,L.jsx)(_HxReq,{n:e},`rq`)]}):txt,time]}',
      'request buttons')
patch('onClick:_ev=>{_nTap(_ev);_nMark(e);a()}',
      'onClick:_ev=>{if(e.req&&e.req.kind===`invite`&&e.req.status!==`accepted`){_ev.preventDefault();_nMark(e);return}_nTap(_ev);_nMark(e);a()}',
      'invite pill does not open huddle')
# Members sheet: invited section
patch('function _hxSheet(post,members){', 'function _hxSheetOld(post,members){', 'old sheet renamed')
patch('children:`${all.length} birds`', 'children:`${all.length} birds`+((post.huddle_pending||[]).length?` · ${post.huddle_pending.length} invited`:``)', 'invited count')

c += r'''
function _hxMe(){return(Qn()?.username||localStorage.getItem(`_myUsername`)||``).toLowerCase()}
function _hxBoss(post){try{const r=JSON.parse(localStorage.getItem(`auth_user`)||`{}`).role;if(r===`mod`||r===`admin`)return!0}catch(e){}return!!post&&_hxMe()===(post.username||``).toLowerCase()}
function _hxRefresh(){try{window.dispatchEvent(new Event(`focus`))}catch(e){}}
function _hxToast(msg){try{document.querySelectorAll(`.hx-toast`).forEach(x=>x.remove());const t=document.createElement(`div`);t.className=`hx-toast`;t.setAttribute(`role`,`status`);t.textContent=msg;document.body.append(t);
 requestAnimationFrame(()=>t.classList.add(`in`));setTimeout(()=>{t.classList.remove(`in`);setTimeout(()=>t.remove(),250)},2600)}catch(e){}}
function _HxReq({n}){const r=n.req,[st,setSt]=(0,_.useState)(r.status),[busy,setBusy]=(0,_.useState)(!1),[err,setErr]=(0,_.useState)(null);
 const go=async(yes,ev)=>{ev.preventDefault();ev.stopPropagation();if(busy)return;setBusy(!0);setErr(null);
  try{const x=await fetch(`${R}/huddle-respond`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({req_id:r.id,accept:yes})});const j=await x.json().catch(()=>({}));
   if(j.status){setSt(j.status);r.status=j.status;r.act=!1}if(!x.ok)setErr(j.error||`Something went wrong`)}catch(e){setErr(`Something went wrong`)}setBusy(!1);try{_nMark(n)}catch(e){}};
 const lb=r.kind===`invite`?[`Accept`,`Decline`]:[`Approve`,`Deny`];
 const done={accepted:r.kind===`invite`?`✓ You joined · tap to open`:`✓ Accepted`,declined:`You declined`,approved:`✓ Approved`,denied:`You said no`,expired:`Expired`,cancelled:`Cancelled`}[st];
 const stop=ev=>{ev.preventDefault();ev.stopPropagation()};
 if(st===`pending`&&r.act)return(0,L.jsxs)(`div`,{className:`hxq`,onClick:stop,children:[(0,L.jsx)(`button`,{type:`button`,className:`hxq-b yes`,disabled:busy,onClick:ev=>go(!0,ev),children:lb[0]}),(0,L.jsx)(`button`,{type:`button`,className:`hxq-b no`,disabled:busy,onClick:ev=>go(!1,ev),children:lb[1]}),err?(0,L.jsx)(`span`,{className:`hxq-err`,children:err}):null]});
 if(st===`pending`)return(0,L.jsx)(`span`,{className:`hxq-done`,children:`Waiting for the owner`});
 return done?(0,L.jsxs)(`span`,{className:`hxq-done`+(st===`accepted`||st===`approved`?` ok`:``),children:[done,err?` · ${err}`:``]}):null}
function _hxSheet(post,members){const host=document.createElement(`div`);document.body.append(host);const root=(0,g.createRoot)(host);
 const close=()=>{host.querySelector(`.hx-sheet`)?.classList.remove(`in`);setTimeout(()=>{root.unmount();host.remove()},200);removeEventListener(`popstate`,close)};addEventListener(`popstate`,close);
 root.render((0,L.jsx)(_HxSheetBody,{post,members,close}));requestAnimationFrame(()=>requestAnimationFrame(()=>host.querySelector(`.hx-sheet`)?.classList.add(`in`)))}
function _HxSheetBody({post,members,close}){const me=_hxMe(),all=_hxAll(post,members),boss=_hxBoss(post),[pend,setPend]=(0,_.useState)(post.huddle_pending||[]);
 const cancel=async(q,ev)=>{ev.stopPropagation();if(!confirm(`Cancel the invite for ${q.target}?`))return;
  try{const x=await fetch(`${R}/huddle-cancel`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({req_id:q.id})});if(!x.ok)throw 0;
   post.huddle_pending=(post.huddle_pending||[]).filter(y=>y.id!==q.id);setPend(post.huddle_pending);_hxToast(`Invite for ${q.target} cancelled`)}catch(e){alert(`Could not cancel the invite`)}};
 const row=(m,extra,dim)=>{const k=_hxCol(m),mine=m.username.toLowerCase()===me;return(0,L.jsxs)(`div`,{className:`hx-item`+(dim?` hx-pend`:``),"data-gpb":mine?void 0:m.username,style:{background:`color-mix(in srgb, ${k} 7%, #15171d)`,border:`1px solid color-mix(in srgb, ${k} 22%, transparent)`},children:[
   _hxDot({...m,owner:!1},40,!1,!1),(0,L.jsx)(`span`,{className:`hx-nm`,style:{color:k===`#ffffff`?`#f1f5f9`:k},children:m.username}),...extra]},m.username)};
 return(0,L.jsx)(`div`,{className:`hx-back`,onClick:close,children:(0,L.jsxs)(`div`,{className:`hx-sheet`,onClick:ev=>ev.stopPropagation(),children:[(0,L.jsx)(`div`,{className:`bc-grab`}),
  (0,L.jsxs)(`div`,{className:`hx-sh`,children:[`Members`,(0,L.jsx)(`span`,{children:all.length})]}),
  (0,L.jsx)(`div`,{className:`hx-list`,children:all.map(m=>row(m,[m.owner?(0,L.jsx)(`span`,{className:`hx-tag`,children:`👑 Owner`},`o`):null,m.username.toLowerCase()===me?(0,L.jsx)(`span`,{className:`hx-tag`,children:`You`},`y`):null],!1))}),
  pend.length?(0,L.jsxs)(`div`,{className:`hx-sh hx-sh2`,children:[`Invited`,(0,L.jsx)(`span`,{children:pend.length})]}):null,
  pend.length?(0,L.jsx)(`div`,{className:`hx-list`,children:pend.map(q=>row({username:q.target},[(0,L.jsx)(`span`,{className:`hx-tag`,children:`⏳ Waiting`},`w`),
   boss||me===(q.from_user||``).toLowerCase()?(0,L.jsx)(`button`,{type:`button`,className:`hx-cancel`,onClick:ev=>cancel(q,ev),children:`Cancel`},`c`):null],!0))}):null]})})}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.hxq{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.hxq-b{height:32px;padding:0 16px;border-radius:999px;font-family:inherit;font-size:13px;font-weight:800;cursor:pointer;-webkit-tap-highlight-color:transparent}
.hxq-b.yes{background:#c084fc;color:#14081d;border:1px solid #c084fc}
.hxq-b.no{background:transparent;color:#cbd5e1;border:1px solid #475569}
.hxq-b:disabled{opacity:.55}
.hxq-err{font-size:12px;color:#f87171}
.hxq-done{font-size:12px;font-weight:700;color:#94a3b8}
.hxq-done.ok{color:#86efac}
.hx-sh2{margin-top:14px}
.hx-pend .hx-dot{opacity:.55}
.hx-pend .hx-nm{opacity:.75}
.hx-cancel{flex-shrink:0;height:28px;padding:0 12px;border-radius:999px;border:1px solid #475569;background:none;color:#cbd5e1;font-family:inherit;font-size:12px;font-weight:700;cursor:pointer}
.hx-toast{position:fixed;left:50%;bottom:calc(28px + env(safe-area-inset-bottom));transform:translate(-50%,12px);z-index:3000;max-width:calc(100vw - 32px);padding:10px 16px;border-radius:999px;background:#1b1d24;border:1px solid #c084fc;color:#f1f5f9;font-size:13.5px;font-weight:700;box-shadow:0 8px 28px rgba(0,0,0,.5);opacity:0;transition:opacity .2s,transform .2s;pointer-events:none;text-align:center}
.hx-toast.in{opacity:1;transform:translate(-50%,0)}
@media (prefers-reduced-motion: reduce){.hx-toast{transition:none}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
