#!/usr/bin/env python3
"""Patch v818 -> v819:
Find jumps straight to the parent chirp and glows it, the same effect as opening a notification. It
centres the chirp by scrolling the chat only, so the page doesn't move on desktop.
Pinned chirps keep that same glow all the time. It's a class, not an inline style, because _glow clears
the inline box-shadow when it finishes, which would wipe a pinned glow after a Find.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v818.js'
dst = '_deploy/assets/index-DUcNPOLc-v819.js'

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

patch(t('if(t&&n){let e=n.offsetTop;t.scrollTo({top:e,behavior:`smooth`});let r=n.querySelector(`.chat-bubble`);r&&setTimeout(()=>{r.classList.add(`highlight`),setTimeout(()=>r.classList.remove(`highlight`),1e3)},500)}}'),
      t('if(t&&n){let _a=n.getBoundingClientRect(),_w=t.getBoundingClientRect();t.scrollTop+=_a.top-_w.top-(t.clientHeight-_a.height)/2;requestAnimationFrame(()=>_glow(n.querySelector(`.chat-msg-body`)||n))}}'),
      'find')

patch(t('(0,L.jsxs)(`div`,{className:`chat-msg-body`,children:['),
      t('(0,L.jsxs)(`div`,{className:`chat-msg-body${e.pinned?` chat-pinned`:``}`,children:['),
      'pinned class')

old = '.comments-shell .chat-panel-header .feed-post-action-pill{height:26px;padding:0 10px;font-size:13px}'
patch(old, old + '.chat-msg-body.chat-pinned{box-shadow:0 0 0 4px rgba(192,132,252,0.6),0 0 20px rgba(192,132,252,0.8)}', 'pinned glow')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
