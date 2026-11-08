#!/usr/bin/env python3
"""Patch v821 -> v822: the preview's Pinned and Latest titles become one row each: a pill, a thin line
and the date. Each row replaces the date divider that used to sit right under the title.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v821.js'
dst = '_deploy/assets/index-DUcNPOLc-v822.js'

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

patch(t('_st=_x=>(0,L.jsx)(`div`,{className:`chat-section-title`,children:_x},`st-`+_x);'),
      t('_df=_d=>{let _n=new Date(),_dt=new Date(_d),_t=new Date(_n.getFullYear(),_n.getMonth(),_n.getDate()),_dd=new Date(_dt.getFullYear(),_dt.getMonth(),_dt.getDate());if(_dd.getTime()===_t.getTime())return`Today`;if(_dd.getTime()===_t.getTime()-864e5)return`Yesterday`;return _dt.toLocaleDateString(void 0,{month:`short`,day:`numeric`,year:_dt.getFullYear()!==_n.getFullYear()?`numeric`:void 0})},'
        '_st=(_x,_c,_d)=>{if(String(_out[_out.length-1]?.key).startsWith(`dsep-`))_out.pop();_out.push((0,L.jsxs)(`div`,{className:`chat-section-title`,children:[(0,L.jsx)(`span`,{className:`chat-section-pill`+_c,children:_x}),(0,L.jsx)(`i`,{}),(0,L.jsx)(`b`,{children:_df(_d)})]},`st-`+_x))};'),
      'title row')
patch(t('if(_np){if(_i===_nl-1)_out.push(_st(`Latest`));if(_i===_rev.length-1)_out.push(_st(`Pinned`))}'),
      t('if(_np){if(_i===_nl-1)_st(`🕒 Latest`,``,_e.created_at);if(_i===_rev.length-1)_st(`📌 Pinned`,` pinned`,_e.created_at)}'),
      'use title row')
patch('.chat-section-title{font-size:12px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.07em;padding:6px 4px 4px}',
      '.chat-section-title{display:flex;align-items:center;gap:10px;padding:8px 0 6px}'
      '.chat-section-title i{flex:1;height:1px;background:rgba(148,163,184,0.12)}'
      '.chat-section-title b{font-size:11px;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:0.07em;white-space:nowrap}'
      '.chat-section-pill{display:inline-flex;align-items:center;height:24px;padding:0 10px;border-radius:999px;border:1px solid #323b48;background:#20262f;color:#cbd5e1;font-size:11px;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;white-space:nowrap}'
      '.chat-section-pill.pinned{border-color:rgba(192,132,252,0.5);background:rgba(192,132,252,0.14);color:#c084fc}',
      'title style')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
