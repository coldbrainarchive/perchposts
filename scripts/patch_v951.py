#!/usr/bin/env python3
"""Patch v950 -> v951: no duplicate for pinned chirps that open the chat.
Pinned chirps at the very start of the chat (before anyone else said anything; huddle join/leave notices
don't count) only show in the pinned area, which sits right above the first chirp anyway. They act as the
real chirp there (keep data-comment-id, so jumps/notifications land on them) and have no Find (nothing to
find), unless they're a reply, where Find still goes to the parent. Only applies once the start of the chat
is loaded; before that, older pins already stay in the pinned area only."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v950.js'
dst = '_deploy/assets/index-DUcNPOLc-v951.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('const _R=(_e,_pc,_k,_px)=>(0,L.jsx)(Rr,{pinCopy:_pc,pinX:_px,comment:_e,',
      'const _R=(_e,_pc,_k,_px,_so)=>(0,L.jsx)(Rr,{pinCopy:_pc,pinX:_px,pinSolo:!!_so,comment:_e,', 'builder: solo flag')
patch('let _pins=[];if(!_pv){_pins=_rev.filter(x=>x.pinned);',
      'let _pins=[],_solo=new Set();if(!_pv){_pins=_rev.filter(x=>x.pinned);'
      'if(!_hmR.current){for(const x of [..._rev].sort((a,b)=>new Date(a.created_at)-new Date(b.created_at))){if(x.username===`__system__`)continue;if(!x.pinned)break;_solo.add(x.id)}}',
      'find opening pins')
patch('_rev=_rev.filter(x=>!x.pinned||!_hmR.current||new Date(x.created_at).getTime()>=_mn)}',
      '_rev=_rev.filter(x=>!_solo.has(x.id)&&(!x.pinned||!_hmR.current||new Date(x.created_at).getTime()>=_mn))}',
      'timeline skips opening pins')
patch('_out.push(_R(_p2[k],!0,`pc-`+_p2[k].id,k>=3));', '_out.push(_R(_p2[k],!0,`pc-`+_p2[k].id,k>=3,_solo.has(_p2[k].id)));', 'copies: solo')
patch('function Rr({pinCopy:_pc=!1,pinX:_px=!1,', 'function Rr({pinCopy:_pc=!1,pinX:_px=!1,pinSolo:_ps1=!1,', 'Rr: prop')
patch('"data-comment-id":_pc?void 0:e.id,"data-pin-of":_pc?e.id:void 0,',
      '"data-comment-id":_pc&&!_ps1?void 0:e.id,"data-pin-of":_pc&&!_ps1?e.id:void 0,', 'Rr: solo is the real chirp')
patch('(_pc||w)&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1),d&&d(_pc?e.id:e.parent_comment_id)},children:`Find`})',
      '(_pc&&!_ps1||w)&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1),d&&d(_pc&&!_ps1?e.id:e.parent_comment_id)},children:`Find`})',
      'Rr: no Find on solo')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
