#!/usr/bin/env python3
"""Patch v1121 -> v1122:
- The bird is purple only when YOU flapped, so tapping always visibly flaps / un-flaps (giving worms used to keep it
  purple, which made un-flapping look broken). The number still counts everyone who flapped or gave worms.
- No more press-and-hold on the bird. Worms for posts are given in the Reactions view (the chirp preview's dropdown on
  phones; the 🪱 pill next to the bird, now always shown, opens it anywhere): a Give worms row with your balance.
  Chirps keep the worm in their reaction bar."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1121.js'
dst = '_deploy/assets/index-DUcNPOLc-v1122.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# purple = your flap only
patch("style:r>=1&&i?{borderColor:`#c084fc`", "style:r===1&&i?{borderColor:`#c084fc`", 'card purple = flapped')
patch("style:re.myVote>=1?{borderColor:`#c084fc`", "style:re.myVote===1?{borderColor:`#c084fc`", 'post page purple = flapped')

# no press-and-hold
i = c.index("// press and hold the bird on a post: the picker (a plain tap still flaps)"); j = c.index("// who did what on a post", i)
c = c[:i] + c[j:]; print('OK: hold removed')

# a Give worms row (React) for the Reactions view
give = r'''function _WormGive({id}){const[bal,setBal]=(0,_.useState)(_ppWorm.bal()),[n,setN]=(0,_.useState)(1),me=(localStorage.getItem(`_myUsername`)||``).toLowerCase(),signed=!!localStorage.getItem(`auth_token`);
 (0,_.useEffect)(()=>{if(signed)_ppWorm.loadBal().then(v=>setBal(v))},[id]);
 if(!signed)return(0,L.jsxs)(`button`,{type:`button`,className:`wg-row wg-out`,onClick:ev=>{ev.stopPropagation();window.dispatchEvent(new CustomEvent(`like-no-auth`))},children:[(0,L.jsx)(`span`,{className:`pp-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),`Sign in to give worms`]});
 const k=bal==null?n:Math.max(1,Math.min(n,bal||1)),none=bal===0;
 return(0,L.jsxs)(`div`,{className:`wg-row`,onClick:ev=>ev.stopPropagation(),children:[(0,L.jsxs)(`div`,{className:`wg-top`,children:[
  (0,L.jsx)(`span`,{className:`pp-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),(0,L.jsx)(`span`,{className:`wg-l`,children:`Give worms`}),
  (0,L.jsx)(`button`,{type:`button`,className:`pp-pick-st`,disabled:k<=1||none,"aria-label":`Fewer`,onClick:()=>setN(Math.max(1,k-1)),children:`−`}),(0,L.jsx)(`b`,{className:`pp-pick-n`,children:k}),
  (0,L.jsx)(`button`,{type:`button`,className:`pp-pick-st`,disabled:none||(bal!=null&&k>=bal)||k>=50,"aria-label":`More`,onClick:()=>setN(k+1),children:`+`}),
  (0,L.jsx)(`button`,{type:`button`,className:`pp-pick-give`,disabled:none,onClick:()=>{if(none)return;_ppWorm.give(`p`,id,k);setN(1);setTimeout(()=>setBal(_ppWorm.bal()),900)},children:`Give ${k}`})]}),
  (0,L.jsx)(`div`,{className:`pp-pick-bal`,children:bal==null?`Counting your worms…`:none?`You don't have any worms to give`:`You have ${bal} worm${bal===1?``:`s`}`})]})}
'''
patch("function _PostReactions({id}){", give + "function _PostReactions({id}){", 'give row component')
# the Reactions view: give row on top (also when nobody has reacted yet)
patch(" if(!ppl)return(0,L.jsx)(`div`,{className:`cp-empty`,children:`Loading…`});\n if(!ppl.length)return(0,L.jsx)(`div`,{className:`cp-empty`,children:`No reactions yet`});",
      " if(!ppl)return(0,L.jsx)(`div`,{className:`cp-empty`,children:`Loading…`});\n if(!ppl.length)return(0,L.jsxs)(`div`,{className:`pr-wrap`,onClick:ev=>ev.stopPropagation(),children:[(0,L.jsx)(_WormGive,{id}),(0,L.jsx)(`div`,{className:`cp-empty`,children:`No flaps or worms yet`})]});", 'give row when empty')
patch("return(0,L.jsxs)(`div`,{className:`pr-wrap`,onClick:ev=>ev.stopPropagation(),children:[\n  (0,L.jsxs)(`div`,{className:`pr-tabs`,",
      "return(0,L.jsxs)(`div`,{className:`pr-wrap`,onClick:ev=>ev.stopPropagation(),children:[(0,L.jsx)(_WormGive,{id}),\n  (0,L.jsxs)(`div`,{className:`pr-tabs`,", 'give row on top')
# the pill next to the bird always shows (🪱 count), so the Reactions view is always reachable
patch(" if(!emo.size&&!nw)return sheet;\n", "", 'pill always shown')
patch("  nw?(0,L.jsxs)(`span`,{className:`pr-w`,children:[(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),nw]}):null]}),sheet]})}",
      "  (0,L.jsxs)(`span`,{className:`pr-w`,children:[(0,L.jsx)(`span`,{className:`pp-ic pr-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),nw]})]}),sheet]})}", 'pill shows 0 too')

css = ("body .wg-row{display:flex;flex-direction:column;gap:6px;margin:0 0 12px;padding:10px 12px 8px;border-radius:14px;border:1px solid rgba(251,113,133,.28);background:rgba(251,113,133,.06)}"
       "body .wg-top{display:flex;align-items:center;gap:8px}body .wg-l{flex:1;font-size:13px;font-weight:700;color:#fecdd3;white-space:nowrap}"
       "body .wg-row .ri.wemo{font-size:16px}body .wg-out{flex-direction:row;align-items:center;justify-content:center;gap:8px;color:#fecdd3;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
