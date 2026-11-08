#!/usr/bin/env python3
"""Patch v791 -> v792:
Pull to refresh could stick with the page pushed down and a frozen spinner. Each touchmove queued
an animation frame that re-applied the pull distance; letting go before that frame ran reset the
pull, then the frame set it back, and nothing cleared it.
1. Letting go cancels the queued frame and clears the pull distance.
2. The full-pull check reads the live distance, not the last rendered one.
3. A cancelled touch (the system taking over) resets instead of reloading.
4. If the reload doesn't happen (offline), the spinner clears after 5s.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v791.js'
dst = '_deploy/assets/index-DUcNPOLc-v792.js'

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

patch('requestAnimationFrame(()=>v(x.current.pullY||0));return}x.current.active&&(x.current.active=!1,requestAnimationFrame(()=>v(0)))},',
      'cancelAnimationFrame(x.current.raf);x.current.raf=requestAnimationFrame(()=>v(x.current.pullY||0));return}'
      'x.current.active&&(x.current.active=!1,x.current.pullY=0,cancelAnimationFrame(x.current.raf),v(0))},',
      'one queued frame at a time')
patch('n=()=>{x.current.active&&S.current>=1?(b(!0),setTimeout(()=>window.location.reload(),300)):v(0),x.current.active=!1};',
      t('n=_ev=>{let _full=_ev.type===`touchend`&&x.current.active&&(x.current.pullY||0)>=1;cancelAnimationFrame(x.current.raf);'
        'x.current.active=!1;x.current.pullY=0;x.current.hapticFired=!1;'
        'if(_full){v(1);b(!0);setTimeout(()=>window.location.reload(),300);setTimeout(()=>{b(!1);v(0)},5e3)}else v(0)};'),
      'letting go always clears the pull')

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
