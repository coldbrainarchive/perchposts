#!/usr/bin/env python3
"""Patch v1174 -> v1176 (v1175's card layout is rolled back):
- Post cards are back to the v1174 layout (time pill bottom right, Share pill with its label, corner badges).
- In Flock, the time pill shows the last activity as a purple chirp bubble + "11h" (instead of "Active 11h ago").
- Kept from v1175: the post page's time pill says "Created 6mo ago"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1174.js'
dst = '_deploy/assets/index-DUcNPOLc-v1176.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

patch("(0,L.jsx)(`span`,{className:`feed-post-action-pill`,style:{marginLeft:`auto`,cursor:`default`},children:a?`Active ${Un(e.last_activity||e.created_at)}`:Un(e.created_at)})]})]})}",
      "(0,L.jsx)(`span`,{className:`feed-post-action-pill`+(a?` pc-act`:``),title:a?`Last activity`:void 0,style:{marginLeft:`auto`,cursor:`default`},children:a?[(0,L.jsx)(`span`,{className:`pp-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`CHAT`)}},`i`),(0,L.jsx)(`span`,{children:Un(e.last_activity||e.created_at).replace(/ ago$/,``)},`t`)]:Un(e.created_at)})]})]})}",
      'flock pill: purple bubble + time')
patch("children:c.is_huddle?(()=>{const _a=Un(c.created_at);return _a===`just now`?`New`:_a.replace(/ ago$/,` old`)})():Un(c.created_at)})",
      "children:c.is_huddle?(()=>{const _a=Un(c.created_at);return _a===`just now`?`New`:_a.replace(/ ago$/,` old`)})():`Created ${Un(c.created_at)}`})", 'post page says Created')
patch("body .lb-ic{",
      "body .feed-post-action-pill.pc-act{color:#c084fc!important;border-color:rgba(192,132,252,.4)!important;background:rgba(192,132,252,.08)!important;gap:5px}"
      "body .feed-post-action-pill.pc-act .pp-ic{color:#c084fc}body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
