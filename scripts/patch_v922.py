#!/usr/bin/env python3
"""Patch v921 -> v922: chirp "materializes". The glowing purple pill flies from the compose box to the bubble
spot as before, then keeps growing to the finished chirp's exact size (name header included), still purple
with the pinned glow; its text stays at the bottom where the message sits. On arrival the real chirp
(username + message) fades in through the purple, the purple dissolves, and the pinned glow lingers and
slowly fades (~2s). Replaces v921's header-grow / corner-straighten landing."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v921.js'
dst = '_deploy/assets/index-DUcNPOLc-v922.js'
content = open(src, encoding='utf-8').read()
GLOW = "0 0 0 4px rgba(192,132,252,0.6),0 0 20px rgba(192,132,252,0.8)"
NOGLOW = "0 0 0 0px rgba(192,132,252,0),0 0 0px rgba(192,132,252,0)"
i = content.index("  const tr=bub.getBoundingClientRect(),cs=getComputedStyle(bub)")
j = content.index("  a.onfinish=land;setTimeout(land,800);")
new = ("  const tr=bub.getBoundingClientRect(),cs=getComputedStyle(bub),br=body.getBoundingClientRect(),RR=(parseFloat(getComputedStyle(body).borderTopLeftRadius)||18)+'px';\n"
 "  const g=document.createElement('div');\n"
 "  g.textContent=(text||'').slice(0,400);\n"
 "  g.style.cssText='position:fixed;z-index:2147483000;pointer-events:none;box-sizing:border-box;overflow:hidden;white-space:pre-wrap;word-break:break-word;display:flex;flex-direction:column;justify-content:flex-end;'+\n"
 "   'color:#f8fafc;line-height:1.4;font-family:inherit;border:1px solid rgba(255,255,255,0.07);';\n"
 "  document.body.appendChild(g);\n"
 "  const px=v=>Math.round(v)+'px';\n"
 "  const a=g.animate([\n"
 "   {left:px(fr.left),top:px(fr.top),width:px(fr.width),height:px(fr.height),borderRadius:'28px',background:'#0d0f14',fontSize:'16px',padding:'12px 16px',borderColor:'rgba(255,255,255,0.07)',boxShadow:'" + NOGLOW + "'},\n"
 "   {offset:.25,borderRadius:'28px',background:'#7c3aed',borderColor:'#7c3aed',boxShadow:'" + GLOW + "'},\n"
 "   {offset:.65,left:px(tr.left),top:px(tr.top),width:px(tr.width),height:px(tr.height),borderRadius:'28px',background:'#7c3aed',fontSize:cs.fontSize,padding:cs.padding,borderColor:'#7c3aed',boxShadow:'" + GLOW + "'},\n"
 "   {left:px(br.left),top:px(br.top),width:px(br.width),height:px(br.height),borderRadius:RR,background:'#7c3aed',fontSize:cs.fontSize,padding:cs.padding,borderColor:'#7c3aed',boxShadow:'" + GLOW + "'}\n"
 "  ],{duration:700,easing:'cubic-bezier(.3,.7,.2,1)',fill:'forwards'});\n"
 "  let landed=false;const land=()=>{if(landed)return;landed=true;\n"
 "   done();\n"
 "   const nb=newest();\n"
 "   if(nb)nb.animate([{opacity:0},{opacity:0,offset:.15},{opacity:1}],{duration:900,easing:'ease-in-out'});\n"
 "   const keep={left:px(br.left),top:px(br.top),width:px(br.width),height:px(br.height),borderRadius:RR,fontSize:cs.fontSize,padding:cs.padding};\n"
 "   g.animate([\n"
 "    {...keep,background:'rgba(124,58,237,1)',borderColor:'rgba(124,58,237,1)',color:'rgba(248,250,252,1)',boxShadow:'" + GLOW + "'},\n"
 "    {...keep,offset:.18,background:'rgba(124,58,237,0.92)',borderColor:'rgba(124,58,237,0.92)',color:'rgba(248,250,252,0)',boxShadow:'" + GLOW + "'},\n"
 "    {...keep,offset:.5,background:'rgba(124,58,237,0)',borderColor:'rgba(124,58,237,0)',color:'rgba(248,250,252,0)',boxShadow:'" + GLOW + "'},\n"
 "    {...keep,background:'rgba(124,58,237,0)',borderColor:'rgba(124,58,237,0)',color:'rgba(248,250,252,0)',boxShadow:'" + NOGLOW + "'}\n"
 "   ],{duration:2200,easing:'ease-out',fill:'forwards'}).onfinish=()=>g.remove();\n"
 "  };\n")
content = content[:i] + new + content[j:]
content = content.replace("  a.onfinish=land;setTimeout(land,800);", "  a.onfinish=land;setTimeout(land,1000);")
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
