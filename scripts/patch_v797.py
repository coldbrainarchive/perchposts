#!/usr/bin/env python3
"""Patch v796 -> v797:
Use the browser's own pull to refresh everywhere. Removes the custom one: its document-wide touch
handlers, spinner strip and pull offset. The chat screen keeps overscroll off, so pulling inside
it doesn't refresh the page.
"""
import re
import sys

src = '_deploy/assets/index-DUcNPOLc-v796.js'
dst = '_deploy/assets/index-DUcNPOLc-v797.js'

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

def cut(start, end, new, label):
    global content
    if content.count(start) != 1:
        errors.append('FAIL (' + label + '): start marker found ' + str(content.count(start)) + ' times')
        return
    a = content.index(start)
    b = content.find(end, a)
    if b < 0:
        errors.append('FAIL (' + label + '): end marker missing')
        return
    content = content[:a] + new + content[b + len(end):]
    print('OK: ' + label + ' (' + str(b + len(end) - a) + ' chars removed)')

def t(s):
    return s.replace('`', q)

cut('(0,_.useEffect)(()=>{let e=e=>{x.current.startX=',
    'let S=(0,_.useRef)(0);return(0,_.useEffect)(()=>{S.current=g},[g]),(0,L.jsx)(Vn,',
    'return (0,L.jsx)(Vn,',
    'touch handlers')
cut(t('(0,L.jsx)(`div`,{className:`ptr-strip`'),
    t('(0,L.jsx)(`style`,{children:`@keyframes ptr-spin { to { transform: rotate(360deg); } }`}),'),
    '',
    'spinner strip')
patch(t('(0,L.jsxs)(`nav`,{className:`app-topbar`,style:{marginTop:`${g*60}px`},children:['),
      t('(0,L.jsxs)(`nav`,{className:`app-topbar`,children:['),
      'top bar offset')
patch('let[g,v]=(0,_.useState)(0),[y,b]=(0,_.useState)(!1),x=(0,_.useRef)({startX:0,startY:0,active:!1});',
      '',
      'pull state')
patch('html.chat-open .ptr-strip{display:none!important}',
      'html.chat-open,html.chat-open body{overscroll-behavior-y:none}',
      'no page refresh from inside the chat')

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
