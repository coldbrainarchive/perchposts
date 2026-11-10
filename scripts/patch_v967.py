#!/usr/bin/env python3
"""Patch v966 -> v967: jumping into a chat (notification, reply link, Find) never skips unread chirps.
Your read position only moves forward through chirps you've actually had on screen, in order. Jumping to a
reply halfway down marks the reply as seen but not the unread chirps above it, so next time the chat opens
at the first one you really haven't seen. Your own chirps count as seen. If older chirps aren't loaded yet
and might be unread, the position waits. The "↓ N new" pill counts unseen chirps below what's on screen."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v966.js'
dst = '_deploy/assets/index-DUcNPOLc-v967.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch(''' const b=w.getBoundingClientRect();let mx=null;
 w.querySelectorAll(`.chat-msg[data-t]`).forEach(m=>{const r=m.getBoundingClientRect();if(r.bottom>b.top+4&&r.top<b.bottom-12){const t=m.dataset.t;if(!mx||t>mx)mx=t}});
 mx&&_rdSet(p,mx)}''',
''' const b=w.getBoundingClientRect(),seen=s.seen||(s.seen=new Set()),els=[...w.querySelectorAll(`.chat-msg[data-t][data-comment-id]`)];
 els.forEach(m=>{const r=m.getBoundingClientRect();if((r.bottom>b.top+4&&r.top<b.bottom-12)||m.classList.contains(`chat-msg--mine`))seen.add(m.dataset.commentId)});
 if(!els.length)return;const ord=els.map(m=>[m.dataset.t,m.dataset.commentId]).sort((x,y)=>x[0]<y[0]?-1:x[0]>y[0]?1:0);
 const cur=_rdGet(p);if(s.more&&(!cur||ord[0][0]>cur))return;
 let mx=null;for(const[t,id]of ord){if(cur&&t<=cur)continue;if(!seen.has(id))break;mx=t}
 mx&&_rdSet(p,mx)}''', 'contiguous read position')
patch('const n=s.state===`ready`&&seen?[...w.querySelectorAll(`.chat-msg[data-t]`)].filter(m=>m.dataset.t>seen).length:0;',
      'const _bb=w.getBoundingClientRect(),n=s.state===`ready`?[...w.querySelectorAll(`.chat-msg[data-t][data-comment-id]`)].filter(m=>m.dataset.t>(seen||``)&&!(s.seen&&s.seen.has(m.dataset.commentId))&&m.getBoundingClientRect().top>_bb.bottom-12).length:0;',
      'pill counts unseen below')
patch('function _rdAfter(p,w,more,older){const s=_rd[p];if(!s||!w)return;s.win=w;',
      'function _rdAfter(p,w,more,older){const s=_rd[p];if(!s||!w)return;s.win=w;s.more=more;', 'remember has-more')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
