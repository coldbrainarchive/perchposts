#!/usr/bin/env python3
"""Patch v842 -> v843: the 📌 🔒 📦 badges on posts match the amber mod buttons, icon only, on the feed and
the post page. Light amber rather than solid, because the yellow lock vanishes on solid amber.
The badges sit in the card corner, so the pill row now leaves room and wraps instead of running under them.
"""
import re, sys

src = '_deploy/assets/index-DUcNPOLc-v842.js'
dst = '_deploy/assets/index-DUcNPOLc-v843.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()

CHIP = '{display:`inline-flex`,alignItems:`center`,justifyContent:`center`,height:20,width:20,borderRadius:999,border:`1px solid #323b48`,background:`#20262f`,fontSize:11,flexShrink:0,lineHeight:1,overflow:`hidden`,boxSizing:`border-box`}'.replace('`', q)
done = 0
for icon, n in (('📌', 2), ('🔒', 2)):
    old = 'style:' + CHIP + ',children:' + q + icon + q
    if content.count(old) != n:
        print('FAIL ' + icon + ': found ' + str(content.count(old))); sys.exit(1)
    content = content.replace(old, 'className:' + q + 'post-badge' + q + ',children:' + q + icon + q); done += n
old = 'title:' + q + 'Archived' + q + ',style:' + CHIP + ',children:' + q + '📦' + q
if content.count(old) != 2:
    print('FAIL archive: found ' + str(content.count(old))); sys.exit(1)
content = content.replace(old, 'title:' + q + 'Archived' + q + ',className:' + q + 'post-badge' + q + ',children:' + q + '📦' + q); done += 2

old = '(0,L.jsxs)(`div`,{style:{position:`absolute`,top:14,right:16,display:`flex`,gap:4,alignItems:`center`}'.replace('`', q)
if content.count(old) != 2:
    print('FAIL badge row: found ' + str(content.count(old))); sys.exit(1)
content = content.replace(old, old.replace('{style:', '{className:' + q + 'post-badges' + q + ',style:'))

old = '.chat-section-title{display:flex;'
if content.count(old) != 1:
    print('FAIL styles'); sys.exit(1)
content = content.replace(old, '.feed-post-card:has(.post-badges>:nth-child(1)) .feed-post-board-row{padding-right:28px}.feed-post-card:has(.post-badges>:nth-child(2)) .feed-post-board-row{padding-right:54px}.feed-post-card:has(.post-badges>:nth-child(3)) .feed-post-board-row{padding-right:80px}.feed-post-card:has(.post-badges>:nth-child(4)) .feed-post-board-row{padding-right:106px}.post-badge{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;border:1px solid rgba(251,191,36,.4);background:rgba(251,191,36,.08);font-size:11px;line-height:22px;text-align:center;flex-shrink:0;box-sizing:border-box;padding:0}' + old)

open(dst, 'w', encoding='utf-8').write(content)
print('OK: ' + str(done) + ' badges. Wrote ' + dst)
