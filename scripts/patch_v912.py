#!/usr/bin/env python3
"""Patch v911 -> v912: the signed-in bird's own name pill sits at the bottom of the Boards tab (under a thin
divider). Tapping it filters the feed to their own posts (?user=<name>), like tapping a name anywhere else."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v911.js'
dst = '_deploy/assets/index-DUcNPOLc-v912.js'
content = open(src, encoding='utf-8').read()
old = ("_tab===`boards`&&(0,L.jsx)(`div`,{className:`search-column srch-body`,children:g.map(x=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>ee(x.slug),children:(0,L.jsx)(Ar,{boardName:x.name,small:!0})},x.slug))}),")
new = ("_tab===`boards`&&(0,L.jsxs)(`div`,{className:`search-column srch-body`,children:[...g.map(x=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>ee(x.slug),children:(0,L.jsx)(Ar,{boardName:x.name,small:!0})},x.slug)),"
       "(()=>{const _me=Qn();const _mn=_me&&_me.username;if(!_mn)return null;"
       "return(0,L.jsx)(`div`,{key:`_me`,style:{flexBasis:`100%`,display:`flex`,justifyContent:`center`,borderTop:`1px solid #374151`,paddingTop:8,marginTop:2},"
       "children:(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,title:`Your posts`,"
       "onClick:()=>{clearTimeout(c.current?._dbt);let n=new URLSearchParams(e);n.set(`user`,_mn);n.delete(`q`);t(n);r(``);s(null);a(!1);if(c.current){c.current.value=``;c.current.blur()}},"
       "children:(0,L.jsx)(Xn,{record:{username:_mn,browser_id:Gn(),is_admin:_me.role===`admin`,is_mod:_me.role===`mod`},name:_mn,color:Hn(Gn(),_mn)})})})})()]}),")
if content.count(old) != 1: print('FAIL', content.count(old)); sys.exit(1)
content = content.replace(old, new)
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
