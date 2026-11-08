#!/usr/bin/env python3
"""Patch v803 -> v804:
Chrome on iPhone: measured on a real phone, the page went from 761 to 662 tall when the chat opened
with Chrome's bars shrunk (screen 852, lvh 761, svh 662), leaving 99 empty points under the chat.
The chat lifts everything out of the page, so the document was shorter than the screen, and Chrome
then uses its full-bars size without bringing the bars back. Keep the document a little taller than
the largest viewport while the chat is open. Only for Chrome on iOS; Safari is untouched.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v803.js'
dst = '_deploy/assets/index-DUcNPOLc-v804.js'

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

patch(t('_h.classList.add(`chat-open`);_b.position=`fixed`;'),
      t('_h.classList.add(`chat-open`);/CriOS/.test(navigator.userAgent)&&_h.classList.add(`chat-crios`);_b.position=`fixed`;'),
      'mark Chrome on iOS')
patch(t('_h.classList.remove(`chat-open`,`chat-kb`);'),
      t('_h.classList.remove(`chat-open`,`chat-kb`,`chat-crios`);'),
      'clear it on close')
patch('html:not(.chat-kb) .comments-shell.chat-full{height:auto;bottom:0;transform:none}',
      'html:not(.chat-kb) .comments-shell.chat-full{height:auto;bottom:0;transform:none}html.chat-crios{min-height:calc(100lvh + 2px)}',
      'keep the page scrollable')
patch(t('_e.textContent=`v803 before:'), t('_e.textContent=`v804 before:'), 'readout version')

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
