#!/usr/bin/env python3
"""Patch v899 -> v900: search dropdown gets a three-way slider (Boards | Regions | Filters), like the
comment page's Oldest/Newest toggle. Remembers the last tab. While typing, the slider hides and matches from
everything show as before.

Filters tab:
  Sort  - 🪶 Flock (moved here from Boards; still ?board=activity underneath) and 🪽 Most flaps, this week
          (?sort=flaps, served by the worker's new get-posts?sort=flaps)
  Bots  - All / Hide bots (?bot=hide, worker get-posts?people=1) / Only bots (?bot=only)
  Time  - Day picker first, then Hour (was Hour first); replaces the 🕐 button in the corner.
Filters combine with board, region and country selections (filtered on the page). New chips in the search
bar for Most flaps and Hide bots; tap to clear. The box stays open after a filter tap (only boards close it).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v899.js'
dst = '_deploy/assets/index-DUcNPOLc-v900.js'
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n != 1:
        errors.append('FAIL (' + label + '): found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

# ── Feed component ─────────────────────────────────────────────────────────────
patch('[TagR,setTagR]=(0,_.useState)(_sn?.tag??null),',
      '[TagR,setTagR]=(0,_.useState)(_sn?.tag??null),[FR,setFR]=(0,_.useState)(null),[PR,setPR]=(0,_.useState)(null),',
      'feed: flaps/people state')
patch('_bot=l.get(`bot`)||``,', '_bot=l.get(`bot`)||``,_srt=l.get(`sort`)||``,', 'feed: sort param')
patch('},[qT]),',
      '},[qT]),'
      '(0,_.useEffect)(()=>{if(_srt!==`flaps`){setFR(null);return}let _c=!1;fetch(`${R}/get-posts?sort=flaps`).then(r2=>r2.ok?r2.json():{posts:[]}).then(d2=>{if(!_c)setFR(Sr((d2.posts||[]).filter(e2=>{const t2=cr(e2);return t2!==`The Cage`&&t2!==`Jail`})))}).catch(()=>{if(!_c)setFR([])});return()=>{_c=!0}},[_srt]),'
      '(0,_.useEffect)(()=>{if(_bot!==`hide`){setPR(null);return}let _c=!1;fetch(`${R}/get-posts?people=1`).then(r2=>r2.ok?r2.json():{posts:[]}).then(d2=>{if(!_c)setPR(Sr((d2.posts||[]).filter(e2=>{const t2=cr(e2);return t2!==`The Cage`&&t2!==`Jail`})))}).catch(()=>{if(!_c)setPR([])});return()=>{_c=!0}},[_bot]),',
      'feed: fetch flaps/people')
patch('},[u,d,f,p,m,qT]),', '},[u,d,f,p,m,qT,_srt,_bot]),', 'feed: reset scroll on new filters')
patch('_bl0=m&&SR!==null?SR:',
      '_bl0=m&&SR!==null?SR:_srt===`flaps`?(FR||[]):_bot===`hide`?(PR||[]):',
      'feed: base list')
patch('_bl=(_pgR.current=_om!==void 0,_old.length?',
      '_bl=(_pgR.current=_om!==void 0,_old.length&&!(_srt===`flaps`||_bot===`hide`)?',
      'feed: no older pages on flaps/people')
patch('.filter(e=>!_bot||!!(e.browser_id&&String(e.browser_id).startsWith(`bot-`)))',
      '.filter(e=>{if(!_bot)return!0;const _ib=fr.includes(e.username)||!!(e.browser_id&&String(e.browser_id).startsWith(`bot-`));return _bot===`hide`?!_ib:_ib})',
      'feed: bots filter')
patch('.filter(e=>!d||(!m&&TagR!==null)||_rgnHit(e,d))',
      '.filter(e=>!d||(!m&&TagR!==null&&_bl0===TagR)||_rgnHit(e,d))',
      'feed: region filter on new lists')
patch('if(!qT||m||TR!==null)return!0',
      'if(!qT||m||(TR!==null&&_bl0===TR))return!0',
      'feed: time filter on new lists')
patch('.sort((e,t)=>{let n=(t.pinned_global?1:0)-(e.pinned_global?1:0);return n===0?_y||_cs?',
      '.sort((e,t)=>{let n=(t.pinned_global?1:0)-(e.pinned_global?1:0);return n===0?_srt===`flaps`?(t.flaps||0)-(e.flaps||0):_y||_cs?',
      'feed: sort by flaps')
patch('m&&!SRLoading&&SR!==null&&b.length===0&&',
      '!m&&_srt===`flaps`&&FR!==null&&b.length===0&&(0,L.jsx)(`div`,{style:{padding:`48px 20px`,textAlign:`center`,color:`#64748b`},children:`No flapped posts this week yet`}),'
      '!m&&_bot===`hide`&&PR!==null&&b.length===0&&(0,L.jsx)(`div`,{style:{padding:`48px 20px`,textAlign:`center`,color:`#64748b`},children:`No posts from people here yet`}),'
      'm&&!SRLoading&&SR!==null&&b.length===0&&',
      'feed: empty states')

patch('_canMore&&o>=b.length&&(0,L.jsx)(`button`,{onClick:_loadOlder,',
      '_canMore&&_srt!==`flaps`&&_bot!==`hide`&&o>=b.length&&(0,L.jsx)(`button`,{onClick:_loadOlder,',
      'feed: no Load older on flaps/people')

# ── Search component ───────────────────────────────────────────────────────────
TABS = (
    "let[_tab,_setTab]=(0,_.useState)(()=>{try{return localStorage.getItem(`srchTab`)||`boards`}catch{return`boards`}}),"
    "_pickTab=k=>{_setTab(k);try{localStorage.setItem(`srchTab`,k)}catch{}},"
    "_srt=e.get(`sort`)||``,"
    "_setParam=(k,v)=>{let n=new URLSearchParams(e);v?n.set(k,v):n.delete(k);t(n)},"
    "_chipS={display:`inline-flex`,alignItems:`center`,gap:5,height:22,padding:`0 8px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,background:`#c084fc`,color:`#0a0a0a`,fontSize:10,fontWeight:800,letterSpacing:`0.03em`,textTransform:`uppercase`,whiteSpace:`nowrap`,lineHeight:1,flexShrink:0,cursor:`pointer`},"
    "_stb=(k,lbl)=>(0,L.jsx)(`button`,{type:`button`,className:`srch-tab`+(_tab===k?` active`:``),onMouseDown:ev=>ev.preventDefault(),onClick:ev=>{ev.stopPropagation();_pickTab(k)},children:lbl},k),"
    "_pill=(on,lbl,fn)=>(0,L.jsx)(`button`,{type:`button`,className:`srch-opt`+(on?` active`:``),onClick:fn,children:lbl},lbl),"
    "_today=(()=>{const d0=new Date();return d0.getFullYear()+`-`+(d0.getMonth()+1).toString().padStart(2,`0`)+`-`+d0.getDate().toString().padStart(2,`0`)})(),"
    "_TABS=()=>(0,L.jsxs)(L.Fragment,{children:["
      "(0,L.jsxs)(`div`,{className:`srch-tabs`,children:[_stb(`boards`,`Boards`),_stb(`regions`,`Regions`),_stb(`filters`,`Filters`)]}),"
      "_tab===`boards`&&(0,L.jsx)(`div`,{className:`search-column srch-body`,children:g.filter(x=>x.slug!==`activity`).map(x=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>ee(x.slug),children:(0,L.jsx)(Ar,{boardName:x.name,small:!0})},x.slug))}),"
      "_tab===`regions`&&(0,L.jsx)(`div`,{className:`search-column srch-body`,children:v.map(x=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>{D(x),x!==`World`&&O(x)},children:(0,L.jsx)(kr,{continent:x,small:!0})},x))}),"
      "_tab===`filters`&&(0,L.jsxs)(`div`,{className:`srch-filters`,children:["
        "(0,L.jsx)(`div`,{className:`search-section-label`,children:`Sort`}),"
        "(0,L.jsxs)(`div`,{className:`srch-row`,children:["
          "_pill(d===`activity`,`🪶 Flock`,()=>{if(d===`activity`)A();else ee(`activity`)}),"
          "_pill(_srt===`flaps`,`🪽 Most flaps · this week`,()=>_setParam(`sort`,_srt===`flaps`?``:`flaps`))]}),"
        "(0,L.jsx)(`div`,{className:`search-section-label`,children:`Bots`}),"
        "(0,L.jsxs)(`div`,{className:`srch-row`,children:["
          "_pill(!_botF,`All`,()=>_setParam(`bot`,``)),"
          "_pill(_botF===`hide`,`Hide bots`,()=>_setParam(`bot`,`hide`)),"
          "_pill(!!_botF&&_botF!==`hide`,`Only bots`,()=>_setParam(`bot`,`only`))]}),"
        "(0,L.jsx)(`div`,{className:`search-section-label`,children:`Time`}),"
        "(0,L.jsxs)(`div`,{className:`srch-row`,children:["
          "_pill(!q2,`Any time`,()=>ae()),"
          "(0,L.jsx)(`input`,{type:`date`,className:`srch-time`+(q2&&q2.includes(`-`)?` active`:``),value:q2&&q2.includes(`-`)?q2:_today,max:_today,"
            "onChange:ev=>{ev.target.value&&oe(ev.target.value)},onMouseDown:ev=>ev.stopPropagation(),onTouchStart:ev=>ev.stopPropagation()}),"
          "(0,L.jsxs)(`select`,{className:`srch-time`+(q2&&q2.startsWith(`ago_`)?` active`:``),value:q2&&q2.startsWith(`ago_`)?q2.slice(4):``,"
            "onChange:ev=>{ev.target.value&&oe(`ago_`+ev.target.value)},children:[(0,L.jsx)(`option`,{value:``,children:`Hour…`}),"
            "Array.from({length:24},(_,i)=>(0,L.jsx)(`option`,{value:i+1,children:(i+1)+`h ago`},i+1))]})]})]})]});"
)
patch('let _botF=e.get(`bot`)||``,', TABS + 'let _botF=e.get(`bot`)||``,', 'search: tabs state + markup')
patch('M=d||f||p||m||q2||_botF;', 'M=d||f||p||m||q2||_botF||_srt;', 'search: filters count as active')
patch('children:[(0,L.jsx)(`span`,{children:`🤖 Bots`})]}),',
      'children:[(0,L.jsx)(`span`,{children:_botF===`hide`?`🙈 No bots`:`🤖 Bots`})]}),'
      '_srt===`flaps`&&(0,L.jsx)(`button`,{type:`button`,style:_chipS,onClick:ev=>{ev.stopPropagation(),_setParam(`sort`,``)},children:`🪽 Most flaps`}),',
      'search: chips')
# The clock button moves into the Filters tab
i = content.find('(0,L.jsx)(`button`,{type:`button`,onClick:()=>W(!P),')
j = content.find('children:`🕐`}),', i)
if i < 0 or j < 0 or j - i > 600:
    errors.append('FAIL (remove clock button)')
else:
    content = content[:i] + content[j + len('children:`🕐`}),'):]
    print('OK: remove clock button')
patch('S?(0,L.jsxs)(L.Fragment,{children:[(0,L.jsxs)(`div`,{className:`search-section-label`,style:{paddingLeft:32}',
      '!S&&!h?_TABS():S?(0,L.jsxs)(L.Fragment,{children:[(0,L.jsxs)(`div`,{className:`search-section-label`,style:{paddingLeft:32}',
      'search: tabs when not typing')

patch("if(!_ud||!_ud.querySelector(`.search-suggestion`))a(!1);",
      "if(!_ud||!_ud.querySelector(`.search-suggestion,.srch-opt`))a(!1);",
      'search: filters tab stays open when the keyboard closes')

# ── Styles ─────────────────────────────────────────────────────────────────────
patch('.search-divider { height: 1px; background: #374151; margin: 8px 0; }',
      '.search-divider { height: 1px; background: #374151; margin: 8px 0; }\n'
      '      .srch-tabs { display: flex; margin: 2px 40px 2px; height: 26px; border: 1px solid #a855f7; border-radius: 999px; overflow: hidden; }\n'
      '      .srch-tab { flex: 1; border: none; background: transparent; color: #c084fc; font-size: 12px; font-weight: 700; cursor: pointer; padding: 0; transition: background 0.15s, color 0.15s; }\n'
      '      .srch-tab.active { background: #c084fc; color: #fff; }\n'
      '      .srch-body { padding: 10px 14px 8px; }\n'
      '      .srch-filters { display: flex; flex-direction: column; gap: 6px; padding: 10px 14px 8px; }\n'
      '      .srch-row { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-bottom: 4px; }\n'
      '      .srch-opt { height: 26px; padding: 0 10px; border-radius: 999px; border: 1px solid #374151; background: #252833; color: #cbd5e1; font-size: 12px; font-weight: 700; cursor: pointer; white-space: nowrap; }\n'
      '      .srch-opt.active { background: #c084fc; border-color: #c084fc; color: #0a0a0a; }\n'
      '      .srch-time { height: 26px; border-radius: 999px; border: 1px solid #374151; background: #252833; color: #cbd5e1; font-size: 12px; font-weight: 700; padding: 0 10px; color-scheme: dark; box-sizing: border-box; -webkit-appearance: none; appearance: none; }\n'
      '      .srch-time.active { border-color: #c084fc; color: #c084fc; }',
      'styles')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
