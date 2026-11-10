#!/usr/bin/env python3
"""Patch v998 -> v999: chat header works like a group chat.
- ‹ now really goes back to wherever you came from (Huddles space, feed, notifications, the post page). If the
  chat was opened straight from a link with nothing behind it, it falls back to the post page.
- New ⓘ button after the title opens the post page (for a huddle: its members / Invite / Leave / highlights;
  for a normal post: the post itself). Tapping the title does the same.
- Long titles shrink with "…" so ⓘ and Oldest/Newest always fit."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v998.js'
dst = '_deploy/assets/index-DUcNPOLc-v999.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('_cf&&(0,L.jsx)(`button`,{type:`button`,className:`chat-back`,"aria-label":`Back to post`,onClick:_closeC,children:`‹`}),_cf?(0,L.jsxs)(`span`,{className:`comments-panel-title`,onClick:_closeC,children:[_ct]}):',
      '_cf&&(0,L.jsx)(`button`,{type:`button`,className:`chat-back`,"aria-label":`Back`,onClick:()=>{history.length>1?history.back():_closeC()},children:`‹`}),'
      '_cf?(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`span`,{className:`comments-panel-title cf-title`,role:`button`,tabIndex:0,onClick:_closeC,children:_ct}),'
      '(0,L.jsx)(`button`,{type:`button`,className:`cf-info`,"aria-label":c.is_huddle?`Huddle info`:`Post info`,onClick:_closeC,children:(0,L.jsxs)(`svg`,{width:22,height:22,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2,strokeLinecap:`round`,children:[(0,L.jsx)(`circle`,{cx:12,cy:12,r:9.5}),(0,L.jsx)(`line`,{x1:12,y1:11,x2:12,y2:16.5}),(0,L.jsx)(`circle`,{cx:12,cy:7.6,r:.6,fill:`currentColor`})]})})]}):',
      'back + info')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.comments-shell.chat-full .chat-panel-header>div:first-child{flex:1;min-width:0}
.cf-title{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;cursor:pointer}
.cf-info{flex-shrink:0;display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;margin-left:-4px;padding:0;border:0;border-radius:999px;background:none;color:#c084fc;cursor:pointer;-webkit-tap-highlight-color:transparent}
.cf-info:active{background:rgba(192,132,252,.14)}
.comments-shell.chat-full .chat-panel-header>div:last-child{flex-shrink:0}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
