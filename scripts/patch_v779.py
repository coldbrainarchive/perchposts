#!/usr/bin/env python3
"""Patch v778 -> v779:
Cut D1 row reads from polling (site hit the D1 free-tier daily read limit).
1. Home feed: poll every 30s instead of 4s; skip while the tab is hidden or a
   time/calendar filter is active (past days don't change); refresh on return.
2. Second feed view: poll every 30s instead of 4s; skip while hidden; refresh on return.
3. Post page: keep 2s polling (chat feel) but skip while hidden; refresh on return.
4. Notification count: keep 10s but skip while hidden.
5. Calendar day / hours-ago fetch: limit 500 -> 5000 so busy days aren't truncated.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v778.js'
dst = '_deploy/assets/index-DUcNPOLc-v779.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label, count=1):
    global content
    n = content.count(old)
    if n != count:
        errors.append('FAIL (' + label + '): expected ' + str(count) + ' matches, found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

TF = 'new URLSearchParams(location.search).get(' + q + 'time' + q + ')'
VIS = q + 'visibilitychange' + q

# 1. Home feed
patch('let e=window.setTimeout(()=>{v()},0),t=window.setInterval(()=>{v()},4e3);return()=>{window.clearTimeout(e),window.clearInterval(t)}},[v])',
      'let e=window.setTimeout(()=>{v()},0),_pv=()=>{document.hidden||' + TF + '||v()},t=window.setInterval(_pv,3e4);'
      'document.addEventListener(' + VIS + ',_pv);'
      'return()=>{window.clearTimeout(e),window.clearInterval(t),document.removeEventListener(' + VIS + ',_pv)}},[v])',
      'home feed poll 30s + hidden/time-filter guard')

# 2. Second feed view
patch('let e=window.setTimeout(()=>{y()},0),t=window.setInterval(()=>{y()},4e3);return()=>{window.clearTimeout(e),window.clearInterval(t)}},[y,e])',
      'let e=window.setTimeout(()=>{y()},0),_pv=()=>{document.hidden||y()},t=window.setInterval(_pv,3e4);'
      'document.addEventListener(' + VIS + ',_pv);'
      'return()=>{window.clearTimeout(e),window.clearInterval(t),document.removeEventListener(' + VIS + ',_pv)}},[y,e])',
      'second feed poll 30s + hidden guard')

# 3. Post page
patch('let e=window.setTimeout(()=>{P()},0),t=window.setInterval(()=>{P()},2e3);return()=>{window.clearTimeout(e),window.clearInterval(t)}},[P])',
      'let e=window.setTimeout(()=>{P()},0),_pv=()=>{document.hidden||P()},t=window.setInterval(_pv,2e3);'
      'document.addEventListener(' + VIS + ',_pv);'
      'return()=>{window.clearTimeout(e),window.clearInterval(t),document.removeEventListener(' + VIS + ',_pv)}},[P])',
      'post page poll hidden guard')

# 4. Notification count
patch('e();let t=setInterval(e,1e4);return()=>clearInterval(t)},[])',
      'e();let t=setInterval(()=>{document.hidden||e()},1e4);return()=>clearInterval(t)},[])',
      'notif-count hidden guard')

# 5. Calendar fetch limit
patch('get-posts?limit=500${since?', 'get-posts?limit=5000${since?', 'calendar fetch limit 5000')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print('Paren delta: ' + str(p_delta) + ', Brace delta: ' + str(b_delta))
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
