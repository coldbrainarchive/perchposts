#!/usr/bin/env python3
"""Patch v983 -> v984: search dropdown tabs are Spaces / Tags / Regions / Filters.
Spaces: Flock, Huddles, The Cage and your own name pill (your posts). Tags: only the topic tags."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v983.js'
dst = '_deploy/assets/index-DUcNPOLc-v984.js'
c = open(src, encoding='utf-8').read()
a = c.index('_tab===`boards`&&(0,L.jsxs)(`div`,{className:`search-column srch-body`,children:[..._tagGroups(g,')
b = c.index(']}),_tab===`regions`', a)
block = c[a:b]
rs = block.index('_tagGroups(g,') + len('_tagGroups(g,')
re_ = block.index('),(()=>{const _me=Qn();')
render = block[rs:re_]
me = block[re_+2:]            # the (()=>{...your posts pill...})() expression
assert me.startswith('(()=>{const _me=Qn();') and render.startswith('x=>(0,L.jsx)(`button`')
new = ('_tab===`spaces`&&(0,L.jsxs)(`div`,{className:`search-column srch-body`,children:[...g.filter(x=>_SPACES.includes(x.slug)).map(' + render + '),' + me + ']}),'
       '_tab===`boards`&&(0,L.jsxs)(`div`,{className:`search-column srch-body`,children:[...g.filter(x=>!_SPACES.includes(x.slug)).map(' + render + ')')
c = c[:a] + new + c[b:]
old = '[_stb(`boards`,`Tags`),_stb(`regions`,`Regions`),_stb(`filters`,`Filters`)]'
if c.count(old) != 1: print('FAIL tabs'); sys.exit(1)
c = c.replace(old, '[_stb(`spaces`,`Spaces`),_stb(`boards`,`Tags`),_stb(`regions`,`Regions`),_stb(`filters`,`Filters`)]')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
