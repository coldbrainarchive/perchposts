#!/usr/bin/env python3
"""Patch v1236 -> v1237: the top-of-the-hour check fires once. One small check (newest 10 posts, ~1 KB) at :00:01 UTC;
only if the batch isn't in yet does it try again, further apart each time (3, 6, 10, 15, 22, 30, 45, 60, 90 s), then
stops for the hour. As soon as it sees the batch it loads the feed, which shows the "N NEW POSTS" pill.
It now also works when you've scrolled far enough down for older posts to load (the regular 30 s check skips that case)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1236.js'
dst = '_deploy/assets/index-DUcNPOLc-v1237.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("window._ppFeedPoll=_pv;", "window._ppFeedPoll=_pv;window._ppFeedLoad=()=>{new URLSearchParams(location.search).get(`time`)||v()};", 'feed load that also works when scrolled down')
patch("window._ppFeedPoll===_pv&&(window._ppFeedPoll=null);", "window._ppFeedPoll===_pv&&(window._ppFeedPoll=null,window._ppFeedLoad=null);", 'clean up')
i = c.index(";(()=>{try{let busy=!1,done=-1;")
j = c.index("},1500)}catch(e){}})();", i) + len("},1500)}catch(e){}})();")
c = c[:i] + r""";(()=>{try{const AT=[1,3,6,10,15,22,30,45,60,90];let hour=-1,step=0,busy=!1;
  setInterval(async()=>{const now=Date.now(),h=Math.floor(now/36e5),s=(now-h*36e5)/1e3;
    if(h!==hour){hour=h;step=0}
    if(busy||step>=AT.length||s<AT[step]||document.hidden||!window._ppFeedLoad)return;
    while(step<AT.length&&s>=AT[step])step++;
    busy=!0;try{const r=await fetch(`https://daboysforumip.coldbrainarchive.workers.dev/get-posts?limit=10`);if(r.ok){const j=await r.json();
      if((j.posts||[]).some(p=>{const t=Date.parse(p.created_at);return t>=h*36e5-6e4&&t<h*36e5+6e4})){step=AT.length;window._ppFeedLoad()}}}catch(e){}busy=!1},500)}catch(e){}})();""" + c[j:]
print('OK: one check at :00:01, retries spaced out')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
