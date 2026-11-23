#!/usr/bin/env python3
"""Patch v1313 -> v1314: user tags (#biking).
- New Post: "+ tag" chip next to "+ country" -> one-word input with suggestions (/tags?q=); sent as user_tag.
- Grey pill with a # line icon (_UTag) on feed cards, the post page and (automatically) the post scroller; tapping
  opens /?utag=<tag> (the tag feed, via get-posts?utag=).
- Post page: the author can add / change / remove the tag (pencil), mods can remove (x), admins can set or remove.
- Search: chip for the active tag (tap clears), "Popular tags" in the Tags tab, matching tags while typing."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1313.js'
dst = '_deploy/assets/index-DUcNPOLc-v1314.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
HASH = '<svg class=\\"ri\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" aria-hidden=\\"true\\"><path d=\\"M5 9h15M4 15h15M10 3.5 8 20.5M16 3.5l-2 17\\"/></svg>'
patch('function _ppIco(k){return ({"AT":', 'function _ppIco(k){return ({"HASH": "' + HASH + '", "AT":', 'hash icon')
# composer: picker after "+ country", and send it
patch("children:`+ country`})]}),b&&(0,L.jsxs)(`div`,{style:{position:`absolute`",
      "children:`+ country`}),!p&&(0,L.jsx)(_UTagPick,{},`utp`)]}),b&&(0,L.jsxs)(`div`,{style:{position:`absolute`", 'composer picker')
patch("country:_isHuddle?null:(v||null),browser_id:f,is_huddle:_isHuddle,",
      "country:_isHuddle?null:(v||null),user_tag:_isHuddle?null:(window._ppNewTag||null),browser_id:f,is_huddle:_isHuddle,", 'send user_tag')
# feed card pill
patch("children:(0,L.jsx)(kr,{country:e.country,continent:e.continent,small:!0})}),]})",
      "children:(0,L.jsx)(kr,{country:e.country,continent:e.continent,small:!0})}),e.utag&&(0,L.jsx)(`span`,{style:{cursor:`pointer`,display:`inline-flex`,alignItems:`center`},onClick:t=>{t.preventDefault();t.stopPropagation();_ppGoTag(e.utag)},children:(0,L.jsx)(_UTag,{tag:e.utag,small:!0})}),]})", 'card pill')
# post page pill + edit
patch("children:(0,L.jsx)(kr,{country:c.country,continent:c.continent,small:!0})})]})}),!c.is_huddle&&(c.pinned||c.locked||c.frozen)",
      "children:(0,L.jsx)(kr,{country:c.country,continent:c.continent,small:!0})}),!c.is_huddle&&(0,L.jsx)(_UTagEdit,{post:c},`ute-`+c.id)]})}),!c.is_huddle&&(c.pinned||c.locked||c.frozen)", 'post page')
# home feed: ?utag= uses the filtered-list path
patch("qT=l.get(`time`)||``,_bot=l.get(`bot`)||``", "qT=l.get(`time`)||``,_bot=l.get(`bot`)||``,_ut=(l.get(`utag`)||``).toLowerCase()", 'home: read utag')
patch("if(!u&&!d&&!p&&(!f||_cs)){setTagR(null);_setTgL(!1);return}", "if(!u&&!d&&!p&&!_ut&&(!f||_cs)){setTagR(null);_setTgL(!1);return}", 'home: fetch when utag')
patch("if(f)turl+=`&country=${encodeURIComponent(f)}`;if(p)turl+=", "if(f)turl+=`&country=${encodeURIComponent(f)}`;if(_ut)turl=`${R}/get-posts?utag=${encodeURIComponent(_ut)}&limit=100`;if(p)turl+=", 'home: tag url')
patch("},[u,d,f,p,_cs,l.get(`flaps`)]),", "},[u,d,f,p,_cs,_ut,l.get(`flaps`)]),", 'home: deps')
patch(":(u||d||f||p||_bot)&&TagR!==null?TagR:e,", ":(u||d||f||p||_bot||_ut)&&TagR!==null?TagR:e,", 'home: use the list')
patch("_canMore=!(u===`feedback`||u===`huddles`)&&!m&&!qT&&_cur!=null", "_canMore=!(u===`feedback`||u===`huddles`)&&!m&&!qT&&!_ut&&_cur!=null", 'home: no load-older for tags')
# search bar: chip, popular, suggestions
patch("let _botF=e.get(`bot`)||``,_clearBot=()=>{let n=new URLSearchParams(e);n.delete(`bot`);t(n)};let j=nr.find(e=>e.slug===d),M=d||f||p||m||q2||_botF||_srt;",
      "let _botF=e.get(`bot`)||``,_clearBot=()=>{let n=new URLSearchParams(e);n.delete(`bot`);t(n)},_utF=(e.get(`utag`)||``).toLowerCase(),_clearUt=()=>{let n=new URLSearchParams(e);n.delete(`utag`);t(n)},_pickUt=tg=>{let n=new URLSearchParams(e);n.set(`utag`,tg);n.delete(`q`);t(n);a(!1);r(``);if(c.current)c.current.value=``};let j=nr.find(e=>e.slug===d),M=d||f||p||m||q2||_botF||_srt||_utF;", 'search: state')
patch("dangerouslySetInnerHTML:{__html:_ppIco(`SEARCH`)}}),j&&(0,L.jsxs)(`button`",
      "dangerouslySetInnerHTML:{__html:_ppIco(`SEARCH`)}}),_utF&&(0,L.jsx)(`button`,{type:`button`,className:`search-chip`,onClick:ev=>{ev.stopPropagation(),_clearUt()},style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},children:(0,L.jsx)(_UTag,{tag:_utF,small:!0})}),j&&(0,L.jsxs)(`button`", 'search: chip')
patch("children:[...g.filter(x=>!_SPACES.includes(x.slug)).map(x=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>ee(x.slug),children:(0,L.jsx)(Ar,{boardName:x.name,small:!0})},x.slug))]})",
      "children:[...g.filter(x=>!_SPACES.includes(x.slug)).map(x=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>ee(x.slug),children:(0,L.jsx)(Ar,{boardName:x.name,small:!0})},x.slug)),(0,L.jsx)(_UTagPopular,{pick:_pickUt},`utpop`)]})", 'search: popular')
patch("UR.length>0&&(0,L.jsxs)(L.Fragment,{children:[(C||w||T)", "(0,L.jsx)(_UTagSuggest,{q:n,pick:_pickUt},`utsug`),UR.length>0&&(0,L.jsxs)(L.Fragment,{children:[(C||w||T)", 'search: suggestions')
CSS = ("body .utag-edit{display:inline-flex;align-items:center;gap:4px;position:relative}"
 "body .utag-ic{display:inline-flex}body .utag-ic .ri{width:11px;height:11px;stroke-width:2.6}body .pp-tag.utag-l .utag-ic .ri{width:12px;height:12px}"
 "body .utag-add{display:inline-flex;align-items:center;gap:3px;padding:2px 8px;border-radius:999px;border:1px dashed #3f4756;background:none;color:#64748b;font:inherit;font-size:11px;font-weight:700;cursor:pointer}"
 "body .utag-mini{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:999px;border:1px solid #2e303a;background:#1b1d24;color:#94a3b8;cursor:pointer;padding:0}body .utag-mini .ri{width:12px;height:12px}"
 "body .utag-in{display:inline-flex;align-items:center;gap:3px;height:22px;padding:0 8px;border-radius:999px;background:#cbd5e1;color:#0a0a0a;position:relative}"
 "body .utag-in input{border:0;background:none;outline:none;font:inherit;font-size:16px;font-weight:800;text-transform:uppercase;letter-spacing:.03em;width:110px;color:#0a0a0a;padding:0;transform:scale(.68);transform-origin:left center;margin-right:-36px}"
 "body .utag-sug{position:absolute;top:calc(100% + 6px);left:0;z-index:300;background:#1e2028;border:1px solid #374151;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,.5);padding:6px;display:flex;flex-direction:column;gap:4px;min-width:180px}"
 "body .utag-sug button{display:flex;align-items:center;justify-content:space-between;gap:10px;background:none;border:0;padding:4px 6px;border-radius:8px;cursor:pointer;color:#94a3b8;font:inherit;font-size:11px}body .utag-sug button:hover,body .utag-sug button.on{background:#2a2340}"
 "body .utag-err{position:absolute;top:calc(100% + 6px);left:0;z-index:300;white-space:nowrap;font-size:11.5px;font-weight:700;color:#fca5a5;background:#1e2028;border:1px solid #7f1d1d;border-radius:8px;padding:5px 8px}"
 "body .utag-pop{flex-basis:100%;width:100%}body .utag-pop .tg-row{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;padding:4px 6px 2px}")
patch("body .lb-ic{", CSS + "body .lb-ic{", 'css')
c += r"""
function _ppGoTag(tag){try{const u=`/?utag=${encodeURIComponent(tag)}`;history.pushState({},``,u);dispatchEvent(new PopStateEvent(`popstate`,{state:{}}))}catch(e){location.href=`/?utag=${encodeURIComponent(tag)}`}}
function _UTag({tag,small}){if(!tag)return null;return(0,L.jsxs)(`span`,{className:`pp-tag utag-l`,title:`#`+tag,style:{"--pc":`#cbd5e1`,display:`inline-flex`,alignItems:`center`,gap:small?4:6,height:small?22:26,padding:small?`0 7px`:`0 8px`,borderRadius:999,border:`1px solid rgba(0,0,0,0.15)`,background:`#cbd5e1`,color:`#0a0a0a`,fontSize:small?10:11,fontWeight:800,letterSpacing:`0.03em`,textTransform:`uppercase`,whiteSpace:`nowrap`,lineHeight:1,flexShrink:0,boxSizing:`border-box`},children:[(0,L.jsx)(`span`,{className:`utag-ic`,"aria-hidden":!0,dangerouslySetInnerHTML:{__html:_ppIco(`HASH`)}}),(0,L.jsx)(`span`,{children:tag})]})}
const _utOk=t=>/^[a-z0-9]{2,20}$/.test(t);
function _UTagInput({initial,done,busy,err}){const[v,setV]=(0,_.useState)(initial||``),[sug,setSug]=(0,_.useState)([]),[on,setOn]=(0,_.useState)(-1),ref=(0,_.useRef)(null),t=(0,_.useRef)(0);
 (0,_.useEffect)(()=>{ref.current&&ref.current.focus()},[]);
 (0,_.useEffect)(()=>{clearTimeout(t.current);const q=v.toLowerCase();if(!q){setSug([]);return}t.current=setTimeout(()=>{fetch(`${R}/tags?q=${encodeURIComponent(q)}`).then(r=>r.ok?r.json():{tags:[]}).then(d=>{setSug((d.tags||[]).filter(x=>x.tag!==q).slice(0,6));setOn(-1)}).catch(()=>{})},160);return()=>clearTimeout(t.current)},[v]);
 const clean=s=>s.replace(/^#+/,``).replace(/[^A-Za-z0-9]/g,``).slice(0,20).toLowerCase();
 const bad=v&&!_utOk(v)?`2–20 letters or numbers, one word`:``;
 const go=tag=>{if(busy)return;if(!tag){done(void 0);return}if(!_utOk(tag))return;done(tag)};
 return(0,L.jsxs)(`span`,{className:`utag-edit`,children:[(0,L.jsxs)(`span`,{className:`utag-in`,children:[(0,L.jsx)(`span`,{className:`utag-ic`,"aria-hidden":!0,dangerouslySetInnerHTML:{__html:_ppIco(`HASH`)}}),
   (0,L.jsx)(`input`,{ref,type:`search`,name:`search_np_utag`,autoComplete:`off`,autoCorrect:`off`,autoCapitalize:`off`,spellCheck:!1,enterKeyHint:`done`,placeholder:`tag`,value:v,maxLength:24,"aria-label":`Your tag (one word)`,
    onChange:e=>setV(clean(e.target.value)),
    onKeyDown:e=>{if(e.key===`ArrowDown`&&sug.length){e.preventDefault();setOn(o=>(o+1)%sug.length)}else if(e.key===`ArrowUp`&&sug.length){e.preventDefault();setOn(o=>(o-1+sug.length)%sug.length)}else if(e.key===`Enter`){e.preventDefault();go(on>=0&&sug[on]?sug[on].tag:v)}else if(e.key===`Escape`){e.preventDefault();done(null)}},
    onBlur:()=>setTimeout(()=>{if(document.activeElement!==ref.current)go(v)},180)})]}),
  err?(0,L.jsx)(`span`,{className:`utag-err`,role:`alert`,children:err}):bad&&v.length>1?(0,L.jsx)(`span`,{className:`utag-err`,children:bad}):sug.length?(0,L.jsx)(`span`,{className:`utag-sug`,onMouseDown:e=>e.preventDefault(),children:sug.map((x,k)=>(0,L.jsxs)(`button`,{type:`button`,className:k===on?`on`:``,onClick:()=>go(x.tag),children:[(0,L.jsx)(_UTag,{tag:x.tag,small:!0}),`${x.n} post${x.n===1?``:`s`}`]},x.tag))}):null]})}
function _UTagPick(){const[tag,setTag]=(0,_.useState)(``),[ed,setEd]=(0,_.useState)(!1);(0,_.useEffect)(()=>{window._ppNewTag=null;return()=>{window._ppNewTag=null}},[]);
 if(ed)return(0,L.jsx)(_UTagInput,{initial:tag,done:t=>{setEd(!1);if(t===void 0){setTag(``);window._ppNewTag=null}else if(t){setTag(t);window._ppNewTag=t}}});
 if(tag)return(0,L.jsx)(`button`,{type:`button`,onClick:()=>setEd(!0),style:{background:`none`,border:`none`,padding:0,cursor:`pointer`},"aria-label":`Change tag`,children:(0,L.jsx)(_UTag,{tag,small:!0})});
 return(0,L.jsx)(`button`,{type:`button`,className:`utag-add`,onClick:()=>setEd(!0),children:`+ tag`})}
function _UTagEdit({post}){const[tag,setTag]=(0,_.useState)(post.utag||``),[ed,setEd]=(0,_.useState)(!1),[busy,setBusy]=(0,_.useState)(!1),[err,setErr]=(0,_.useState)(``);
 const me=(localStorage.getItem(`_myUsername`)||``).toLowerCase(),role=localStorage.getItem(`user_role`)||``,mine=!!me&&(post.username||``).toLowerCase()===me,adm=role===`admin`,mod=role===`mod`||adm;
 const bot=String(post.browser_id||``).startsWith(`bot-`)||/Bot$/.test(post.username||``),cage=/cage/i.test(String(post.community_id||post.board||``));
 const canSet=!bot&&!cage&&(mine||adm),canRm=!!tag&&(mine||mod);
 const save=async t=>{setBusy(!0);setErr(``);try{const r=await fetch(`${R}/post-tag`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({post_id:post.id,tag:t||``})});const j=await r.json().catch(()=>({}));if(r.ok){setTag(j.utag||``);setEd(!1)}else setErr(j.error||`Couldn't save the tag`)}catch(e){setErr(`Couldn't save the tag`)}setBusy(!1)};
 if(ed)return(0,L.jsx)(_UTagInput,{initial:tag,busy,err,done:t=>{if(t===null||t===tag){setEd(!1);setErr(``);return}if(t===void 0){if(tag)save(``);else setEd(!1);return}save(t)}});
 const pill=tag?(0,L.jsx)(`button`,{type:`button`,onClick:()=>_ppGoTag(tag),style:{background:`none`,border:`none`,padding:0,cursor:`pointer`,display:`inline-flex`},children:(0,L.jsx)(_UTag,{tag,small:!0})}):null;
 const pen=`<svg class="ri" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4L19 9a2.8 2.8 0 0 0-4-4L4 16z"/></svg>`,x=`<svg class="ri" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg>`;
 return(0,L.jsxs)(`span`,{className:`utag-edit`,children:[pill,
  !tag&&canSet?(0,L.jsx)(`button`,{type:`button`,className:`utag-add`,onClick:()=>setEd(!0),children:`+ tag`}):null,
  tag&&canSet?(0,L.jsx)(`button`,{type:`button`,className:`utag-mini`,"aria-label":`Change the tag`,onClick:()=>setEd(!0),dangerouslySetInnerHTML:{__html:pen}}):null,
  tag&&canRm&&!canSet?(0,L.jsx)(`button`,{type:`button`,className:`utag-mini`,"aria-label":`Remove the tag`,onClick:()=>{confirm(`Remove #${tag} from this post?`)&&save(``)},dangerouslySetInnerHTML:{__html:x}}):null,
  err&&!ed?(0,L.jsx)(`span`,{className:`utag-err`,children:err}):null]})}
