#!/usr/bin/env python3
"""Patch v1232 -> v1233: the home feed checks for the hourly batch right at the top of the hour (2, 5, 10 and 20 s
past :00) instead of waiting for its next 30 s check, so the "N NEW POSTS" pill shows ~2 s after the title's timer
hits zero rather than up to 30 s later. The normal 30 s checks are unchanged."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1232.js'
dst = '_deploy/assets/index-DUcNPOLc-v1233.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("t=window.setInterval(_pv,3e4);document.addEventListener(`visibilitychange`,_pv);return()=>{window.clearTimeout(e),window.clearInterval(t),document.removeEventListener(`visibilitychange`,_pv)}},[v])",
      "t=window.setInterval(_pv,3e4);window._ppFeedPoll=_pv;document.addEventListener(`visibilitychange`,_pv);return()=>{window._ppFeedPoll===_pv&&(window._ppFeedPoll=null);window.clearTimeout(e),window.clearInterval(t),document.removeEventListener(`visibilitychange`,_pv)}},[v])",
      'let the top of the hour trigger a check')
c += r"""
;(()=>{try{let last=-1;setInterval(()=>{const n=new Date(),s=n.getSeconds();
  if(n.getMinutes()===0&&[2,5,10,20].includes(s)&&s!==last){last=s;try{window._ppFeedPoll&&window._ppFeedPoll()}catch(e){}}
  if(n.getMinutes()!==0)last=-1},500)}catch(e){}})();
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
