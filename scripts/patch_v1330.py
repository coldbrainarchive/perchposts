#!/usr/bin/env python3
"""Patch v1329 -> v1330: Flock combines with every other filter.
Picking Flock (Spaces tab) sets ?flock=1 instead of replacing the board, so Flock + a perch tag / region / country /
flock tag works (feed: get-posts activity=1 plus those filters). Flock has its own search-bar chip; picking another
space clears it. Old ?board=activity links still work."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1329.js'
dst = '_deploy/assets/index-DUcNPOLc-v1330.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
# search: Flock sets flock=1; other spaces clear it; board=activity turns into flock
patch("function ee(n){clearTimeout(c.current?._dbt);let i=new URLSearchParams(e);i.set(`board`,n),i.delete(`q`),",
      "function ee(n){clearTimeout(c.current?._dbt);let i=new URLSearchParams(e);if(n===`activity`){i.set(`flock`,`1`);if(i.get(`board`)===`activity`||_SPACES.includes(i.get(`board`)))i.delete(`board`)}else{i.set(`board`,n);if(_SPACES.includes(n))i.delete(`flock`)}i.delete(`q`),", 'flock is its own filter')
patch("_utF=(e.get(`utag`)||``).toLowerCase(),_clearUt=()=>{let n=new URLSearchParams(e);n.delete(`utag`);t(n)},",
      "_utF=(e.get(`utag`)||``).toLowerCase(),_clearUt=()=>{let n=new URLSearchParams(e);n.delete(`utag`);t(n)},_fkF=e.get(`flock`)===`1`,_clearFk=()=>{let n=new URLSearchParams(e);n.delete(`flock`);t(n)},", 'search: flock state')
patch("M=d||f||p||m||q2||_botF||_srt||_utF;", "M=d||f||p||m||q2||_botF||_srt||_utF||_fkF;", 'search: has filter')
patch("dangerouslySetInnerHTML:{__html:_ppIco(`SEARCH`)}}),_utF&&(0,L.jsx)(`button`",
      "dangerouslySetInnerHTML:{__html:_ppIco(`SEARCH`)}}),_fkF&&(0,L.jsx)(`button`,{type:`button`,className:`search-chip board-chip`,onClick:ev=>{ev.stopPropagation(),_clearFk()},style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},children:(0,L.jsx)(Ar,{boardName:(nr.find(x=>x.slug===`activity`)||{}).name||`Flock`,small:!0})}),_utF&&(0,L.jsx)(`button`", 'search: flock chip')
# home feed
patch("_ut=(l.get(`utag`)||``).toLowerCase()", "_ut=(l.get(`utag`)||``).toLowerCase(),_flk=l.get(`flock`)===`1`", 'home: read flock')
patch("if(!u&&!d&&!p&&!_ut&&(!f||_cs)){setTagR(null);_setTgL(!1);return}", "if(!u&&!d&&!p&&!_ut&&!_flk&&(!f||_cs)){setTagR(null);_setTgL(!1);return}", 'home: fetch when flock')
patch("turl=u===`activity`?`${R}/get-posts?activity=1&sort=activity&limit=50`", "turl=(u===`activity`||_flk)?`${R}/get-posts?activity=1&sort=activity&limit=50`", 'home: flock url')
patch("},[u,d,f,p,_cs,_ut,l.get(`flaps`)]),", "},[u,d,f,p,_cs,_ut,_flk,l.get(`flaps`)]),", 'home: deps')
patch(":(u||d||f||p||_bot||_ut)&&TagR!==null?TagR:e,", ":(u||d||f||p||_bot||_ut||_flk)&&TagR!==null?TagR:e,", 'home: use list')
patch("let y=u===`activity`,_y=y||u===`feedback`", "let y=u===`activity`||_flk&&!u,_y=y||_flk||u===`feedback`", 'home: flock sorting')
patch("&&!qT&&!_ut&&_cur!=null", "&&!qT&&!_ut&&!_flk&&_cur!=null", 'home: no load-older')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
