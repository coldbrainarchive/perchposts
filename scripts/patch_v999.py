#!/usr/bin/env python3
"""Patch v998 -> v999: chat header works like a group chat.
- The ‹ arrow is replaced by an ⓘ icon, and the whole left part of the top bar (icon + title) opens the post page:
  for a huddle its members / Invite / Leave / highlights, for a normal post the post itself.
- Going back is the browser's back button or swiping out.
- Long titles shrink with "…" so ⓘ and Oldest/Newest always fit."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v998.js'
dst = '_deploy/assets/index-DUcNPOLc-v999.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8},children:[_cf&&(0,L.jsx)(`button`,{type:`button`,className:`chat-back`,"aria-label":`Back to post`,onClick:_closeC,children:`‹`}),_cf?(0,L.jsxs)(`span`,{className:`comments-panel-title`,onClick:_closeC,children:[_ct]}):',
      '(0,L.jsxs)(`div`,{className:_cf?`cf-bar`:void 0,role:_cf?`button`:void 0,tabIndex:_cf?0:void 0,"aria-label":_cf?(c.is_huddle?`Huddle info`:`Post info`):void 0,onClick:_cf?_closeC:void 0,style:{display:`flex`,alignItems:`center`,gap:8},children:['
      '_cf&&(0,L.jsx)(`span`,{className:`cf-info`,"aria-hidden":`true`,children:(0,L.jsxs)(`svg`,{width:24,height:24,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2,strokeLinecap:`round`,children:[(0,L.jsx)(`circle`,{cx:12,cy:12,r:9.5}),(0,L.jsx)(`line`,{x1:12,y1:11,x2:12,y2:16.5}),(0,L.jsx)(`circle`,{cx:12,cy:7.6,r:.6,fill:`currentColor`})]})}),'
      '_cf?(0,L.jsx)(`span`,{className:`comments-panel-title cf-title`,children:_ct}):',
      'info icon + whole bar opens info')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.comments-shell.chat-full .chat-panel-header>div:first-child{flex:1;min-width:0}
.cf-title{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;cursor:pointer}
.cf-bar{cursor:pointer;-webkit-tap-highlight-color:transparent;border-radius:12px;align-self:stretch;margin:-6px 0;padding:6px 0}
.cf-bar:active{background:rgba(192,132,252,.08)}
.cf-info{flex-shrink:0;display:inline-flex;align-items:center;justify-content:center;color:#c084fc}
.comments-shell.chat-full .chat-panel-header>div:last-child{flex-shrink:0}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
