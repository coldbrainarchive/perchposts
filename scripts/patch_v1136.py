#!/usr/bin/env python3
"""Patch v1135 -> v1136: post Reactions: the "Give worms ⌄" button sits at the end of the tab row (All · Flaps · 🪱),
on every tab. It opens a slim give row (You have N · − N + · Give N) with no worm emoji or "Give worms" label of its
own. The give button inside the 🪱 tab is gone. Bot posts still get no worm tab or button."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1135.js'
dst = '_deploy/assets/index-DUcNPOLc-v1136.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# slim give row
patch("function _WormGive({id,kind=`p`}){", "function _WormGive({id,kind=`p`,bare}){", 'give row: bare option')
patch("(0,L.jsx)(`span`,{className:`pp-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}}),(0,L.jsx)(`span`,{className:`wg-l`,children:`Give worms`}),\n  (0,L.jsx)(`button`,{type:`button`,className:`pp-pick-st`,disabled:k<=1||none,",
      "...(bare?[(0,L.jsx)(`span`,{className:`wg-l wg-bal`,children:bal==null?`Counting your worms…`:none?`No worms to give`:`You have ${bal} worm${bal===1?``:`s`}`},`b`)]:[(0,L.jsx)(`span`,{className:`pp-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`WORM`)}},`i`),(0,L.jsx)(`span`,{className:`wg-l`,children:`Give worms`},`l`)]),\n  (0,L.jsx)(`button`,{type:`button`,className:`pp-pick-st`,disabled:k<=1||none,",
      'give row: no emoji/label when bare')
patch("  (0,L.jsx)(`div`,{className:`pp-pick-bal`,children:bal==null?`Counting your worms…`:none?`You don't have any worms to give`:`You have ${bal} worm${bal===1?``:`s`}`})]})}",
      "  bare?null:(0,L.jsx)(`div`,{className:`pp-pick-bal`,children:bal==null?`Counting your worms…`:none?`You don't have any worms to give`:`You have ${bal} worm${bal===1?``:`s`}`})]})}",
      'give row: balance moves up when bare')
# button in the tab row, panel under the tabs
patch("function _PostReactions({id,bot}){const ppl=_usePrx(id),", "function _PostReactions({id,bot}){const[gop,setGop]=(0,_.useState)(!1),ppl=_usePrx(id),", 'reactions: give state')
patch("T(`all`,`All ${list.length}`),T(`flap`,[ic(`BIRD`),nf]),bot?null:T(`worm`,[ic(`WORM`),nw])]}),",
      "T(`all`,`All ${list.length}`),T(`flap`,[ic(`BIRD`),nf]),bot?null:T(`worm`,[ic(`WORM`),nw]),bot?null:(0,L.jsxs)(`button`,{type:`button`,className:`wg-open`+(gop?` on`:``),\"aria-expanded\":gop,onClick:ev=>{ev.stopPropagation();setGop(!gop)},children:[`Give worms`,(0,L.jsx)(`span`,{className:`wg-chev`,children:`⌄`})]},`give`)]}),\n  gop&&!bot?(0,L.jsx)(_WormGive,{id,kind:`p`,bare:1}):null,",
      'Give worms beside the tabs')
patch("tab===`worm`&&!bot?(0,L.jsx)(_WormGivers,{kind:`p`,id,give:1})", "tab===`worm`&&!bot?(0,L.jsx)(_WormGivers,{kind:`p`,id})", 'no give button inside the 🪱 tab')
patch("body .lb-ic{", "body .pr-tabs .wg-open{margin:0 0 0 auto;align-self:stretch;height:auto;padding-top:0;padding-bottom:0}body .wg-row .wg-bal{font-size:12.5px;font-weight:600;color:#94a3b8}body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
