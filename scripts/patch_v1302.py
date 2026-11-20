#!/usr/bin/env python3
"""Patch v1301 -> v1302: Share sheet feedback + scroller outline.
- In the post scroller the black sheet has only a fine top edge (side lines couldn't reach the keyboard).
- Copy link: the pill turns into a purple check + "Copied", then the sheet closes.
- Send: the message bubble shows a check + "Sent to <huddle>" (purple), then closes; errors show in the bubble (red).
  The note line under the buttons is gone."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1301.js'
dst = '_deploy/assets/index-DUcNPOLc-v1302.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("html.reel-shown .ps-sheet{background:#000;border:1px solid #2a2d36;border-bottom:0}", "html.reel-shown .ps-sheet{background:#000;border-top:1px solid #2a2d36}", 'top edge only')
# state for button / bubble feedback
patch("[note,setNote]=(0,_.useState)(``),", "[note,setNote]=(0,_.useState)(``),[copied,setCopied]=(0,_.useState)(!1),[sent,setSent]=(0,_.useState)(``),[err,setErr]=(0,_.useState)(``),", 'state')
patch("const copy=async()=>{try{await navigator.clipboard.writeText(url);done(`Link copied`)}catch(e){setNote(`Couldn't copy the link`)}};",
      "const copy=async()=>{try{await navigator.clipboard.writeText(url);setCopied(!0);setTimeout(bye,900)}catch(e){setErr(`Couldn't copy the link`)}};", 'copy feedback')
patch("const more=async()=>{try{if(navigator.share){await navigator.share({url});bye()}else{await navigator.clipboard.writeText(url);done(`Link copied`)}}catch(e){}};",
      "const more=async()=>{try{if(navigator.share){await navigator.share({url});bye()}else{await navigator.clipboard.writeText(url);setCopied(!0);setTimeout(bye,900)}}catch(e){}};", 'more fallback')
patch("setBusy(!0);setNote(``);let ok=0,err=``;", "setBusy(!0);setErr(``);let ok=0,er2=``;", 'send start')
patch("if(r.ok)ok++;else{const j=await r.json().catch(()=>({}));err=j.error||`Couldn't send`}}catch(e){err=`Couldn't send`}}",
      "if(r.ok)ok++;else{const j=await r.json().catch(()=>({}));er2=j.error||`Couldn't send`}}catch(e){er2=`Couldn't send`}}", 'send errors')
patch("setBusy(!1);if(ok){const one=sel.length===1&&(hs||[]).find(x=>x.id===sel[0]);done(`Sent to ${one?one.title:ok+` huddles`}`)}else setNote(err===`Caged`?`You're Caged: you can only chirp in The Cage`:err)};",
      "setBusy(!1);if(ok){const one=sel.length===1&&(hs||[]).find(x=>x.id===sel[0]);try{document.activeElement&&document.activeElement.blur()}catch(e){}setSent(`Sent to ${one?one.title:ok+` huddles`}`);setTimeout(bye,1100)}else setErr(er2===`Caged`?`You're Caged: you can only chirp in The Cage`:er2)};", 'send result')
CHK = '<svg viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2.8\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\"><path d=\\"M5 12.5l4.5 4.5L19 7.5\\"/></svg>'
# bubble shows sent / error
patch("(0,L.jsx)(`div`,{className:`ps-bub`,children:(0,L.jsx)(`input`,",
      "(0,L.jsx)(`div`,{className:`ps-bub`+(sent?` ok`:err?` bad`:``),children:sent?(0,L.jsxs)(`span`,{className:`ps-sent`,role:`status`,children:[(0,L.jsx)(`span`,{className:`ps-chk`,dangerouslySetInnerHTML:{__html:\"" + CHK + "\"}}),sent]}):err?(0,L.jsx)(`span`,{className:`ps-err`,role:`alert`,onClick:()=>setErr(``),children:err}):(0,L.jsx)(`input`,", 'bubble states')
# copy pill
patch("(0,L.jsxs)(`button`,{type:`button`,className:`ps-ln`,onClick:copy,children:[",
      "copied?(0,L.jsxs)(`button`,{type:`button`,className:`ps-ln ok`,children:[(0,L.jsx)(`span`,{className:`ps-chk`,dangerouslySetInnerHTML:{__html:\"" + CHK + "\"}}),`Copied`]}):(0,L.jsxs)(`button`,{type:`button`,className:`ps-ln`,onClick:copy,children:[", 'copy pill')
patch("body .ps-note{", "body .ps-chk{display:inline-flex;width:18px;height:18px;color:#c084fc}body .ps-chk svg{width:100%;height:100%}body .ps-ln.ok{color:#e9d5ff;border-color:#c084fc66}body .ps-sent{display:flex;align-items:center;gap:8px;color:#e9d5ff;font-size:15px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}body .ps-bub.ok{border-color:#c084fc66}body .ps-err{color:#fca5a5;font-size:14px;font-weight:600;cursor:pointer}body .ps-bub.bad{border-color:#f8717166}body .ps-note{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
