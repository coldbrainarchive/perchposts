#!/usr/bin/env python3
"""Patch v1129 -> v1130: tapping a reaction on a chirp shows who did it, right in the chirp's dropdown.
- Tapping any pill (an emoji, the 🪱, or "…") opens the chirp's dropdown (Reply / React / ...) with the who-reacted
  list for that pill. The pill is highlighted. Tap another pill to switch; tap the highlighted one again for everyone.
- Tapping a pill no longer adds or removes your reaction. React → pick an emoji you already used to take it back.
- The dark who-reacted sheet is gone."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1129.js'
dst = '_deploy/assets/index-DUcNPOLc-v1130.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# who list: filter by a pill, and "+N more" expands in place
patch("function _rxWho(ee,only,go,more,wg){", "function _rxWho(ee,only,go,more,wg,nocap){", 'who list: no-cap flag')
patch("const _extra=rows.length>5?rows.length-5:0;", "const _extra=!nocap&&rows.length>5?rows.length-5:0;", 'who list: expand')
patch("function _RxWhoC({ee,cid,go,more}){const wn=_ppWorm.n(_ppWorm.key(`c`,cid)),g=_useWG(cid,wn>0);return _rxWho(ee,null,go,more,wn>0?g:null)}",
      "function _RxWhoC({ee,cid,go,only}){const wn=_ppWorm.n(_ppWorm.key(`c`,cid)),g=_useWG(cid,wn>0),[all,setAll]=(0,_.useState)(!1),f=only&&only!==`all`?only:null,more=()=>setAll(!0),G=wn>0?g:null;\n"
      " return f===`🪱`?_rxWho([],null,go,more,G,all):f?_rxWho(ee,f,go,more,null,all):_rxWho(ee,null,go,more,G,all)}", 'who list follows the pill')
patch("v&&(0,L.jsx)(_RxWhoC,{ee,cid:e.id,go:_rxGo,more:()=>_setRxW(`all`)})", "v&&(0,L.jsx)(_RxWhoC,{ee,cid:e.id,go:_rxGo,only:_rxW},_rxW||`all`)", 'dropdown list uses the pill')
# no more dark sheet
patch("_rxW?_rxSheet(ee,_rxW,_setRxW,_rxGo,e.id):null", "null", 'no dark sheet')
# pills select instead of reacting
PICK = "{if(v&&_rxW===%s){_setRxW(null)}else{_setRxW(%s);y(!0)}}"
patch("onPointerDown:ev=>_rxLPStart(ev,()=>_setRxW(t)),onPointerUp:_rxLPEnd,onPointerLeave:_rxLPEnd,onPointerCancel:_rxLPEnd,onContextMenu:ev=>{ev.preventDefault();_rxLPEnd();_rxF=Date.now();_setRxW(t)},onClick:()=>{if(_rxLPFired())return;let _m=n.includes(C);c&&c(e.id,t);_m||_rxPop(e.id,t,null)},",
      "onClick:ev=>{ev.stopPropagation();" + (PICK % ("t","t"))[1:] + ",",
      'emoji pill shows who')
patch("className:`chat-reaction-pill${n.includes(C)?` mine`:``}`,\"data-emoji\":t,", "className:`chat-reaction-pill${n.includes(C)?` mine`:``}${v&&_rxW===t?` sel`:``}`,\"data-emoji\":t,", 'selected emoji pill')
patch("onClick:ev=>{ev.stopPropagation();_setRxW(`all`)}},`__more`)", "onClick:ev=>{ev.stopPropagation();_setRxW(null);y(!0)}},`__more`)", '… opens everyone')
patch("(0,L.jsx)(_WormPill,{k:`c`,id:e.id,chirp:1,onOpen:()=>_setRxW(`all`)})", "(0,L.jsx)(_WormPill,{k:`c`,id:e.id,chirp:1,sel:v&&_rxW===`🪱`,onOpen:()=>" + PICK % ("`🪱`","`🪱`") + "})", 'worm pill shows givers')
patch("(0,L.jsx)(_WormPill,{k:`c`,id:e.id,chirp:1,solo:1,onOpen:()=>_setRxW(`all`)})", "(0,L.jsx)(_WormPill,{k:`c`,id:e.id,chirp:1,solo:1,sel:v&&_rxW===`🪱`,onOpen:()=>" + PICK % ("`🪱`","`🪱`") + "})", 'solo worm pill shows givers')
patch("function _WormPill({k,id,chirp,solo,onOpen}){", "function _WormPill({k,id,chirp,solo,onOpen,sel}){", 'worm pill: sel')
patch("className:(chirp?`chat-reaction-pill pp-worm-pill`:`feed-post-action-pill pp-worm-pill`)+(m?` mine`:``)", "className:(chirp?`chat-reaction-pill pp-worm-pill`:`feed-post-action-pill pp-worm-pill`)+(m?` mine`:``)+(sel?` sel`:``)", 'worm pill highlight')
# closing the dropdown forgets the pill
patch("className:`chat-bubble${p?` pending`:``}`,onClick:()=>!p&&y(e=>!e),", "className:`chat-bubble${p?` pending`:``}`,onClick:()=>{if(p)return;_setRxW(null);y(e=>!e)},", 'tap chirp resets the pill')
# React picker: picking your own emoji again takes it back
patch(" _rxIos(q=>{if((E[q]||[]).includes(me))return;react(id,q);_rxPop(id,q,null)},_src,{kind:`c`,id})}",
      " _rxIos(q=>{const had=(E[q]||[]).includes(me);react(id,q);had||_rxPop(id,q,null)},_src,{kind:`c`,id})}", 'picker toggles your emoji')
patch("body .lb-ic{", "body .chat-reaction-pill.sel{border-color:#c084fc!important;background:rgba(192,132,252,.22)!important;box-shadow:0 0 0 1px #c084fc}body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
