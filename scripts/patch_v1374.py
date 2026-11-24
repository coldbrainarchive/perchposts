#!/usr/bin/env python3
"""Patch v1373 -> v1374: the flash when opening chirps from the scroller after swiping down (measured on the user's
iPhone, frame by frame): the feed under the scroller is scrolled to the current post (726px in the test); the chat
locks the page at that scroll (body fixed, top -726) and for one frame the scroller was pushed off screen, showing
the bare page, before the scroll reset to 0. The hidden feed is now scrolled to the top before the chat opens."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1373.js'
dst = '_deploy/assets/index-DUcNPOLc-v1374.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)
patch("st.reelResume=id;history.replaceState(st,``)}catch(e){}",
      "st.reelResume=id;history.replaceState(st,``)}catch(e){}try{window.scrollTo(0,0)}catch(e){}", 'scroll hidden feed to top')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
