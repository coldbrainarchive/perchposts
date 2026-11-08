#!/usr/bin/env python3
"""Patch v199 -> v200: fix nested useEffect bug from v199 patch."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v199.js'
dst = '_deploy/assets/index-DUcNPOLc-v200.js'

content = open(src, encoding='utf-8').read()
errors = []

# The v199 patch left an orphaned (0,_.useEffect)(()=>{ wrapping the highlight effect.
# Fix: remove the extra wrapper.
OLD = (
    '(0,_.useEffect)(()=>{'
    '(0,_.useEffect)(()=>{'
    'if(!a)return;'
    'let e=D.current,t=e?.querySelector(`[data-comment-id="${a}"]`);'
    'if(!t)return;'
    'let n=document.querySelector(`.comments-shell`);'
    'n&&n.scrollIntoView({behavior:`smooth`}),'
    'setTimeout(()=>{'
    'let n=Math.max(0,t.offsetTop-e.clientHeight/2+t.offsetHeight/2);'
    'e.scrollTo({top:n,behavior:`smooth`}),'
    'setTimeout(()=>{'
    'let e=t.querySelector(`.chat-bubble`);'
    'e&&(e.classList.add(`highlight`),setTimeout(()=>e.classList.remove(`highlight`),2500))'
    '},400)},450),'
    'setTimeout(()=>o(`/post/${r}`,{replace:!0}),700)'
    '},[u,a])'
)
NEW = (
    '(0,_.useEffect)(()=>{'
    'if(!a)return;'
    'let e=D.current,t=e?.querySelector(`[data-comment-id="${a}"]`);'
    'if(!t)return;'
    'let n=document.querySelector(`.comments-shell`);'
    'n&&n.scrollIntoView({behavior:`smooth`}),'
    'setTimeout(()=>{'
    'let n=Math.max(0,t.offsetTop-e.clientHeight/2+t.offsetHeight/2);'
    'e.scrollTo({top:n,behavior:`smooth`}),'
    'setTimeout(()=>{'
    'let e=t.querySelector(`.chat-bubble`);'
    'e&&(e.classList.add(`highlight`),setTimeout(()=>e.classList.remove(`highlight`),2500))'
    '},400)},450),'
    'setTimeout(()=>o(`/post/${r}`,{replace:!0}),700)'
    '},[u,a])'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: nested useEffect removed')
else:
    errors.append('FAIL: nested useEffect pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
