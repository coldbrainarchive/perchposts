#!/usr/bin/env python3
"""Patch v198 -> v199: highlight always fires on click; clears URL param after so re-clicks work."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v198.js'
dst = '_deploy/assets/index-DUcNPOLc-v199.js'

content = open(src, encoding='utf-8').read()
errors = []

# Remove the k.current guard entirely and the reset effect from v198.
# After scrolling, clear the ?highlight param from the URL (replace:true) so that:
# - page refreshes don't keep re-triggering the scroll
# - clicking the same notification again sets the param fresh → effect re-runs → scrolls again
OLD = (
    'k.current=!1;},[a]);'
    '(0,_.useEffect)(()=>{'
    'if(!a||k.current)return;'
    'let e=D.current,t=e?.querySelector(`[data-comment-id="${a}"]`);'
    'if(!t)return;k.current=!0;'
    'let n=document.querySelector(`.comments-shell`);'
    'n&&n.scrollIntoView({behavior:`smooth`}),'
    'setTimeout(()=>{'
    'let n=Math.max(0,t.offsetTop-e.clientHeight/2+t.offsetHeight/2);'
    'e.scrollTo({top:n,behavior:`smooth`}),'
    'setTimeout(()=>{'
    'let e=t.querySelector(`.chat-bubble`);'
    'e&&(e.classList.add(`highlight`),setTimeout(()=>e.classList.remove(`highlight`),2500))'
    '},400)},450)},[u,a])'
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
    # After scroll settles, clear the highlight param so refresh doesn't re-scroll,
    # but a fresh click on the same notification sets it again → works every time
    'setTimeout(()=>o(`/post/${r}`,{replace:!0}),700)'
    '},[u,a])'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: highlight always fires; URL cleared after scroll')
else:
    errors.append('FAIL: highlight effect not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
