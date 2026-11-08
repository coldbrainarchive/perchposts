#!/usr/bin/env python3
"""Patch v787 -> v788:
A region pill shows its feeds plus articles naming any of its countries (worker /get-posts).
1. The feed keeps what the server returned for a region instead of re-filtering to post.continent.
   A typed word next to a region pill still means "this word, within this region's feeds".
2. Filtered views clear previous results on change and ignore late responses, since the
   client filter can no longer hide another view's posts.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v787.js'
dst = '_deploy/assets/index-DUcNPOLc-v788.js'

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

def t(s):
    return s.replace('`', q)

patch('.filter(e=>!d||e.continent===d).filter(e=>!f||_cs||e.country===f)',
      '.filter(e=>!d||(!m&&TagR!==null)||e.continent===d).filter(e=>!f||_cs||e.country===f)',
      'keep server results for region pills')
patch(t('let turl=u===`activity`?`${R}/get-posts?activity=1&sort=activity&limit=50`:`${R}/get-posts?limit=50`;if(u&&u!==`activity`)turl+='),
      t('setTagR(null);_setTm(null);let _c=!1,turl=u===`activity`?`${R}/get-posts?activity=1&sort=activity&limit=50`:`${R}/get-posts?limit=50`;if(u&&u!==`activity`)turl+='),
      'clear previous filtered results')
patch('.then(d2=>{_setTm(d2.next_before??null);setTagR(Sr(d2.posts||[]))}).catch(()=>setTagR(null))},[u,d,f,p])',
      '.then(d2=>{if(_c)return;_setTm(d2.next_before??null);setTagR(Sr(d2.posts||[]))}).catch(()=>{_c||setTagR(null)});return()=>{_c=!0}},[u,d,f,p])',
      'ignore late filtered responses')

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
