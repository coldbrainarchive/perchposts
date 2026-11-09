#!/usr/bin/env python3
"""Patch v919 -> v920: the chirp send animation keeps the compose box's pill shape in flight, in the send
button's purple (#7c3aed) with the pinned-chirp glow (4px ring + 20px glow). It only eases into the bubble's
corners at the very end. On landing the name header grows up out of the top of the bubble, and the pinned
glow + purple fade slowly back to the normal bubble (~1.8s)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v919.js'
dst = '_deploy/assets/index-DUcNPOLc-v920.js'
content = open(src, encoding='utf-8').read()
GLOW = "0 0 0 4px rgba(192,132,252,0.6),0 0 20px rgba(192,132,252,0.8)"
NOGLOW = "0 0 0 0px rgba(192,132,252,0),0 0 0px rgba(192,132,252,0)"
i = content.index("  const a=g.animate([")
j = content.index("  a.onfinish=land;setTimeout(land,800);")
new = ("  const a=g.animate([\n"
 "   {left:px(fr.left),top:px(fr.top),width:px(fr.width),height:px(fr.height),borderRadius:'28px',background:'#0d0f14',fontSize:'16px',padding:'12px 16px',borderColor:'rgba(255,255,255,0.07)',boxShadow:'" + NOGLOW + "'},\n"
 "   {offset:.3,borderRadius:'28px',background:'#7c3aed',borderColor:'#7c3aed',boxShadow:'" + GLOW + "'},\n"
 "   {offset:.85,left:px(tr.left),top:px(tr.top),width:px(tr.width),height:px(tr.height),borderRadius:'28px',background:'#7c3aed',fontSize:cs.fontSize,padding:cs.padding,borderColor:'#7c3aed',boxShadow:'" + GLOW + "'},\n"
 "   {left:px(tr.left),top:px(tr.top),width:px(tr.width),height:px(tr.height),borderRadius:cs.borderRadius,background:'#7c3aed',fontSize:cs.fontSize,padding:cs.padding,borderColor:'#7c3aed',boxShadow:'" + GLOW + "'}\n"
 "  ],{duration:520,easing:'cubic-bezier(.3,.7,.2,1)',fill:'forwards'});\n"
 "  let landed=false;const land=()=>{if(landed)return;landed=true;\n"
 "   done();\n"
 "   const nb=newest();const b2=nb&&(nb.querySelector('.chat-bubble')||nb);const mt=nb&&nb.querySelector('.chat-msg-meta');\n"
 "   if(mt){mt.style.transformOrigin='50% 100%';mt.animate([{transform:'scaleY(0)',opacity:0},{transform:'scaleY(1.08)',opacity:1,offset:.7},{transform:'scaleY(1)',opacity:1}],{duration:320,easing:'cubic-bezier(.3,.7,.2,1)'})}\n"
 "   if(b2){const to=getComputedStyle(b2).backgroundColor;b2.animate([{background:'#7c3aed',boxShadow:'" + GLOW + "'},{background:'#7c3aed',boxShadow:'" + GLOW + "',offset:.3},{background:to,boxShadow:'" + NOGLOW + "'}],{duration:1800,easing:'ease-out'})}\n"
 "   g.animate([{opacity:1},{opacity:0}],{duration:120,easing:'ease-out',fill:'forwards'}).onfinish=()=>g.remove();\n"
 "  };\n")
content = content[:i] + new + content[j:]
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
