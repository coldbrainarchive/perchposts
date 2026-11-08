#!/usr/bin/env python3
"""Patch v807 -> v808:
Remove the temporary ?vvdebug readout and swipe counter. The reset from v807 stays, unchanged.

Measured with Web Inspector on a real iPhone (Safari, iOS 27.2): every time the keyboard opens, Safari
scrolls the locked page by the keyboard's height (303), and innerHeight shrinks along with the visual
viewport (695 to 392). So the "keyboard is down" check in _rs passes while the keyboard is up, and the
reset clears that scroll about 350ms after the keyboard opens, not when it closes. That is what stopped
the freezing, so don't tighten the check without retesting on a phone.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v807.js'
dst = '_deploy/assets/index-DUcNPOLc-v808.js'

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

start_mark = t('_dv=/vvdebug/.test(location.search),')
end_mark = '_f=()=>{cancelAnimationFrame(_r);if(!_rt)'
if content.count(start_mark) != 1 or content.count(end_mark) != 1:
    errors.append('FAIL: debug block not found exactly once')
else:
    a = content.index(start_mark)
    b = content.index(end_mark)
    block = content[a:b]
    if not (block.endswith('},') and '_tmv=' in block and len(block) < 2000):
        errors.append('FAIL: debug block looks wrong (' + str(len(block)) + ' chars)')
    else:
        content = content[:a] + content[b:]
        print('OK: remove readout (' + str(len(block)) + ' chars)')

patch('_rc=0,_ro=0,_rt=0,_rd=!1,', '_rt=0,_rd=!1,', 'drop reset counters')
patch('_rd=!0;_rc++;_ro=_o;window.scrollTo(0,0);', '_rd=!0;window.scrollTo(0,0);', 'reset no longer counts')
patch(t('.test(document.activeElement?.tagName||``));_ds()})}'),
      t('.test(document.activeElement?.tagName||``))})}'),
      'stop calling the readout')
patch(t('_fo();if(_dv){document.addEventListener(`touchstart`,_tsd,{passive:!0});document.addEventListener(`touchmove`,_tmv,{passive:!0})}document.addEventListener(`focusin`,_fo);'),
      t('_fo();document.addEventListener(`focusin`,_fo);'),
      'stop watching swipes')
patch(t('document.removeEventListener(`touchstart`,_tsd);document.removeEventListener(`touchmove`,_tmv);document.getElementById(`vvd`)?.remove();'),
      '', 'nothing to clean up')

for gone in ('vvdebug', '_ds(', '_tsd', '_tmv', 'vvd`'):
    if gone in content:
        errors.append('FAIL: still contains ' + gone)

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
