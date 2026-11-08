#!/usr/bin/env python3
"""Patch v665 -> v666:
Fix fullscreen cropping on desktop only.
In onPlay, attach a fullscreenchange listener that sets objectFit:contain
when entering fullscreen and restores objectFit:cover on exit.
Guard with _fsOf flag to avoid duplicate listeners across play cycles.
Desktop only (window.innerWidth >= 768). Mobile untouched.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v665.js'
dst = '_deploy/assets/index-DUcNPOLc-v666.js'

content = open(src, encoding='utf-8').read()
errors = []
q = chr(0x60)

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

patch(
    '_vp._io.observe(_vp);}',
    ('_vp._io.observe(_vp);'
     + 'if(window.innerWidth>=768&&!_vp._fsOf){'
     + '_vp._fsOf=()=>{_vp.style.objectFit=(document.fullscreenElement||document.webkitFullscreenElement)?' + q + 'contain' + q + ':' + q + 'cover' + q + ';};'
     + '_vp.addEventListener(' + q + 'fullscreenchange' + q + ',_vp._fsOf);'
     + '}}'),
    'desktop fullscreenchange listener: contain on enter, cover on exit'
)

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
