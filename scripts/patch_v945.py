#!/usr/bin/env python3
"""Patch v944 -> v945:
- Reactions list: the gap above the REACTIONS label now matches the gap between the label and the first row.
- Tapping a bird in the reactions list (menu or long-press sheet) opens that bird's quick-glance card
  (the same sheet as the Bird button: stats, Huddle, See Posts). Your own row isn't tappable."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v944.js'
dst = '_deploy/assets/index-DUcNPOLc-v945.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# Rows can open a bird
patch('function _rxRow(r,i,_a,sm){', 'function _rxRow(r,i,_a,sm,go){const _tap=!!(go&&r.name&&r.name!==`Extinct Bird`&&r.name!==Qn()?.username);', 'row: go param')
patch('return(0,L.jsxs)(`div`,{className:`rx-row`,style:{',
      'return(0,L.jsxs)(`div`,{className:`rx-row${_tap?` tap`:``}`,onClick:_tap?ev=>{ev.stopPropagation();go(r.name)}:void 0,style:{', 'row: click')
patch('function _rxWho(ee,only){', 'function _rxWho(ee,only,go){', 'who: go')
patch('rows.map((r,i)=>_rxRow(r,i,0,1))', 'rows.map((r,i)=>_rxRow(r,i,0,1,go))', 'who rows: go')
patch('function _rxSheet(ee,sel,set){', 'function _rxSheet(ee,sel,set,go){', 'sheet: go')
patch('_rxGroup(ee,cur).map(_rxRow)', '_rxGroup(ee,cur).map((r,i)=>_rxRow(r,i,0,0,go?n=>{set(null);go(n)}:null))', 'sheet rows: go')

# Chirp: who the Bird card is about (null = the chirp's author)
patch('[_rxW,_setRxW]=(0,_.useState)(null),',
      '[_rxW,_setRxW]=(0,_.useState)(null),[_bw,_setBw]=(0,_.useState)(null),'
      '_rxGo=nm=>{_setBw(nm);_setBirdStats(null);y(!1);fetch(`${R}/user-stats?username=${encodeURIComponent(nm)}`).then(r=>r.json()).then(d=>{_setBirdStats(d);_setBirdOpen(!0)}).catch(()=>_setBirdOpen(!0))},',
      'chirp: bird target')
patch('_rxWho(ee,null)', '_rxWho(ee,null,_rxGo)', 'menu list taps')
patch('_rxSheet(ee,_rxW,_setRxW)', '_rxSheet(ee,_rxW,_setRxW,_rxGo)', 'sheet taps')
patch('_setBirdOpen(!1);_setBirdStats(null);', '_setBirdOpen(!1);_setBirdStats(null);_setBw(null);', 'close resets', 2)
patch('(_UserCard,{username:e.username,record:e,stats:_birdStats})', '(_UserCard,{username:_bw||e.username,record:_bw?null:e,stats:_birdStats},_bw||e.username)', 'card user')
patch('/new?huddle=1&invite=${encodeURIComponent(e.username)}', '/new?huddle=1&invite=${encodeURIComponent(_bw||e.username)}', 'huddle link')
patch('/?user=${encodeURIComponent(e.username)}`,style:{display:`block`,flex:1', '/?user=${encodeURIComponent(_bw||e.username)}`,style:{display:`block`,flex:1', 'posts link')

c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.chat-action-sheet:has(+ .rx-who){padding-bottom:2px}
.rx-who{padding-top:0}
.rx-who-lb{padding:4px 2px 2px}
.rx-row.tap{cursor:pointer;-webkit-tap-highlight-color:transparent;transition:filter .12s}
.rx-row.tap:active{filter:brightness(1.35)}
@media (hover:hover){.rx-row.tap:hover{filter:brightness(1.2)}}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
