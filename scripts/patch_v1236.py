#!/usr/bin/env python3
"""Patch v1235 -> v1236: the "N NEW POSTS" pill fires as soon as the hourly batch lands. From :59:55 to 1½ min
past the hour the page makes a tiny check (newest 10 posts, ~1 KB) every 1.5 s; the moment a post stamped in
the first minute of the hour shows up, it runs the normal feed check (which shows the pill) and stops.
Replaces the fixed checks at 2/5/10/20 s past :00. Works even if the phone's clock is a little off."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1235.js'
dst = '_deploy/assets/index-DUcNPOLc-v1236.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch(""";(()=>{try{let last=-1;setInterval(()=>{const n=new Date(),s=n.getSeconds();
  if(n.getMinutes()===0&&[2,5,10,20].includes(s)&&s!==last){last=s;try{window._ppFeedPoll&&window._ppFeedPoll()}catch(e){}}
  if(n.getMinutes()!==0)last=-1},500)}catch(e){}})();""",
""";(()=>{try{let busy=!1,done=-1;
  const win=n=>(n.getUTCMinutes()===59&&n.getSeconds()>=55)||(n.getUTCMinutes()===0)||(n.getUTCMinutes()===1&&n.getSeconds()<30);
  setInterval(async()=>{const n=new Date();if(!win(n)||busy||document.hidden||!window._ppFeedPoll)return;
    const hr=new Date(n.getTime()+6e4);hr.setUTCMinutes(0,0,0);const key=hr.getTime();if(done===key)return;
    busy=!0;try{const r=await fetch(`https://daboysforumip.coldbrainarchive.workers.dev/get-posts?limit=10`);if(r.ok){const j=await r.json();
      const fresh=(j.posts||[]).some(p=>{const t=Date.parse(p.created_at);return t>Date.now()-15e4&&new Date(t).getUTCMinutes()===0});
      if(fresh){done=key;window._ppFeedPoll()}}}catch(e){}busy=!1},1500)}catch(e){}})();""", 'check every 1.5 s around :00 until the batch lands')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
