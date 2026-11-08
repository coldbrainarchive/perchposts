#!/usr/bin/env python3
"""Patch v829 -> v830: chats load the latest 100 chirps and 100 more as you scroll up, like the feed.
Polls keep whatever is loaded (from). Pinned chirps always come with the page, and quoted chirps older
than the page come separately (quoted), for the quote only. Notifications ask the server to reach back
to their chirp (to, to_user, or all for system lines) so it's on the page before the jump. Find does the
same when its chirp isn't loaded, then jumps and flashes. Oldest loads everything, since that's what it
promises. The count comes from the server. A newer request always wins, so a slow poll can't shrink
the page, and polling waits while older chirps load.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v829.js'
dst = '_deploy/assets/index-DUcNPOLc-v830.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label, count=1):
    global content
    n = content.count(old)
    if n != count:
        errors.append('FAIL (' + label + '): expected ' + str(count) + ' matches, found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

def t(s):
    return s.replace('`', q)

patch(t('_pk=(0,_.useRef)(null),_qt=(0,_.useRef)(0);'),
      t('_pk=(0,_.useRef)(null),_qt=(0,_.useRef)(0),_fr=(0,_.useRef)(null),_nx=(0,_.useRef)(null),_rid=(0,_.useRef)(0),_lo=(0,_.useRef)(!1),_hmR=(0,_.useRef)(!1),_jmp=(0,_.useRef)(null),_hd=(0,_.useRef)(!1),_fa=(0,_.useRef)(null),[_tot,_setTot]=(0,_.useState)(null),[_qd,_setQd]=(0,_.useState)([]),[_ldO,_setLdO]=(0,_.useState)(!1);_fa.current=[a,_nc,_sy];'),
      'paging state')

patch(t('if(_pk.current)_gpUrl+=`&v=${_pk.current}`;if(_un2)_gpUrl+=`&req_username=${encodeURIComponent(_un2)}`;let e=await fetch(_gpUrl,{headers:er()});'),
      t('let _op=_nx.current,[_ha,_hn,_hs]=_fa.current;_nx.current=null;_gpUrl+=`&limit=100`;if(_fr.current!==null)_gpUrl+=`&from=${encodeURIComponent(_fr.current)}`;if(_op)_gpUrl+=`&${_op}`;else{if(_pk.current)_gpUrl+=`&v=${_pk.current}`;if(_hs)_gpUrl+=`&all=1`;else if(_ha)_gpUrl+=`&to=${encodeURIComponent(_ha)}`;else if(_hn)_gpUrl+=`&to_user=${encodeURIComponent(_hn)}`}if(_un2)_gpUrl+=`&req_username=${encodeURIComponent(_un2)}`;let _rq=++_rid.current,e=await fetch(_gpUrl,{headers:er()});'),
      'request')
patch(t('let{post:t,comments:n,reactions:_rx,unchanged:_un0,version:_ver}=await e.json();if(_un0){'),
      t('let{post:t,comments:n,reactions:_rx,unchanged:_un0,version:_ver,from:_fr0,has_more:_hm0,comment_total:_tt,quoted:_qd0}=await e.json();if(_rq!==_rid.current)return;if(_un0){'),
      'response')
patch(t('_qt.current=0;_pk.current=_ver||null;l(Cr(t));'),
      t('_qt.current=0;_pk.current=_ver||null;if(_fr0!==void 0)_fr.current=_fr0;_hmR.current=!!_hm0;_setTot(_tt??null);_setQd(_qd0||[]);l(Cr(t));'),
      'apply response')

patch(t('_pv=()=>{_tk++;if(document.hidden||_qt.current>30&&_tk%5)return;P()}'),
      t('_pv=()=>{_tk++;if(document.hidden||_lo.current||_qt.current>30&&_tk%5)return;P()}'),
      'polling waits for older chirps')
patch(t('(0,_.useEffect)(()=>{let e=D.current;if(!e||!u.length)return;if(!_isd.current)'),
      t('(0,_.useEffect)(()=>{(a||_nc||_sy)&&_pk.current&&P()},[a,_nc,_sy]),(0,_.useEffect)(()=>{let _id=_jmp.current,t=D.current;if(!_id||!t)return;let n=t.querySelector(`[data-comment-id="${_id}"]`);if(!n)return;_jmp.current=null;_hd.current=!0;requestAnimationFrame(()=>{let _a=n.getBoundingClientRect(),_w=t.getBoundingClientRect();t.scrollTop+=_a.top-_w.top-(t.clientHeight-_a.height)/2;_glow(n.querySelector(`.chat-msg-body`)||n)})},[u]),(0,_.useEffect)(()=>{let e=D.current;if(!e||!u.length)return;if(!_isd.current)'),
      'jump effects')

patch(t('_closeC=()=>history.back();'),
      t('_closeC=()=>history.back(),_older=async _o=>{if(_lo.current||!_hmR.current)return;_lo.current=!0;_setLdO(!0);_nx.current=_o||`older=1`;try{await P()}finally{_lo.current=!1;_setLdO(!1)}};'),
      'load older')
patch(t('(0,_.useEffect)(()=>{_cfR.current=!1;_ckR.current=null;_setCF(!1)},[r]);'),
      t('(0,_.useEffect)(()=>{_cfR.current=!1;_ckR.current=null;_setCF(!1);_fr.current=null;_pk.current=null;_hmR.current=!1;_jmp.current=null;_setTot(null);_setQd([])},[r]);'),
      'reset for a new post')

patch(t('onScroll:()=>{let e=D.current;e&&(O.current=Math.abs(e.scrollTop)<60)}'),
      t('onScroll:()=>{let e=D.current;if(!e)return;O.current=Math.abs(e.scrollTop)<60;!_pv&&!_hd.current&&e.scrollHeight-e.clientHeight-Math.abs(e.scrollTop)<600&&_older()}'),
      'load on scroll')
# A jump near the top must not load more, because older chirps land between it and a pinned chirp
patch(t('_wk=()=>{_qt.current=0},'), t('_wk=()=>{_qt.current=0;_hd.current=!1},'), 'touch ends the hold')
patch(t('document.addEventListener(`pointerdown`,_wk,!0);'), t('document.addEventListener(`pointerdown`,_wk,!0);document.addEventListener(`wheel`,_wk,{capture:!0,passive:!0});'), 'wheel ends the hold')
patch(t('return()=>{document.removeEventListener(`pointerdown`,_wk,!0);'), t('return()=>{document.removeEventListener(`pointerdown`,_wk,!0);document.removeEventListener(`wheel`,_wk,!0);'), 'remove wheel listener')
patch(t('if(!t)return;requestAnimationFrame(()=>{t.scrollIntoView({block:`center`,behavior:`instant`});let _b=t?.querySelector'), t('if(!t)return;_hd.current=!0;requestAnimationFrame(()=>{t.scrollIntoView({block:`center`,behavior:`instant`});let _b=t?.querySelector'), 'hold for notifications')
patch(t('let _id=_fid.current,_w=D.current;_fid.current=null;if(!_w)return;'), t('let _id=_fid.current,_w=D.current;_fid.current=null;if(!_w)return;_hd.current=!0;'), 'hold for preview taps')
patch(t('if(_np&&_i===_rev.length-1)_st(`📌 Pinned`,_e.created_at)}});return _out;})()]})'),
      t('if(_np&&_i===_rev.length-1)_st(`📌 Pinned`,_e.created_at)}});_ldO&&!_pv&&_out.push((0,L.jsx)(_Bd,{},`ldo`));return _out;})()]})'),
      'bird while loading')

patch(t('onClick:()=>{let e=D.current;if(e&&e.lastElementChild){e.lastElementChild.scrollIntoView();x(!1);}},children:`Oldest`'),
      t('onClick:async()=>{await _older(`all=1`);requestAnimationFrame(()=>requestAnimationFrame(()=>{let e=D.current;if(e&&e.lastElementChild){e.lastElementChild.scrollIntoView();x(!1);}}))},children:`Oldest`'),
      'oldest')
patch(t('onFindParent:e=>{let t=D.current,n=t?.querySelector(`[data-comment-id="${e}"]`);if(t&&n){'),
      t('onFindParent:e=>{let t=D.current,n=t?.querySelector(`[data-comment-id="${e}"]`);if(t&&!n){_jmp.current=e;_older(`to=${encodeURIComponent(e)}`)}if(t&&n){_hd.current=!0;'),
      'find older chirp')
patch(t('ue=[...u,...g],de=[...ue]'), t('ue=[...u,...g],_ua=[...ue,..._qd],de=[...ue]'), 'quoted chirps')
patch(t('allComments:ue,onFindParent'), t('allComments:_ua,onFindParent'), 'quote lookup')
patch(t('_cn=u.filter(_c=>_c.username!==`__system__`).length,'), t('_cn=_tot??u.filter(_c=>_c.username!==`__system__`).length,'), 'true count')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
