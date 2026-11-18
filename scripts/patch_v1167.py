#!/usr/bin/env python3
"""Patch v1166 -> v1167: huddle controls move into the Members sheet.
- The huddle post no longer shows Invite / Remove / Leave pills (only the members row and the age pill).
- Members sheet: "+ Invite" in the header opens a search inside the sheet; each removable member gets a ⋯ button
  ("Remove from huddle" / "Ask to remove"); a red "Leave huddle" at the bottom.
- Same rules and server calls as before (the page's own invite / remove / leave code does the work)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1166.js'
dst = '_deploy/assets/index-DUcNPOLc-v1167.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

def grab(start, end):
    i = c.index(start); j = c.index(end, i)
    if c.count(start) != 1: print('FAIL grab', start[:40]); sys.exit(1)
    return c[i + len(start):j]

# --- pull the page's handlers out so the sheet can call them ---
INV_START = "onClick:()=>{if(!_wpInvP)return;"
INV_END = "},children:(_hxBoss(c)?`Invite `"
inv_body = grab(INV_START, INV_END)
REM_START = "marginTop:8},onClick:()=>{const _rUn2=localStorage.getItem(`_myUsername`)||null;"
REM_END = "},children:(_hxBoss(c)?`Remove `"
rem_body = grab(REM_START, REM_END)
LV_START = "c?.is_huddle&&!c.frozen&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:()=>{const _un3="
LV_END = "},children:`Leave`})"
lv_body = "const _un3=" + grab(LV_START, LV_END)

# invite: the picked user arrives as _P; resolve when the server answers
inv_fn = inv_body.replace("_wpInvP", "_P")
assert "fetch(`${R}/invite-to-huddle`" in inv_fn
inv_fn = inv_fn.replace("fetch(`${R}/invite-to-huddle`", "return fetch(`${R}/invite-to-huddle`", 1)
inv_fn = inv_fn.replace("if(!_r.ok){alert(_ij.error||`Could not invite user`);return;}", "if(!_r.ok){alert(_ij.error||`Could not invite user`);return!1;}", 1)
inv_fn = inv_fn.replace(".catch(err=>alert(`Invite failed: `+err.message));", ".then(v=>v!==!1).catch(err=>{alert(`Invite failed: `+err.message);return!1});", 1)
rem_fn = rem_body.replace("_wpRemP", "_M")
rem_fn = rem_fn.replace("fetch(`${R}/remove-from-huddle`", "return fetch(`${R}/remove-from-huddle`", 1)
ACT = ("window._hxAct=c.is_huddle&&!c.frozen?{id:c.id,"
       "invite:_P=>{" + inv_fn + "},"
       "remove:_M=>{const _rUn2=localStorage.getItem(`_myUsername`)||null;" + rem_fn + "},"
       "leave:()=>{" + lv_body + "}}:null;")
patch("return de.filter(e=>!e.parent_comment_id),(0,L.jsxs)(`div`,{className:`home-shell`",
      ACT + "return de.filter(e=>!e.parent_comment_id),(0,L.jsxs)(`div`,{className:`home-shell`", 'page exposes huddle actions')

# --- hide the three pills on the post ---
patch("c?.is_huddle&&!c.frozen&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,style:_wpInvOpen?",
      "!1&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,style:_wpInvOpen?", 'no Invite pill')
patch("return c?.is_huddle&&!c.frozen?(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,style:_wpRemOpen?",
      "return !1?(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,style:_wpRemOpen?", 'no Remove pill')
patch(LV_START, "!1&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:()=>{const _un3=", 'no Leave pill')

# --- the sheet ---
patch("function _HxSheetBody({post,members,close}){const me=_hxMe(),all=_hxAll(post,members),boss=_hxBoss(post),[pend,setPend]=(0,_.useState)(post.huddle_pending||[]);",
      r'''function _hxCanRm(m,me){if(!m||m.owner||!m.username||m.username.toLowerCase()===me)return!1;let staff=!1;try{const r=JSON.parse(localStorage.getItem(`auth_user`)||`{}`).role;staff=r===`mod`||r===`admin`}catch(e){}
 const u=m.username.toLowerCase();if(!staff&&(m.role===`admin`||m.role===`mod`||_adminUsers.has(u)||_modUsers.has(u)))return!1;return!0}
function _HxInvite({post,all,boss,close}){const[q,setQ]=(0,_.useState)(``),[res,setRes]=(0,_.useState)([]),[busy,setBusy]=(0,_.useState)(null),tm=(0,_.useRef)(null),inp=(0,_.useRef)(null);
 (0,_.useEffect)(()=>{setTimeout(()=>inp.current?.focus(),60)},[]);
 const have=new Set([...all.map(m=>m.username.toLowerCase()),...(post.huddle_pending||[]).map(p=>(p.target||``).toLowerCase())]);
 const onQ=v=>{setQ(v);clearTimeout(tm.current);if(!v.trim()){setRes([]);return}tm.current=setTimeout(()=>{fetch(`${R}/search-users?q=${encodeURIComponent(v.trim())}`).then(r=>r.ok?r.json():{users:[]}).then(d=>setRes((d.users||[]).filter(u=>u.username&&!have.has(u.username.toLowerCase())).slice(0,6))).catch(()=>setRes([]))},250)};
 const go=async u=>{const a=window._hxAct;if(!a||a.id!==post.id||busy)return;setBusy(u.username);const ok=await a.invite(u);setBusy(null);if(ok)close()};
 return(0,L.jsxs)(`div`,{className:`hx-inv`,children:[(0,L.jsx)(`input`,{ref:inp,className:`hx-inv-in`,type:`search`,value:q,onChange:e=>onQ(e.target.value),placeholder:`Search birds to invite`,autoComplete:`off`,autoCapitalize:`none`,spellCheck:!1,enterKeyHint:`search`}),
  res.length?(0,L.jsx)(`div`,{className:`hx-list`,children:res.map(u=>{const m={username:u.username,browser_id:u.browser_id||null,role:u.role||null},k=_hxCol(m);return(0,L.jsxs)(`div`,{className:`hx-item`,style:{background:`color-mix(in srgb, ${k} 7%, #15171d)`,border:`1px solid color-mix(in srgb, ${k} 22%, transparent)`},onClick:()=>go(u),children:[
   _hxDot(m,34,!1,!1),(0,L.jsx)(`span`,{className:`hx-nm`,style:{color:k===`#ffffff`?`#f1f5f9`:k},children:u.username}),(0,L.jsx)(`button`,{type:`button`,className:`hx-inv-go`,disabled:!!busy,onClick:ev=>{ev.stopPropagation();go(u)},children:busy===u.username?`…`:boss?`Invite`:`Ask`})]},u.username)})}):q.trim()?(0,L.jsx)(`div`,{className:`hx-inv-none`,children:`No birds found`}):null]})}
function _HxSheetBody({post,members,close}){const me=_hxMe(),all=_hxAll(post,members),boss=_hxBoss(post),[pend,setPend]=(0,_.useState)(post.huddle_pending||[]),[inv,setInv]=(0,_.useState)(!1);
 const act=window._hxAct&&window._hxAct.id===post.id?window._hxAct:null,amIn=all.some(m=>m.username.toLowerCase()===me);
 const more=(m,ev)=>{ev.stopPropagation();const b=ev.currentTarget;_prFilterMenu(b,null,[[`rm`,null,boss?`Remove from huddle`:`Ask to remove`]],()=>{if(!confirm(boss?`Remove ${m.username} from this huddle?`:`Ask the owner to remove ${m.username}?`))return;close();act&&act.remove({u:m.username,r:m.role||null})});const mm=document.querySelector(`.cp-menu`);if(mm)mm.classList.add(`hx-menu`)};''',
      'sheet: invite + remove helpers')
# header: + Invite
patch("(0,L.jsxs)(`div`,{className:`hx-sh`,children:[`Members`,(0,L.jsx)(`span`,{children:all.length})]}),\n  (0,L.jsx)(`div`,{className:`hx-list`,children:all.map(m=>row(m,[",
      "(0,L.jsxs)(`div`,{className:`hx-sh`,children:[`Members`,(0,L.jsx)(`span`,{children:all.length}),act&&amIn?(0,L.jsx)(`button`,{type:`button`,className:`hx-addb`+(inv?` on`:``),onClick:ev=>{ev.stopPropagation();setInv(!inv)},children:inv?`Cancel`:`+ Invite`}):null]}),\n"
      "  inv&&act?(0,L.jsx)(_HxInvite,{post,all,boss,close}):null,\n"
      "  (0,L.jsx)(`div`,{className:`hx-list`,children:all.map(m=>row(m,[", 'header invite button')
# ⋯ on removable rows
patch("m.username.toLowerCase()===me?(0,L.jsx)(`span`,{className:`hx-tag`,children:`You`},`y`):null],!1))}),",
      "m.username.toLowerCase()===me?(0,L.jsx)(`span`,{className:`hx-tag`,children:`You`},`y`):null,act&&amIn&&_hxCanRm(m,me)?(0,L.jsx)(`button`,{type:`button`,className:`hx-more`,\"aria-label\":`Options for ${m.username}`,onClick:ev=>more(m,ev),children:`⋯`},`m`):null],!1))}),", 'row ⋯')
# leave at the bottom
patch("boss||me===(q.from_user||``).toLowerCase()?(0,L.jsx)(`button`,{type:`button`,className:`hx-cancel`,onClick:ev=>cancel(q,ev),children:`Cancel`},`c`):null],!0))}):null]})})}",
      "boss||me===(q.from_user||``).toLowerCase()?(0,L.jsx)(`button`,{type:`button`,className:`hx-cancel`,onClick:ev=>cancel(q,ev),children:`Cancel`},`c`):null],!0))}):null,\n"
      "  act&&amIn?(0,L.jsx)(`button`,{type:`button`,className:`hx-leave`,onClick:()=>{close();setTimeout(()=>act.leave(),230)},children:`Leave huddle`}):null]})})}", 'leave button')

css = ("body .hx-addb{margin-left:auto;height:32px;padding:0 14px;border-radius:999px;border:1px solid rgba(192,132,252,.45);background:rgba(192,132,252,.1);color:#d8b4fe;font-family:inherit;font-size:13px;font-weight:800;cursor:pointer;-webkit-tap-highlight-color:transparent}"
       "body .hx-addb.on{border-color:#475569;background:none;color:#cbd5e1}"
       "body .hx-sh>span{background:rgba(148,163,184,.12)}"
       "body .hx-inv{display:flex;flex-direction:column;gap:7px;margin:0 0 14px}"
       "body .hx-inv-in{height:42px;box-sizing:border-box;width:100%;border-radius:14px;border:1px solid #3a3d48;background:#0f1116;color:#f1f5f9;font:inherit;font-size:16px;padding:0 14px;outline:none;-webkit-appearance:none;appearance:none}"
       "body .hx-inv-in:focus{border-color:#c084fc;box-shadow:0 0 0 3px rgba(192,132,252,.18)}"
       "body .hx-inv-go{flex-shrink:0;height:30px;padding:0 14px;border-radius:999px;border:0;background:#c084fc;color:#14081d;font-family:inherit;font-size:12.5px;font-weight:800;cursor:pointer}"
       "body .hx-inv-none{font-size:13px;color:#94a3b8;padding:4px 6px}"
       "body .hx-more{flex-shrink:0;width:34px;height:34px;margin-right:-6px;border-radius:999px;border:0;background:none;color:#94a3b8;font-size:20px;font-weight:800;line-height:1;cursor:pointer;-webkit-tap-highlight-color:transparent}"
       "body .hx-more:active,body .hx-more:hover{background:rgba(148,163,184,.12);color:#f1f5f9}"
       "body .hx-leave{display:block;width:100%;margin:18px 0 0;height:46px;border-radius:999px;border:1px solid rgba(248,113,113,.35);background:rgba(248,113,113,.08);color:#f87171;font-family:inherit;font-size:14.5px;font-weight:800;cursor:pointer}"
       "body .cp-menu.hx-menu{z-index:1600}body .hx-menu .cp-opt[data-k=rm]{color:#f87171}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
