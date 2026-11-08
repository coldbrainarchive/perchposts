#!/usr/bin/env python3
"""Patch v824 -> v825: the pinned chirp's flash is a plain off and on, twice, with no brighter peak."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v824.js'
dst = '_deploy/assets/index-DUcNPOLc-v825.js'

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

patch('.chat-msg-body.chat-pinned.chat-flash{animation:chat-pin-flash .5s ease-in-out 3}',
      '.chat-msg-body.chat-pinned.chat-flash{animation:chat-pin-flash .7s linear 2}', 'timing')
patch('@keyframes chat-pin-flash{0%,100%{box-shadow:0 0 0 4px rgba(192,132,252,0.6),0 0 20px rgba(192,132,252,0.8)}'
      '35%{box-shadow:0 0 0 1px rgba(192,132,252,0.15),0 0 0 rgba(192,132,252,0)}'
      '70%{box-shadow:0 0 0 6px rgba(216,180,254,1),0 0 34px rgba(192,132,252,1)}}',
      '@keyframes chat-pin-flash{0%,45%{box-shadow:0 0 0 0 rgba(192,132,252,0),0 0 0 rgba(192,132,252,0)}'
      '55%,100%{box-shadow:0 0 0 4px rgba(192,132,252,0.6),0 0 20px rgba(192,132,252,0.8)}}', 'off and on')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
