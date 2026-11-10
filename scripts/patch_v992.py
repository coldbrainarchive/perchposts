#!/usr/bin/env python3
"""Patch v991 -> v992: bird ID card redesign, styled like the notification pills.
One shared card (_BC) for all three places: the quick-glance pop-up, the bird header on See Posts, and the Nest.
- The card is tinted, outlined and softly glowing in the bird's own colour (like an unread notification).
- Header: a tinted avatar circle like a notification's. For other birds it holds their bird, with the rank emoji
  as the corner badge, and their name (bold, in their colour) and rank sit beside it. In the Nest it holds your
  evolution emoji, with the evolution name and its line beside it (your bird is already shown above).
- Hatched / Clan / Worms are stacked pills (label left, value right) instead of a grid. Date stays numeric.
- "Tap to close" is gone from the pop-ups (tapping outside still closes them)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v991.js'
dst = '_deploy/assets/index-DUcNPOLc-v992.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
def span(start, end, new, label):
    global c
    i = c.find(start)
    if i < 0 or c.count(start) != 1: print('FAIL start', label, c.count(start)); sys.exit(1)
    j = c.find(end, i)
    if j < 0: print('FAIL end', label); sys.exit(1)
    c = c[:i] + new + c[j:]; print('OK:', label, j - i, 'chars replaced')

# 1. _UserCard body -> shared card
span('return(0,L.jsxs)(`div`,{style:_om?{padding:`10px 0 16px`}',
     '}\nfunction _Si(){',
     'return _BC({col:_resolvedCol,role:_isAdmin?`admin`:_isMod?`mod`:null,pad:_om?`10px 0 16px`:`10px 14px`,'
     'face:_bd&&_bd.hat?(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{width:44,height:44,objectFit:`contain`}}):(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-flex`,fontSize:38,lineHeight:1},children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``},children:_bd&&_bd.e?_bd.e:`🐤`}),...(_bd&&_bd.s?_spEls(_bd.s,38):[])]}),'
     'badge:_rk?_rk.e:`🐣`,title:_un,sub:_rk?_rk.n:null,'
     'stats:[[`🥚`,`Hatched`,_hd],_clan?[_clan.e,`Clan`,_clan.n]:null,[`🪱`,`Worms`,_wc]],'
     'btn:_om&&_me&&_me!==_un?(0,L.jsx)(`button`,{type:`button`,className:`bc-btn`,onClick:()=>_om(_un,_br),children:`Huddle`}):null});',
     'user card uses shared card')

# 2. Nest card -> shared card (evolution in the header)
span('e?(0,L.jsxs)(`div`,{className:`content-card`,style:{display:`flex`,flexDirection:`column`,gap:10},children:[(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:10},children:[(0,L.jsx)(`div`,{style:{fontSize:36',
     ':null,O&&(0,L.jsxs)(L.Fragment',
     'e?_BC({col:t===`admin`?`#ffffff`:t===`mod`?`#c084fc`:A,pad:`0`,nest:!0,face:(0,L.jsx)(`span`,{style:{fontSize:36,lineHeight:1},children:_rank.e}),'
     'title:_rank.n,desc:_rank.d,stats:[[`🥚`,`Hatched`,_hd||`—`],_clanN?[_clanN.e,`Clan`,_clanN.n]:null,[`🪱`,`Worms`,_wc]]})',
     'nest card uses shared card')

# 3. Drop "Tap to close" rows in both pop-ups
patch('(0,L.jsx)(`div`,{style:{padding:`10px 16px 4px`,display:`flex`,justifyContent:`center`},children:(0,L.jsx)(`button`,{onClick:()=>{_setBirdOpen(!1);_setBirdStats(null);_setBw(null);},style:{background:`none`,border:`none`,color:`#64748b`,fontSize:12,fontWeight:600,cursor:`pointer`,padding:0},children:`Tap to close`})}),',
      '(0,L.jsx)(`div`,{className:`bc-grab`}),', 'chat pop-up: no Tap to close')
patch('(0,L.jsx)(`div`,{style:{padding:`10px 16px 4px`,display:`flex`,justifyContent:`center`},children:(0,L.jsx)(`button`,{onClick:()=>{_setGpBird(null);_setGpStats(null);},style:{background:`none`,border:`none`,color:`#64748b`,fontSize:12,fontWeight:600,cursor:`pointer`,padding:0},children:`Tap to close`})}),',
      '(0,L.jsx)(`div`,{className:`bc-grab`}),', 'global pop-up: no Tap to close')

# 4. New-chirps pill hides while a bird card pop-up is open
patch('_birdOpen?(0,L.jsxs)(`div`,{onClick:', '_birdOpen?(0,L.jsxs)(`div`,{className:`bc-sheet`,onClick:', 'chat pop-up class')
patch('_gpBird&&_gpStats?(0,L.jsxs)(`div`,{onClick:', '_gpBird&&_gpStats?(0,L.jsxs)(`div`,{className:`bc-sheet`,onClick:', 'global pop-up class')

c += r'''
function _BC({col,role,pad,face,badge,title,sub,desc,stats,btn,nest}){const k=col||`#c084fc`,mx=(p,b)=>`color-mix(in srgb, ${k} ${p}%, ${b||`transparent`})`;
 const globe=role?(0,L.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 100 100`,style:{flexShrink:0},children:[(0,L.jsx)(`circle`,{cx:50,cy:50,r:44,fill:`none`,stroke:k,strokeWidth:8}),(0,L.jsx)(`line`,{x1:6,y1:50,x2:94,y2:50,stroke:k,strokeWidth:7}),(0,L.jsx)(`ellipse`,{cx:50,cy:50,rx:20,ry:44,fill:`none`,stroke:k,strokeWidth:7})]}):null;
 const av=(0,L.jsxs)(`div`,{className:`bc-av`,style:{background:mx(26,`#1b1d24`),border:`1px solid ${mx(45)}`},children:[face,badge?(0,L.jsx)(`span`,{className:`bc-badge`,children:badge}):null]});
 const head=(0,L.jsxs)(`div`,{className:`bc-head`,children:[av,(0,L.jsxs)(`div`,{className:`bc-id`,children:[
  (0,L.jsxs)(`div`,{className:`bc-name`,style:{color:k===`#ffffff`?`#f1f5f9`:k},children:[(0,L.jsx)(`span`,{className:`bc-nt`,children:title}),globe]}),
  sub?(0,L.jsx)(`div`,{className:`bc-sub`,children:sub}):null,desc?(0,L.jsx)(`div`,{className:`bc-desc`,children:desc}):null]})]});
 const rows=(0,L.jsx)(`div`,{className:`bc-rows`,children:stats.filter(Boolean).map(([e,l,v])=>(0,L.jsxs)(`div`,{className:`bc-row`,style:{background:mx(6,`#15171d`),border:`1px solid ${mx(16)}`},children:[(0,L.jsxs)(`span`,{className:`bc-l`,children:[(0,L.jsx)(`span`,{className:`bc-e`,children:e}),l]}),(0,L.jsx)(`span`,{className:`bc-v`,children:v})]},l))});
 const card=(0,L.jsxs)(`div`,{className:`bc-card`+(nest?` bc-nest`:``),style:{background:mx(12,`#15171d`),border:`1px solid ${mx(70)}`,boxShadow:`0 0 0 1px ${mx(25)}, 0 0 22px ${mx(32)}`},children:[head,rows,btn]});
 return(0,L.jsx)(`div`,{style:{padding:pad,maxWidth:480,margin:`0 auto`,width:`100%`,boxSizing:`border-box`},children:card})}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.bc-card{border-radius:22px;padding:14px;display:flex;flex-direction:column;gap:12px;text-align:left}
.bc-head{display:flex;align-items:center;gap:14px;padding:2px 2px 0}
.bc-av{position:relative;flex-shrink:0;width:64px;height:64px;border-radius:999px;display:flex;align-items:center;justify-content:center}
.bc-badge{position:absolute;right:-4px;bottom:-3px;width:26px;height:26px;border-radius:999px;background:#1b1d24;border:1px solid #2e303a;display:flex;align-items:center;justify-content:center;font-size:15px;line-height:1}
.bc-id{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}
.bc-name{display:flex;align-items:center;gap:6px;font-size:16px;font-weight:800;line-height:1.25;min-width:0}
.bc-nt{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}
.bc-sub{font-size:13px;font-weight:600;color:#94a3b8}
.bc-desc{font-size:12.5px;color:#8b98a9;font-style:italic;line-height:1.4}
.bc-rows{display:flex;flex-direction:column;gap:7px}
.bc-row{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 14px;border-radius:16px}
.bc-l{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:#94a3b8;white-space:nowrap}
.bc-e{font-size:16px;line-height:1;width:20px;text-align:center}
.bc-v{font-size:14px;font-weight:700;color:#f1f5f9;text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}
.bc-btn{margin-top:2px;padding:11px 12px;border-radius:14px;line-height:18px;border:none;background:#c084fc;color:#14081d;font-weight:700;font-size:14px;font-family:inherit;cursor:pointer}
body:has(.bc-sheet) .rd-pill{display:none!important}
.bc-grab{width:38px;height:5px;border-radius:999px;background:#3a3d48;margin:10px auto 4px}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
