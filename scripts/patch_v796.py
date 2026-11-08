#!/usr/bin/env python3
"""Patch v795 -> v796:
1. Chat header uses the site's top bar colour. Safari tints the status bar from the page (it ignored
   theme-color here: measured #0c0f12 against a #14161b header), so the header matches it instead.
2. Tapping the title in the chat screen goes back to the post.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v795.js'
dst = '_deploy/assets/index-DUcNPOLc-v796.js'

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

patch(t('className:`comments-panel-title`,children:_cf?[_ct]:'),
      t('className:`comments-panel-title`,onClick:_cf?_closeC:void 0,children:_cf?[_ct]:'),
      'title goes back to the post')
patch('.chat-full .chat-panel-header,.chat-full .chat-compose{background:#14161c}',
      '.chat-full .chat-compose{background:#14161c}'
      '.chat-full .chat-panel-header{background:#0b0f12;border-top:env(safe-area-inset-top) solid #0b0f12}'
      '.chat-full .comments-panel-title{cursor:pointer}',
      'header matches the status bar')
patch('z-index:45;padding-top:env(safe-area-inset-top);box-sizing:border-box;',
      'z-index:45;box-sizing:border-box;',
      'safe area moves onto the header')
patch(t('_tc&&(_tc.content=`#14161c`);'),
      t('_tc&&(_tc.content=`#0b0f12`);'),
      'browsers that honour theme-color match too')

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
