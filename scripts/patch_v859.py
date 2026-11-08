#!/usr/bin/env python3
"""Patch v858 -> v859: stop filling local storage, which broke the feed on iPhone Safari.
Sr saved the board of every post it ever saw, forever. Once storage was full setItem threw, which killed the
feed update, so new posts never appeared. Posts carry their own board, so only a post with no board of its own
is saved now, a full store can't break anything, and the old oversized list is cleared on load.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v858.js'
dst = '_deploy/assets/index-DUcNPOLc-v859.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n != 1:
        errors.append('FAIL (' + label + '): found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

def t(s):
    return s.replace('`', q)

patch(t('if(i)return e.id&&t[e.id]!==i&&(r[e.id]=i,a=!0),e;'), t('if(i)return e;'), 'stop saving every post')
patch(t('function mr(e,t){typeof window>`u`||window.localStorage.setItem(e,JSON.stringify(t))}'),
      t('function mr(e,t){try{typeof window>`u`||window.localStorage.setItem(e,JSON.stringify(t))}catch{}}'), 'a full store is harmless')
patch(t('var ur=`board_tags_by_post_id`,dr=`pending_board_tags`'),
      t('try{let _bt=localStorage.getItem(`board_tags_by_post_id`);if(_bt&&_bt.length>2e4)localStorage.removeItem(`board_tags_by_post_id`)}catch{}var ur=`board_tags_by_post_id`,dr=`pending_board_tags`'), 'clear the old list')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
