#!/usr/bin/env python3
"""Patch v697 -> v698:
Fix notification deep-link scroll/highlight:
1. Skip window.scrollTo(0,0) on mount when a highlight param is present
2. Skip the [u] effect's scroll-to-bottom when a highlight param is present
3. Replace smooth scrolling with instant jumps (scrollIntoView block:nearest + scrollTop)
4. Fire highlight immediately, no nested setTimeout
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v697.js'
dst = '_deploy/assets/index-DUcNPOLc-v698.js'

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

# 1. [r] effect: skip scroll-to-top when highlight param is set
patch(
    '(0,_.useEffect)(()=>{window.scrollTo(0,0)},[r]);',
    '(0,_.useEffect)(()=>{if(!a)window.scrollTo(0,0)},[r]);',
    '[r] effect: skip scrollTo(0,0) when highlight param set'
)

# 2. [u] effect: skip scroll-to-bottom when highlight param is set
old_u = ('requestAnimationFrame(()=>requestAnimationFrame(()=>{let e=D.current;if(e)e.scrollTop=0;'
         'window.scrollTo(0,document.body.scrollHeight);setTimeout(()=>{if(e)e.scrollTop=0;},100);}))}'
         ',[u])')
new_u = ('if(!a){requestAnimationFrame(()=>requestAnimationFrame(()=>{let e=D.current;if(e)e.scrollTop=0;'
         'window.scrollTo(0,document.body.scrollHeight);setTimeout(()=>{if(e)e.scrollTop=0;},100);}))}'
         '},[u])')
patch(old_u, new_u, '[u] effect: skip scroll-to-bottom when highlight param set')

# 3. [u,a] effect: instant scroll + immediate highlight, no animation
old_highlight = ('let n=document.querySelector(' + q + '.comments-shell' + q + ');'
                 'n&&n.scrollIntoView({behavior:' + q + 'smooth' + q + '}),'
                 'setTimeout(()=>{let n=Math.max(0,t.offsetTop-e.clientHeight/2+t.offsetHeight/2);'
                 'e.scrollTo({top:n,behavior:' + q + 'smooth' + q + '});'
                 'let _b=t.querySelector(' + q + '.chat-bubble' + q + ');'
                 '_b&&(_b.classList.add(' + q + 'highlight' + q + '),'
                 'setTimeout(()=>_b.classList.remove(' + q + 'highlight' + q + '),2500));'
                 '},350),'
                 'setTimeout(()=>o(' + q + '/post/${r}' + q + ',{replace:!0}),1200)')

new_highlight = ('let _cs=document.querySelector(' + q + '.comments-shell' + q + ');'
                 '_cs&&_cs.scrollIntoView({block:' + q + 'nearest' + q + '});'
                 'let _n=Math.max(0,t.offsetTop-e.clientHeight/2+t.offsetHeight/2);'
                 'e.scrollTop=_n;'
                 'let _b=t.querySelector(' + q + '.chat-bubble' + q + ');'
                 '_b&&(_b.classList.add(' + q + 'highlight' + q + '),'
                 'setTimeout(()=>_b.classList.remove(' + q + 'highlight' + q + '),2500));'
                 'setTimeout(()=>o(' + q + '/post/${r}' + q + ',{replace:!0}),1500)')

patch(old_highlight, new_highlight, '[u,a] effect: instant scroll + immediate highlight')

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
