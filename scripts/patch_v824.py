#!/usr/bin/env python3
"""Patch v823 -> v824: Find or a notification landing on a pinned chirp pulses its outline three times.
_glow's normal effect is the same shadow a pinned chirp already has, so it showed no change. The pulse
is a class, so the steady pinned glow comes back on its own when the animation ends.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v823.js'
dst = '_deploy/assets/index-DUcNPOLc-v824.js'

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

patch(t('function _glow(e){e=e.closest(`.chat-msg-body`)||e;'),
      t('function _glow(e){e=e.closest(`.chat-msg-body`)||e;if(e.classList.contains(`chat-pinned`)){e.classList.remove(`chat-flash`);void e.offsetWidth;e.classList.add(`chat-flash`);setTimeout(()=>e.classList.remove(`chat-flash`),1600);return}'),
      'pulse pinned chirps')
old = '.chat-msg-body.chat-pinned{box-shadow:0 0 0 4px rgba(192,132,252,0.6),0 0 20px rgba(192,132,252,0.8)}'
patch(old, old + '.chat-msg-body.chat-pinned.chat-flash{animation:chat-pin-flash .5s ease-in-out 3}'
      '@keyframes chat-pin-flash{0%,100%{box-shadow:0 0 0 4px rgba(192,132,252,0.6),0 0 20px rgba(192,132,252,0.8)}'
      '35%{box-shadow:0 0 0 1px rgba(192,132,252,0.15),0 0 0 rgba(192,132,252,0)}'
      '70%{box-shadow:0 0 0 6px rgba(216,180,254,1),0 0 34px rgba(192,132,252,1)}}', 'pulse style')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
