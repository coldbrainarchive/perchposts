#!/usr/bin/env python3
"""Patch v955 -> v956: the 💬 chirps pill on a post card opens the post straight into its chat
(?chat=1&via=card). On phones, back from that chat returns to the feed (no extra post-page step)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v955.js'
dst = '_deploy/assets/index-DUcNPOLc-v956.js'
c = open(src, encoding='utf-8').read()
old = '(0,L.jsxs)(I,{to:`/post/${e.id}`,className:`feed-post-action-pill`,children:[(0,L.jsx)(`span`,{children:`💬`})'
if c.count(old) != 1: print('FAIL', c.count(old)); sys.exit(1)
c = c.replace(old, '(0,L.jsxs)(I,{to:`/post/${e.id}?chat=1&via=card`,className:`feed-post-action-pill`,children:[(0,L.jsx)(`span`,{children:`💬`})')
old2 = 'history.replaceState(history.state,``,location.pathname);history.pushState(history.state,``,location.pathname+`?chat=1`);_cyR.current=0;'
if c.count(old2) != 1: print('FAIL2', c.count(old2)); sys.exit(1)
c = c.replace(old2, 'if(new URLSearchParams(location.search).get(`via`)===`card`)history.replaceState(history.state,``,location.pathname+`?chat=1`);else{history.replaceState(history.state,``,location.pathname);history.pushState(history.state,``,location.pathname+`?chat=1`)}_cyR.current=0;')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
