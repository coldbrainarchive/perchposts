#!/usr/bin/env python3
"""Patch v957 -> v958: the Oldest/Newest toggle follows the scroll. At the very top of the chat (everything
loaded) it flips to Oldest; back at the newest chirp it flips to Newest; in between it stays as it was.
So opening a chat at the top (first visit) shows Oldest highlighted."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v957.js'
dst = '_deploy/assets/index-DUcNPOLc-v958.js'
c = open(src, encoding='utf-8').read()
old = 'onScroll:()=>{let e=D.current;if(!e)return;O.current=Math.abs(e.scrollTop)<60;'
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, old + 'if(!_pv){let _up=Math.abs(e.scrollTop);if(!_hmR.current&&e.scrollHeight-e.clientHeight-_up<6&&e.scrollHeight>e.clientHeight+6)x(!1);else if(_up<6)x(!0)}')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
