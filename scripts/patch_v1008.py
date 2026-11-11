#!/usr/bin/env python3
"""Patch v1007 -> v1008: cleaner New Post page for posts (matches the huddle side).
- Same card style; no "now", no divider, no own name pill.
- The tag / country pills stay at the top (the picker works as before).
- The body is a bordered box that starts at 4 lines and grows as you type.
- 🔗 Link, 📎 Media, Post."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1007.js'
dst = '_deploy/assets/index-DUcNPOLc-v1008.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('className:_isHuddle?`content-card feed-post-card hp-card nh-card`:`content-card feed-post-card`',
      'className:_isHuddle?`content-card feed-post-card hp-card nh-card`:`content-card feed-post-card hp-card nh-card np-card`', 'post card style')
patch('(0,L.jsx)(`span`,{className:`feed-post-time`,children:`now`})', 'null', 'no "now"')
patch('!_isHuddle&&(0,L.jsx)(`div`,{className:`feed-post-author-row`', '!1&&(0,L.jsx)(`div`,{className:`feed-post-author-row`', 'no own name pill')
patch('_isHuddle?` Media`:` Attach`', '` Media`', 'Media')
patch('rows:_isHuddle?3:5,onInput:_isHuddle?', 'rows:_isHuddle?3:4,onInput:!0?', 'body grows')
patch('className:_isHuddle?`nh-msg`:void 0', 'className:`nh-msg`', 'body box style')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.np-card .feed-post-header{border-bottom:0!important;padding-bottom:0!important;margin-bottom:14px!important}
.np-card .feed-post-board-row{align-items:center;gap:8px}
.np-card .feed-post-header{position:relative}
.np-card .feed-post-board-group>div[style*="position: relative"]{position:static!important}
.np-card .feed-post-board-group>div>div[style*="position: absolute"]{left:0!important;max-width:100%}
.np-in{font-size:13px;font-weight:700;color:#94a3b8;white-space:nowrap}
.np-card input[placeholder^="Give the thread"]{margin-top:0!important;font-size:22px!important;margin-bottom:12px!important}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
