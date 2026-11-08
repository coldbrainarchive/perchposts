#!/usr/bin/env python3
"""Patch v782 -> v784 (v783 country tagging was rolled back):
A country chip also searches for its name.
1. Selecting a chip, or opening ?country=X from a post's flag, fills the search box with the country.
2. Removing the chip clears that text.
3. The feed treats the chip as a search for that word, plus that country's own feed articles.
4. Typing a different word next to a chip still means "this word, within this country's feed".
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v782.js'
dst = '_deploy/assets/index-DUcNPOLc-v784.js'

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

# Search bar: keep the text in step with the country chip
patch(t('[qM,setQM]=(0,_.useState)(!1);(0,_.useEffect)(()=>{let e=setTimeout('),
      t('[qM,setQM]=(0,_.useState)(!1),_pc=(0,_.useRef)(``);'
        '(0,_.useEffect)(()=>{let _was=_pc.current;_pc.current=p;if(p===_was)return;'
        'let _v=(c.current?.value||``).trim().toLowerCase(),_same=!_v||_v===_was.toLowerCase();'
        'if(_same){r(p);if(c.current)c.current.value=p}},[p]);'
        '(0,_.useEffect)(()=>{let e=setTimeout('),
      'search text follows country chip')
patch(t('function k(n){let i=new URLSearchParams(e);i.set(`country`,n),i.delete(`continent`),t(i),r(``),s(null);if(c.current){c.current.value=``;c.current.focus();}}'),
      t('function k(n){let i=new URLSearchParams(e);i.set(`country`,n),i.delete(`continent`),t(i),r(``),s(null),a(!1);if(c.current){c.current.value=``;c.current.blur();}}'),
      'choosing a chip closes the dropdown')

# Feed: chip = search for its name
patch(t('m=(l.get(`q`)||``).toLowerCase().trim(),qT='),
      t('m=(l.get(`q`)||l.get(`country`)||``).toLowerCase().trim(),_cs=!!f&&m===f.toLowerCase(),qT='),
      'chip acts as a search')
patch(t('fetch(`${R}/get-posts?search=${encodeURIComponent(m)}&limit=1000`)'),
      t('fetch(`${R}/get-posts?search=${encodeURIComponent(m)}&limit=1000${_cs?`&country=${encodeURIComponent(f)}`:``}`)'),
      'chip search includes country feed')
patch('.catch(()=>{setSR(null);setSRLoading(!1)})},[m])',
      '.catch(()=>{setSR(null);setSRLoading(!1)})},[m,f])',
      'rerun search when chip changes')
patch('.filter(e=>!d||e.continent===d).filter(e=>!f||e.country===f).filter(e=>!p||(e.username||``).toLowerCase()===p).filter(e=>{if(!m)return!0;'.replace('`', q),
      '.filter(e=>!d||e.continent===d).filter(e=>!f||_cs||e.country===f).filter(e=>!p||(e.username||``).toLowerCase()===p).filter(e=>{if(!m||(_cs&&e.country===f))return!0;'.replace('`', q),
      'keep search matches and country feed articles')
patch(t('children:`No results for "${m}"`}'),
      t('children:_cs?`No articles mentioning ${f} yet`:`No results for "${m}"`}'),
      'empty chip message')
patch(t('children:`Try a different spelling, or check if the user is registered`}'),
      t('children:_cs?`Check back soon`:`Try a different spelling, or check if the user is registered`}'),
      'empty chip hint')

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
