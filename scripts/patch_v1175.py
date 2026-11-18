#!/usr/bin/env python3
"""Patch v1174 -> v1175: post card layout.
- The time moves up to the card's name row, as small plain text on the right (no pill): "11h".
  In Flock it shows the last chirp/flap time with a chirp-bubble icon, in purple.
- Pinned / locked / archived icons sit in that row too (before the time) instead of floating in the corner.
- Share becomes a round icon-only button at the right of the bottom row (shows "Copied"/"Shared" briefly).
- The post page's time pill says "Created 11d ago"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1174.js'
dst = '_deploy/assets/index-DUcNPOLc-v1175.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# header row: group + badges + time
patch("(0,L.jsx)(`div`,{className:`feed-post-board-row`,style:{marginBottom:10},children:(0,L.jsxs)(`span`,{className:`feed-post-board-group`,style:{flexWrap:`wrap`,gap:5},children:[!e.browser_id",
      "(0,L.jsxs)(`div`,{className:`feed-post-board-row pc-head`,style:{marginBottom:10},children:[(0,L.jsxs)(`span`,{className:`feed-post-board-group`,style:{flexWrap:`wrap`,gap:5},children:[!e.browser_id",
      'header row holds more')
BADGES = "(e.pinned||e.locked||e.frozen)&&(0,L.jsxs)(`div`,{className:`post-badges`,style:{position:`absolute`,top:14,right:16,display:`flex`,gap:4,alignItems:`center`},children:[e.pinned&&(0,L.jsx)(`span`,{className:`post-badge pp-badge-ic`,title:`Pinned`,dangerouslySetInnerHTML:{__html:_ppIco(`PIN`)}}),e.locked&&(0,L.jsx)(`span`,{className:`post-badge pp-badge-ic`,title:`Locked`,dangerouslySetInnerHTML:{__html:_ppIco(`LOCK`)}}),e.frozen&&(0,L.jsx)(`span`,{title:`Archived`,className:`post-badge pp-badge-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`ARCHIVE`)}})]}),"
inline = BADGES.replace("className:`post-badges`,style:{position:`absolute`,top:14,right:16,display:`flex`,gap:4,alignItems:`center`}", "className:`post-badges pc-badges`")
TIME = ("(0,L.jsxs)(`span`,{className:`pc-time`+(a?` pc-act`:``),title:a?`Last activity`:`Posted`,children:[a?(0,L.jsx)(`span`,{className:`pp-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`CHAT`)}}):null,"
        "(()=>{const _a=Un(a?e.last_activity||e.created_at:e.created_at);return _a.replace(/ ago$/,``)})()]})")
patch("small:!0})}),]})}),(e.pinned||e.locked||e.frozen)&&(0,L.jsxs)(`div`,{className:`post-badges`,style:{position:`absolute`,top:14,right:16,",
      "small:!0})}),]}),"+inline[:-1]+","+TIME+"]}),!1&&(0,L.jsxs)(`div`,{className:`post-badges`,style:{position:`absolute`,top:14,right:16,",
      'badges + time in the header')
# bottom row: share icon-only on the right, no time pill
patch("(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:h,children:[(0,L.jsx)(`span`,{className:`pp-ic pp-share`,dangerouslySetInnerHTML:{__html:_ppIco(`SHARE`)}}),(0,L.jsx)(`span`,{children:o})]}),(0,L.jsx)(`span`,{className:`feed-post-action-pill`,style:{marginLeft:`auto`,cursor:`default`},children:a?`Active ${Un(e.last_activity||e.created_at)}`:Un(e.created_at)})]})]})}",
      "(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill pc-share`+(o!==`Share`?` pc-said`:``),\"aria-label\":`Share`,onClick:h,children:[(0,L.jsx)(`span`,{className:`pp-ic pp-share`,dangerouslySetInnerHTML:{__html:_ppIco(`SHARE`)}}),o!==`Share`?(0,L.jsx)(`span`,{children:o}):null]})]})]})}",
      'share icon, no time pill')
# post page: Created
patch("children:c.is_huddle?(()=>{const _a=Un(c.created_at);return _a===`just now`?`New`:_a.replace(/ ago$/,` old`)})():Un(c.created_at)})",
      "children:c.is_huddle?(()=>{const _a=Un(c.created_at);return _a===`just now`?`New`:_a.replace(/ ago$/,` old`)})():`Created ${Un(c.created_at)}`})", 'post page says Created')

css = ("body .feed-post-board-row.pc-head{display:flex;align-items:flex-start;gap:8px;padding-right:0!important}"
       "body .pc-head .feed-post-board-group{flex:1;min-width:0}"
       "body .pc-badges{display:flex;gap:4px;align-items:center;flex-shrink:0;min-height:var(--pc-h,22px)}"
       "body .pc-time{flex-shrink:0;min-height:var(--pc-h,22px);display:inline-flex;align-items:center;gap:4px;font-size:12.5px;font-weight:600;color:#64748b;white-space:nowrap}"
       "body .pc-time.pc-act{color:#c084fc}body .pc-time .pp-ic svg{width:13px!important;height:13px!important}"
       "body .feed-post-actions .pc-share{margin-left:auto;width:34px;padding:0!important;justify-content:center}"
       "body .feed-post-actions .pc-share.pc-said{width:auto;padding:0 12px!important}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
