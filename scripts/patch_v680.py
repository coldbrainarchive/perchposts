#!/usr/bin/env python3
"""Patch v679 -> v680:
Remove shadow stack cards. Keep only the front image + number badge.
Also remove padding from containers (no longer needed without shadows).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v679.js'
dst = '_deploy/assets/index-DUcNPOLc-v680.js'

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

def rm_shadows(atts, border, container_old, container_new):
    q = chr(0x60)
    s2 = (atts + '.length>2&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
          + ',top:-13,left:-13,right:0,bottom:0,borderRadius:' + border
          + ',background:' + q + '#3a3d4e' + q + ',zIndex:0,transform:' + q + 'rotate(-5deg)' + q + '}}),')
    s1 = (atts + '.length>1&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
          + ',top:-7,left:-7,right:0,bottom:0,borderRadius:' + border
          + ',background:' + q + '#2e3140' + q + ',zIndex:0,transform:' + q + 'rotate(-2.5deg)' + q + '}}),')
    # Remove container padding
    patch(container_old, container_new, atts + ' container: remove padding')
    # Remove shadow 2
    patch(s2, '', atts + ' shadow 2: remove')
    # Remove shadow 1
    patch(s1, '', atts + ' shadow 1: remove')

rm_shadows(
    '_pAtts', '10',
    'marginTop:6,paddingTop:13,paddingLeft:13}',
    'marginTop:6}'
)
# _tAtts shadows already removed above; container needs no change (no padding was added)
patch(
    '_tAtts.length>2&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
    + ',top:-13,left:-13,right:0,bottom:0,borderRadius:10,background:' + q + '#3a3d4e' + q + ',zIndex:0,transform:' + q + 'rotate(-5deg)' + q + '}}),',
    '', '_tAtts shadow 2 (double-check)'
)
patch(
    '_tAtts.length>1&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
    + ',top:-7,left:-7,right:0,bottom:0,borderRadius:10,background:' + q + '#2e3140' + q + ',zIndex:0,transform:' + q + 'rotate(-2.5deg)' + q + '}}),',
    '', '_tAtts shadow 1 (double-check)'
)
rm_shadows(
    '_cAtts', '8',
    'marginBottom:_ct?8:0,paddingTop:13,paddingLeft:13}',
    'marginBottom:_ct?8:0}'
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
