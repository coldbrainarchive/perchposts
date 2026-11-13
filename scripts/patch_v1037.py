#!/usr/bin/env python3
"""Patch v1036 -> v1037: the full-screen link view shows each post's time ("46m ago") at the top right, above the
picture, on the same row as the tags (tags left, time right). The time is read from the post card's own time pill."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1036.js'
dst = '_deploy/assets/index-DUcNPOLc-v1037.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('seen.add(d.post);d.tags=_reelTags(el);out.push(d)',
      'seen.add(d.post);d.tags=_reelTags(el);d.time=_reelTime(el);out.push(d)', 'collect time')
patch('function _reelCollect(){',
      'function _reelTime(el){try{const card=el.closest(`.feed-post-card`);if(!card)return ``;for(const x of card.querySelectorAll(`.feed-post-actions .feed-post-action-pill, .feed-post-actions span`)){if(x.closest(`[data-lp]`)||x.children.length)continue;const t=(x.textContent||``).trim();if(/^(just now|\\d+\\s*(s|m|h|d|w|mo|y)( ago)?|.+ ago)$/i.test(t))return t}}catch(e){}return ``}\nfunction _reelCollect(){',
      'time reader')
patch('if((d.tags||[]).length){const tr=tagRow();tr.classList.add(`flat`);inner.appendChild(tr)}',
      'if((d.tags||[]).length||d.time){const hd=document.createElement(`div`);hd.className=`reel-head`;if((d.tags||[]).length){const tr=tagRow();tr.classList.add(`flat`);hd.appendChild(tr)}if(d.time){const tm=document.createElement(`span`);tm.className=`reel-time`;tm.textContent=d.time;hd.appendChild(tm)}inner.appendChild(hd)}',
      'head row')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel-head{display:flex;align-items:flex-start;gap:10px;margin-bottom:10px}
.reel-head .reel-tags.flat{margin-bottom:0;flex:1;min-width:0}
.reel-time{margin-left:auto;color:#94a3b8;font-size:12px;font-weight:700;line-height:22px;white-space:nowrap;flex-shrink:0}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
