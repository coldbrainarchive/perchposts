#!/usr/bin/env python3
"""Patch v1238 -> v1239: AI check controls in the mod panel.
- Settings tab: an "AI check" On/Off switch (admins), next to the sign-up limit.
- New "Flagged" tab (mods and admins): what the AI check hid, with "Not bad" (puts it back and lets the bird out
  of The Cage) and "Confirm" (keeps it hidden, bird stays caged). Reviewed ones are listed underneath.
- Flag notifications show a line shield badge on the flagged bird."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1238.js'
dst = '_deploy/assets/index-DUcNPOLc-v1239.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

COMP = r"""function _AiCheck(){const[st,setSt]=(0,_.useState)(null),[busy,setBusy]=(0,_.useState)(!1),[err,setErr]=(0,_.useState)(``);
 (0,_.useEffect)(()=>{fetch(`${R}/site-settings`,{headers:er()}).then(r=>r.ok?r.json():null).then(d=>d&&setSt(d)).catch(()=>{})},[]);
 if(!st)return null;
 const cur=st.ai_check===`on`?`on`:`off`;
 const set=async v=>{if(!st.can_edit||busy||v===cur)return;setBusy(!0);setErr(``);try{const r=await fetch(`${R}/site-settings`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({ai_check:v})});const d=await r.json().catch(()=>({}));if(r.ok)setSt(d);else setErr(d.error||`Could not save`)}catch(e){setErr(`Could not save`)}setBusy(!1)};
 const say=cur===`on`?`Public posts and chirps are checked by AI right after they go up. If one is flagged for hate, threats or sexual abuse it's hidden, the bird goes to The Cage, and mods get a notification to review it (Flagged tab). Swearing isn't flagged.`:`Off: nothing is checked by AI. Slurs are still refused when someone tries to post them.`;
 return(0,L.jsxs)(`div`,{className:`content-card su-lim`,children:[
  (0,L.jsxs)(`div`,{className:`su-top`,children:[(0,L.jsxs)(`div`,{children:[(0,L.jsx)(`div`,{className:`su-t`,children:`AI check`}),(0,L.jsx)(`div`,{className:`su-s`,children:`Hate, threats and abuse`})]}),
   (0,L.jsx)(`div`,{className:`su-opts`,children:[[`on`,`On`],[`off`,`Off`]].map(([k,lb])=>(0,L.jsx)(`button`,{type:`button`,disabled:!st.can_edit||busy,className:`mod-tool fs`+(cur===k?` on`:``),onClick:()=>set(k),children:lb},k))})]}),
  (0,L.jsx)(`div`,{className:`su-say`,children:st.can_edit?say:say+` Only admins can change this.`}),err?(0,L.jsx)(`div`,{className:`su-err`,children:err}):null]})}
