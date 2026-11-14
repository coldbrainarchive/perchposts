#!/usr/bin/env python3
"""Patch v1053 -> v1054: in Your Nest, the level colour moves from a pill around the name to a box around the
whole top section (picture + level name + description), full width like the Hatched / Clan / Worms rows below.
The level name becomes plain text in the level colour."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1053.js'
dst = '_deploy/assets/index-DUcNPOLc-v1054.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('function _BC({col,role,pad,face,badge,title,sub,desc,stats,btn,nest}){',
      'function _BC({col,role,pad,face,badge,title,sub,desc,stats,btn,nest,rc,rtop}){', '_BC takes rank colour')
patch('const head=(0,L.jsxs)(`div`,{className:`bc-head`,children:',
      'const head=(0,L.jsxs)(`div`,{className:`bc-head`+(rc?` bc-rbox`:``)+(rtop?` bc-rtop`:``),style:rc?{"--rc":rc}:void 0,children:', 'head box')
patch('title:(0,L.jsx)(`span`,{className:`bc-rank`+(_rank.n===`Legendary Brood`?` bc-rank-top`:``),style:{"--rc":_rank.c||`#c084fc`},children:_rank.n}),desc:_rank.d',
      'rc:_rank.c||`#c084fc`,rtop:_rank.n===`Legendary Brood`,title:(0,L.jsx)(`span`,{className:`bc-rname`,children:_rank.n}),desc:_rank.d',
      'nest passes rank colour')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.bc-head.bc-rbox{padding:12px 14px;border-radius:16px;border:1.5px solid var(--rc);background:color-mix(in srgb,var(--rc) 10%,#15171d)}
.bc-head.bc-rtop{box-shadow:0 0 14px color-mix(in srgb,var(--rc) 40%,transparent)}
.bc-rbox .bc-name{color:var(--rc)!important}
.bc-rname{font-size:13px;font-weight:800;letter-spacing:.06em;text-transform:uppercase}
.bc-rbox .bc-av{width:58px;height:58px}
.bc-nest .bc-id{gap:4px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