function _UTagPopular({pick}){const[tags,setTags]=(0,_.useState)(null);(0,_.useEffect)(()=>{fetch(`${R}/tags?popular=1`).then(r=>r.ok?r.json():{tags:[]}).then(d=>setTags(d.tags||[])).catch(()=>setTags([]))},[]);
 if(!tags||!tags.length)return null;return(0,L.jsxs)(`div`,{className:`utag-pop`,children:[(0,L.jsx)(`div`,{className:`search-section-label tg-lb`,children:`Popular tags this week`}),(0,L.jsx)(`div`,{className:`tg-row`,children:tags.map(x=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>pick(x.tag),children:(0,L.jsx)(_UTag,{tag:x.tag,small:!0})},x.tag))})]})}
function _UTagSuggest({q,pick}){const[tags,setTags]=(0,_.useState)([]);const k=String(q||``).trim().replace(/^#+/,``).toLowerCase();
 (0,_.useEffect)(()=>{if(!/^[a-z0-9]{1,20}$/.test(k)){setTags([]);return}let dead=!1;const tm=setTimeout(()=>{fetch(`${R}/tags?q=${encodeURIComponent(k)}`).then(r=>r.ok?r.json():{tags:[]}).then(d=>{dead||setTags(d.tags||[])}).catch(()=>{})},150);return()=>{dead=!0;clearTimeout(tm)}},[k]);
 if(!tags.length)return null;return(0,L.jsxs)(L.Fragment,{children:[(0,L.jsx)(`div`,{className:`search-divider`}),(0,L.jsx)(`div`,{className:`search-section-label`,children:`Tags`}),(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:8,padding:`4px 14px 6px`},children:tags.map(x=>(0,L.jsx)(`button`,{className:`search-suggestion`,type:`button`,onClick:()=>pick(x.tag),children:(0,L.jsx)(_UTag,{tag:x.tag,small:!0})},x.tag))})]})}
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
