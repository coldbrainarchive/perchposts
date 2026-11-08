#!/usr/bin/env python3
"""Patch v797 -> v798:
The top bar and chat title header use the page colour, which is what the browser shows behind pull
to refresh and in the status bar, instead of near-black. Popup panels keep their darker shade.
"""
import re
import sys

src = '_deploy/assets/index-DUcNPOLc-v797.js'
dst = '_deploy/assets/index-DUcNPOLc-v798.js'

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

m = re.search(r'\.app-topbar \{[^}]*?background: #0b0f12;', content)
if not m:
    errors.append('FAIL (top bar): rule not found')
else:
    content = content[:m.start()] + m.group(0).replace('#0b0f12', '#16171d') + content[m.end():]
    print('OK: top bar')

patch('.chat-full .chat-panel-header{background:#0b0f12;border-top:env(safe-area-inset-top) solid #0b0f12}',
      '.chat-full .chat-panel-header{background:#16171d;border-top:env(safe-area-inset-top) solid #16171d}',
      'chat title header')
patch('_tc&&(_tc.content=' + q + '#0b0f12' + q + ');',
      '_tc&&(_tc.content=' + q + '#16171d' + q + ');',
      'browser colour in the chat')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
