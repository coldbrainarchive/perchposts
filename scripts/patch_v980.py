#!/usr/bin/env python3
"""Patch v979 -> v980:
1. One reaction per bird per chirp: reacting with a different emoji replaces yours right away on screen
   (the server enforces it by account). Picking the emoji you already have does nothing; tapping your pill
   still removes it.
2. Post page preview: 📌 Pinned (3) -> 🔥 Top chirps (3, 2+ reactions) -> ↩️ Most replied (3, 2+ replies,
   never repeating a top chirp or a pin). 🕒 Latest (5) only when neither section has anything."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v979.js'
dst = '_deploy/assets/index-DUcNPOLc-v980.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch('if(i){let e=o.filter(e=>e!==r);e.length===0?delete a[t]:a[t]=e}else a[t]=[...o,r];return{...n,[e]:a}}',
      'if(i){let e=o.filter(e=>e!==r);e.length===0?delete a[t]:a[t]=e}else{for(const k of Object.keys(a)){if(k===t)continue;const f=a[k].filter(x=>x!==r);f.length?a[k]=f:delete a[k]}a[t]=[...o,r]}return{...n,[e]:a}}',
      'reacting replaces your previous emoji')

patch('quoted:_qd0,top:_tp0}=await e.json();if(!_un0&&_tp0)_cpTop[r]=_tp0;',
      'quoted:_qd0,top:_tp0,replied:_rp0}=await e.json();if(!_un0&&_tp0)_cpTop[r]=_tp0;if(!_un0&&_rp0)_cpRep[r]=_rp0;', 'keep most replied')
patch('let _nl=0,_np=0,_pmo=0,_tpOn=!1,', 'let _nl=0,_np=0,_pmo=0,_tpOn=!1,_nR=0,', 'count var')
patch('const _tpl=(_cpTop[r]||[]).filter(_x=>!_x.pinned);_tpOn=_tpl.length>0;let _ps=_rev.filter(_x=>_x.pinned).slice(0,3),_ls=_tpOn?[..._tpl].reverse():',
      'const _tpl=(_cpTop[r]||[]).filter(_x=>!_x.pinned).slice(0,3),_tid=new Set(_tpl.map(_x=>_x.id)),_rpl=(_cpRep[r]||[]).filter(_x=>!_x.pinned&&!_tid.has(_x.id)).slice(0,3);'
      '_nR=_rpl.length;_tpOn=_tpl.length+_rpl.length>0;let _ps=_rev.filter(_x=>_x.pinned).slice(0,3),_ls=_tpOn?[..._rpl].reverse().concat([..._tpl].reverse()):',
      'top + most replied')
patch('if(_pv){if(_i===_nl-1)_st(_tpOn?`🔥 Top chirps`:`🕒 Latest`,_tpOn?null:_e.created_at);',
      'if(_pv){if(_nR&&_i===_nR-1)_st(`↩️ Most replied`,null);if(_i===_nl-1&&_nl>_nR)_st(_tpOn?`🔥 Top chirps`:`🕒 Latest`,_tpOn?null:_e.created_at);',
      'section titles')
c += '\nvar _cpRep={};\n'
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
