#!/usr/bin/env python3
"""Patch v700 -> v701:
Fix 'just commented' notifications that have no targetId.
1. Notification link: add ?nc=1 when targetId is absent so post detail knows
   it came from a notification even without a specific comment to highlight.
2. Post detail: read _nc from URL params.
3. [r] effect: also skip scrollTo(0,0) when _nc is set.
4. [u] effect: when _nc is set (no specific comment), scroll to bottom (show newest)
   and blink the first chat-bubble (newest comment in column-reverse).
5. URL cleanup: remove ?nc=1 after 1500ms.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v700.js'
dst = '_deploy/assets/index-DUcNPOLc-v701.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append('FAIL (' + label + '): not found')
    elif n > 1:
        errors.append('FAIL (' + label + '): ' + str(n) + ' matches')
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

# 1. Notification link: add ?nc=1 when no targetId
patch(
    'e.postId?' + q + '/post/${e.postId}${e.targetId?' + q + '?highlight=${e.targetId}' + q + ':' + q + q + '}' + q + ':`#`',
    'e.postId?' + q + '/post/${e.postId}${e.targetId?' + q + '?highlight=${e.targetId}' + q + ':' + q + '?nc=1' + q + '}' + q + ':`#`',
    'notification link: add ?nc=1 when no targetId'
)

# 2. Post detail: read _nc = i.get('nc') alongside a = i.get('highlight')
patch(
    'a=i.get(' + q + 'highlight' + q + '),o=nt()',
    'a=i.get(' + q + 'highlight' + q + '),_nc=i.get(' + q + 'nc' + q + '),o=nt()',
    'post detail: read _nc from URL params'
)

# 3. [r] effect: skip scrollTo(0,0) when _nc is set too
patch(
    'if(!a)window.scrollTo(0,0)},[r]);',
    'if(!a&&!_nc)window.scrollTo(0,0)},[r]);',
    '[r] effect: also skip scroll-to-top when _nc set'
)

# 4. [u] effect: when _nc, scroll to newest comment and blink first chat-bubble
old_u = ('if(!a){requestAnimationFrame(()=>requestAnimationFrame(()=>{let e=D.current;if(e)e.scrollTop=0;window.scrollTo(0,document.body.scrollHeight);setTimeout(()=>{if(e)e.scrollTop=0;},100);}))}'
         '},[u])')
new_u = ('if(!a){requestAnimationFrame(()=>requestAnimationFrame(()=>{let e=D.current;if(e)e.scrollTop=0;window.scrollTo(0,document.body.scrollHeight);setTimeout(()=>{if(e)e.scrollTop=0;},100);'
         'if(_nc){let _b=e&&e.querySelector(' + q + '.chat-bubble' + q + ');'
         'if(_b){let _bn=0;const _bl=()=>{'
         '_b.style.background=' + q + 'rgba(192,132,252,0.38)' + q + ';'
         '_b.style.outline=' + q + '2px solid rgba(192,132,252,0.75)' + q + ';'
         'setTimeout(()=>{_b.style.background=' + q + q + ';_b.style.outline=' + q + q + ';_bn++;if(_bn<3)setTimeout(_bl,130);},350)};_bl();}'
         'setTimeout(()=>o(' + q + '/post/${r}' + q + ',{replace:!0}),1800);}}))}'
         '},[u])')
patch(old_u, new_u, '[u] effect: blink newest comment when _nc set')

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
