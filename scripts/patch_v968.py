#!/usr/bin/env python3
"""Patch v967 -> v968: tapping Newest means "I'm caught up": it still scrolls to the newest chirp, and now
also marks everything up to it as read, so next time the chat opens at the newest with no NEW line.
(Notification / reply / Find jumps still don't count skipped chirps as read.)"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v967.js'
dst = '_deploy/assets/index-DUcNPOLc-v968.js'
c = open(src, encoding='utf-8').read()
old = 'className:b?`sort-toggle-btn active`:`sort-toggle-btn`,onClick:()=>{let e=D.current;if(e&&e.firstElementChild){e.firstElementChild.scrollIntoView();x(!0);}}'
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, 'className:b?`sort-toggle-btn active`:`sort-toggle-btn`,onClick:()=>{let e=D.current;_rdCaught(r,e);if(e&&e.firstElementChild){e.firstElementChild.scrollIntoView();x(!0);}}')
c += r'''
function _rdCaught(p,w){if(!w)return;let mx=null;const s=_rd[p];
 w.querySelectorAll(`.chat-msg[data-t][data-comment-id]`).forEach(m=>{const t=m.dataset.t;if(!mx||t>mx)mx=t;s&&(s.seen||(s.seen=new Set())).add(m.dataset.commentId)});
 mx&&_rdSet(p,mx);s&&s.pill&&(s.pill.remove(),s.pill=null)}
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
