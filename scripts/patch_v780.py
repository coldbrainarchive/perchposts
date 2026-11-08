#!/usr/bin/env python3
"""Patch v779 -> v780:
"N h ago" time filter means "skip back to news from N+ hours ago".
1. Home feed server fetch used since=now-N (last N hours); use until=now-N instead,
   matching the client-side fallback filter and the other feed view.
2. Limit: 5000 for a calendar day (since set), 500 for hours-ago (one-shot, older posts).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v779.js'
dst = '_deploy/assets/index-DUcNPOLc-v780.js'

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

patch('else if(qT.startsWith(' + q + 'ago_' + q + ')){const n=parseInt(qT.slice(4));since=new Date(Date.now()-n*3600000).toISOString()}',
      'else if(qT.startsWith(' + q + 'ago_' + q + ')){const n=parseInt(qT.slice(4));until=new Date(Date.now()-n*3600000).toISOString()}',
      'hours-ago fetch: until=now-N')

patch('get-posts?limit=5000${since?', 'get-posts?limit=${since?5000:500}${since?', 'limit 5000 day / 500 hours-ago')

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
