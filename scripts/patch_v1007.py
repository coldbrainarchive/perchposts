#!/usr/bin/env python3
"""Patch v1006 -> v1007: cleaner New Post page for huddles.
- No HUDDLES tag / "now" / divider / your own name pill: just the title, who to invite and the opening message,
  on a card styled like the huddle cards.
- "Invite birds · they'll get an invite to accept"; "Opening message · optional, gets pinned".
- The opening message box starts short (3 lines) and grows as you type.
- "📎 Photo / video" and a "Start huddle" button."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1006.js'
dst = '_deploy/assets/index-DUcNPOLc-v1007.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('{className:`content-card feed-post-card`,style:{marginBottom:16},children:[(0,L.jsx)(`div`,{className:`feed-post-header`,children:_isHuddle?',
      '{className:_isHuddle?`content-card feed-post-card hp-card nh-card`:`content-card feed-post-card`,style:{marginBottom:16},children:[!_isHuddle&&(0,L.jsx)(`div`,{className:`feed-post-header`,children:_isHuddle?',
      'no header row for huddles')
patch('(0,L.jsx)(`div`,{className:`feed-post-author-row`,children:(()=>{let n=Gn()',
      '!_isHuddle&&(0,L.jsx)(`div`,{className:`feed-post-author-row`,children:(()=>{let n=Gn()', 'no own name pill')
patch('style:{fontSize:12,color:`#94a3b8`,marginBottom:6},children:`Add the birds you want in this huddle:`',
      'className:`nh-lb`,children:[`Invite birds`,(0,L.jsx)(`span`,{className:`nh-hint`,children:` · they’ll get an invite to accept`})]',
      'invite label')
patch('children:`Opening message (optional, it gets pinned):`',
      'className:`nh-lb`,children:[`Opening message`,(0,L.jsx)(`span`,{className:`nh-hint`,children:` · optional, gets pinned`})]',
      'message label')
patch('disabled:l,rows:5,style:{width:`100%`',
      'disabled:l,rows:_isHuddle?3:5,onInput:_isHuddle?_ev=>{const _t=_ev.currentTarget;_t.style.height=`auto`;_t.style.height=Math.min(_t.scrollHeight,360)+`px`}:void 0,className:_isHuddle?`nh-msg`:void 0,style:{width:`100%`',
      'short growing message box')
patch('` Attach`]})', '_isHuddle?` Photo / video`:` Attach`]})', 'photo/video label')
patch('children:l?`Sending…`:`Post`', 'children:l?`Sending…`:_isHuddle?`Start huddle`:`Post`', 'Start huddle')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.nh-card .feed-post-main{padding-top:0!important;border-top:0!important;margin-top:0!important}
.nh-card input[placeholder^="Give this huddle"]{margin-top:0!important;font-size:22px!important}
.nh-lb{font-size:13px!important;font-weight:700;color:#e2e8f0!important;margin:18px 0 8px!important}
.nh-hint{font-weight:500;color:#64748b}
.nh-card .nh-msg{min-height:0!important;padding:12px 14px!important;border:1px solid #2e303a!important;border-radius:14px!important;background:#15171d!important;font-size:15px!important;line-height:1.45}
.nh-card .nh-msg:focus{border-color:#c084fc!important}
.nh-card .feed-post-actions{border-top:0!important;padding-top:4px!important}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
