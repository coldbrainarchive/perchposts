#!/usr/bin/env python3
"""Patch v696 -> v697:
Fix notification highlight so it always fires, even when comment is already visible.
Problem: highlight was nested inside scroll callback (fires at 450+400=850ms), and
the URL replace fired at 700ms potentially causing a race. If the comment was already
in view, the nested timing was fragile.
Fix: un-nest highlight from scroll callback — it fires at 350ms independently,
well before the URL replace which is pushed to 1200ms.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v696.js'
dst = '_deploy/assets/index-DUcNPOLc-v697.js'

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

# Old: scroll at 450ms → nested: highlight at 850ms total; URL replace at 700ms
# New: scroll+highlight together at 350ms; URL replace at 1200ms
old_block = ('setTimeout(()=>{let n=Math.max(0,t.offsetTop-e.clientHeight/2+t.offsetHeight/2);'
             'e.scrollTo({top:n,behavior:' + q + 'smooth' + q + '}),'
             'setTimeout(()=>{let e=t.querySelector(' + q + '.chat-bubble' + q + ');'
             'e&&(e.classList.add(' + q + 'highlight' + q + '),'
             'setTimeout(()=>e.classList.remove(' + q + 'highlight' + q + '),2500))},'
             '400)},450),'
             'setTimeout(()=>o(' + q + '/post/${r}' + q + ',{replace:!0}),700)')

new_block = ('setTimeout(()=>{let n=Math.max(0,t.offsetTop-e.clientHeight/2+t.offsetHeight/2);'
             'e.scrollTo({top:n,behavior:' + q + 'smooth' + q + '});'
             'let _b=t.querySelector(' + q + '.chat-bubble' + q + ');'
             '_b&&(_b.classList.add(' + q + 'highlight' + q + '),'
             'setTimeout(()=>_b.classList.remove(' + q + 'highlight' + q + '),2500));'
             '},350),'
             'setTimeout(()=>o(' + q + '/post/${r}' + q + ',{replace:!0}),1200)')

patch(old_block, new_block, 'highlight: un-nest from scroll, fire at 350ms, replace URL at 1200ms')

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