function _AiFlags(){const[d,setD]=(0,_.useState)(null),[busy,setBusy]=(0,_.useState)(``),[err,setErr]=(0,_.useState)(``);
 (0,_.useEffect)(()=>{fetch(`${R}/ai-flags`,{headers:er()}).then(r=>r.ok?r.json():null).then(x=>x&&setD(x)).catch(()=>{})},[]);
 const act=async(id,verdict)=>{if(busy)return;setBusy(id);setErr(``);try{const r=await fetch(`${R}/ai-flags`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({id,verdict})});const x=await r.json().catch(()=>({}));if(r.ok)setD(x);else setErr(x.error||`Could not save`)}catch(e){setErr(`Could not save`)}setBusy(``)};
 if(!d)return(0,L.jsx)(`div`,{className:`content-card af-card`,children:(0,L.jsx)(`div`,{className:`af-empty`,children:`Loading…`})});
 const when=t=>{try{return new Date(t).toLocaleString([],{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`})}catch(e){return``}};
 const open=d.flags.filter(f=>f.status===`open`),done=d.flags.filter(f=>f.status!==`open`);
 const row=f=>(0,L.jsxs)(`div`,{className:`af-row`+(f.status!==`open`?` done`:``),children:[
   (0,L.jsxs)(`div`,{className:`af-top`,children:[(0,L.jsx)(`b`,{children:f.username||`Someone`}),(0,L.jsx)(`span`,{className:`af-why`,children:f.why}),(0,L.jsx)(`span`,{className:`af-when`,children:(f.kind===`post`?`Post`:`Chirp`)+` · `+when(f.created_at)})]}),
   (0,L.jsx)(`div`,{className:`af-text`,children:f.excerpt||``}),
   (0,L.jsxs)(`div`,{className:`af-acts`,children:[
     f.post_id?(0,L.jsx)(I,{to:`/post/${f.post_id}`+(f.kind===`post`?``:`?highlight=${f.target_id}`),className:`mod-tool fs`,children:`Open`}):null,
     f.status===`open`?[(0,L.jsx)(`button`,{type:`button`,className:`mod-tool fs`,disabled:!!busy,onClick:()=>act(f.id,`ok`),children:busy===f.id?`…`:`Not bad`},`ok`),
       (0,L.jsx)(`button`,{type:`button`,className:`mod-tool fs danger`,disabled:!!busy,onClick:()=>act(f.id,`confirm`),children:`Confirm`},`cf`)]
     :(0,L.jsx)(`span`,{className:`af-done`,children:f.status===`ok`?`Not bad: put back`+(f.caged?`, out of The Cage`:``):`Confirmed: kept hidden`+(f.caged?`, in The Cage`:``)})]})]},f.id);
 return(0,L.jsxs)(`div`,{className:`content-card af-card`,children:[
  (0,L.jsxs)(`div`,{className:`af-hd`,children:[(0,L.jsx)(`div`,{className:`su-t`,children:`Flagged by the AI check`}),(0,L.jsx)(`div`,{className:`su-s`,children:d.ai_check===`on`?`AI check is on`:`AI check is off (Settings tab)`})]}),
  err?(0,L.jsx)(`div`,{className:`su-err`,style:{padding:`0 18px`},children:err}):null,
  open.length?open.map(row):(0,L.jsx)(`div`,{className:`af-empty`,children:`Nothing waiting for review.`}),
  done.length?[(0,L.jsx)(`div`,{className:`af-sub`,children:`Reviewed`},`rv`),...done.map(row)]:null]})}
"""
patch("function _SignupLimit(){", COMP + "function _SignupLimit(){", 'AI check card + flagged list')
patch("[`deleted`,`Deleted`,d.length],..._adm?", "[`deleted`,`Deleted`,d.length],[`flagged`,`Flagged`,null],..._adm?", 'Flagged tab')
patch("(0,L.jsx)(_SignupLimit,{},`sul`),", "(0,L.jsx)(_SignupLimit,{},`sul`),(0,L.jsx)(_AiCheck,{},`aic`),", 'switch in Settings')
patch("_adm&&_tb===`settings`&&", "_tb===`flagged`&&(0,L.jsx)(_AiFlags,{},`aif`),_adm&&_tb===`settings`&&", 'flagged tab body')
patch("children:e.icon===`🪽`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}):e.icon}",
      "children:e.icon===`🪽`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,dangerouslySetInnerHTML:{__html:_ppIco(`BIRD`)}}):e.icon===`SHIELD`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#f87171`},dangerouslySetInnerHTML:{__html:_ppIco(`SHIELD`)}}):e.icon}", 'shield badge')
patch("body .lb-ic{", "body .af-card{margin-top:16px;padding:14px 0 6px}body .af-hd{padding:0 18px 10px}body .af-empty{color:#64748b;font-size:13px;padding:10px 18px 14px}body .af-sub{color:#64748b;font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:14px 18px 4px}body .af-row{padding:12px 18px;border-top:1px solid #23252e}body .af-row.done{opacity:.6}body .af-top{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 8px;font-size:13px;color:#e5e7eb}body .af-why{color:#f87171;font-weight:700;font-size:12px}body .af-when{color:#64748b;font-size:12px}body .af-text{margin:8px 0 10px;padding:8px 10px;border-radius:10px;background:#15171d;border:1px solid #2e303a;color:#cbd5e1;font-size:13px;line-height:1.45;white-space:pre-wrap;word-break:break-word}body .af-acts{display:flex;flex-wrap:wrap;gap:6px;align-items:center}body .af-acts a.mod-tool{text-decoration:none}body .af-done{color:#94a3b8;font-size:12px}body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
