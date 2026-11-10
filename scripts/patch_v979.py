#!/usr/bin/env python3
"""Patch v978 -> v979: post page chirp preview shows the conversation's top chirps.
- The server now sends `top`: up to 5 chirps from the whole conversation with 2+ reactions, most reacted
  first (with their reactions, even if they're older than the loaded page).
- Preview: 📌 Pinned (up to 3) then 🔥 Top chirps (up to 5, most reacted at the top, no date dividers).
  If no chirp has 2+ reactions it falls back to 🕒 Latest (5) as before; there's no Latest when there are
  top chirps.
- A faded "Chirp preview" label sits next to the 💬 count.
- Tapping a top chirp that's older than the loaded part of the chat opens the chat and loads back to it."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v978.js'
dst = '_deploy/assets/index-DUcNPOLc-v979.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch('quoted:_qd0}=await e.json();', 'quoted:_qd0,top:_tp0}=await e.json();if(!_un0&&_tp0)_cpTop[r]=_tp0;', 'keep top chirps')
patch('let _nl=0,_np=0,_pmo=0,_df=', 'let _nl=0,_np=0,_pmo=0,_tpOn=!1,_df=', 'flag')
patch('if(_pv){_pmo=_rev.filter(_x=>_x.pinned).length-3;let _ps=_rev.filter(_x=>_x.pinned).slice(0,3),_ls=_rev.filter(_x=>!_x.pinned).slice(0,5);',
      'if(_pv){_pmo=_rev.filter(_x=>_x.pinned).length-3;const _tpl=(_cpTop[r]||[]).filter(_x=>!_x.pinned);_tpOn=_tpl.length>0;let _ps=_rev.filter(_x=>_x.pinned).slice(0,3),_ls=_tpOn?[..._tpl].reverse():_rev.filter(_x=>!_x.pinned).slice(0,5);',
      'top or latest')
patch('if(_pv){if(_i===_nl-1)_st(`🕒 Latest`,_e.created_at);', 'if(_pv){if(_i===_nl-1)_st(_tpOn?`🔥 Top chirps`:`🕒 Latest`,_tpOn?null:_e.created_at);', 'section title')
patch('(0,L.jsx)(`b`,{children:_df(_d)})', '_d?(0,L.jsx)(`b`,{children:_df(_d)}):null', 'title without date')
patch('`rdnew`));if(_next){', '`rdnew`));if(_pv&&_tpOn&&_i<_nl);else if(_next){', 'no date dividers in Top')
patch('"aria-label":`${_cn} chirp${_cn===1?``:`s`}`,children:[(0,L.jsx)(`span`,{children:`💬`}),(0,L.jsx)(`span`,{children:_cn})]})',
      '"aria-label":`${_cn} chirp${_cn===1?``:`s`}`,children:[(0,L.jsx)(`span`,{children:`💬`}),(0,L.jsx)(`span`,{children:_cn})]}),_pv&&(0,L.jsx)(`span`,{className:`cp-label`,children:`Chirp preview`})',
      'header label')
# Focusing a chirp that isn't loaded yet (older top chirp): load back to it
patch('let _go=()=>{let _pp=_id===`__pins__`,', 'let _ft=0,_go=()=>{let _pp=_id===`__pins__`,', 'focus: retry flag')
patch(':_w.querySelector(`[data-comment-id="${_id}"]`);if(!_n)return;',
      ':_w.querySelector(`[data-comment-id="${_id}"]`);if(!_n){if(!_pp&&!_ft){_ft=1;_jmp.current=_id;_older(`to=${encodeURIComponent(_id)}`)}return}',
      'focus: load older chirp')

c += r'''
var _cpTop={};
;(()=>{try{const s=document.createElement(`style`);s.textContent=`.cp-label{font-size:12px;font-weight:600;color:#64748b;margin-left:8px;white-space:nowrap;letter-spacing:.01em}`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
