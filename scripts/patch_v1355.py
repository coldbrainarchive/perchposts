#!/usr/bin/env python3
"""Patch v1354 -> v1355: chat screen redesign for posts (huddles unchanged).
- Header: the post's thumbnail + title + a second line (site or bird · N chirps) with a ▾. Tapping it drops down a
  panel with the tags, photo, summary and Open post / Share (it no longer leaves the chat).
- Oldest / Newest stays where it was, with a filter button beside it: All chirps, Top, Most replied, Media, Flaps —
  the post page's chirp filters, applied to the whole chat (a "Showing: Top · Show all" strip while one is on).
- Worker sends up to 20 top / most-replied chirps (was 6 / 9) so the filters have more to show."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1354.js'
dst = '_deploy/assets/index-DUcNPOLc-v1355.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

# state
patch("[_cpm,_setCpm]=(0,_.useState)(`hl`),", "[_cpm,_setCpm]=(0,_.useState)(`hl`),[_cff,_setCff]=(0,_.useState)(`all`),[_chx,_setChx]=(0,_.useState)(!1),", 'state')

# header: posts get the new left block (huddles keep the info icon + title that go back to the huddle info)
patch("(0,L.jsxs)(`div`,{className:_cf?`cf-bar`:void 0,role:_cf?`button`:void 0,tabIndex:_cf?0:void 0,\"aria-label\":_cf?(c.is_huddle?`Huddle info`:`Post info`):void 0,onClick:_cf?_closeC:void 0,style:{display:`flex`,alignItems:`center`,gap:8},children:[_cf&&(",
      "(0,L.jsxs)(`div`,{className:_cf?`cf-bar`+(c.is_huddle?``:` ch-bar`):void 0,role:_cf?`button`:void 0,tabIndex:_cf?0:void 0,\"aria-label\":_cf?(c.is_huddle?`Huddle info`:`Post details`):void 0,\"aria-expanded\":_cf&&!c.is_huddle?_chx:void 0,onClick:_cf?(c.is_huddle?_closeC:()=>_setChx(v=>!v)):void 0,style:{display:`flex`,alignItems:`center`,gap:8,minWidth:0},children:[_cf&&!c.is_huddle&&(0,L.jsx)(_ChThumb,{post:c},`cht`),_cf&&c.is_huddle&&(", 'header left')
patch("_cf?(0,L.jsx)(`span`,{className:`comments-panel-title cf-title`,children:_ct}):",
      "_cf&&!c.is_huddle?(0,L.jsx)(_ChHeadTx,{post:c,title:_ct,n:_cn,open:_chx},`chtx`):_cf?(0,L.jsx)(`span`,{className:`comments-panel-title cf-title`,children:_ct}):", 'header title')
# right side: filter button before the Oldest/Newest toggle
patch("(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:6},children:[(0,L.jsxs)(`div`,{className:`sort-toggle`,children:[(0,L.jsx)(`button`,{type:`button`,className:b?`sort-toggle-btn`:`sort-toggle-btn active`",
      "(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:6,flexShrink:0},children:[_cf&&!c.is_huddle&&(0,L.jsx)(_ChFilter,{v:_cff,set:_setCff},`chf`),(0,L.jsxs)(`div`,{className:`sort-toggle`,children:[(0,L.jsx)(`button`,{type:`button`,className:b?`sort-toggle-btn`:`sort-toggle-btn active`", 'filter button')
# drop-down panel + "showing" strip, right under the header
patch("(0,L.jsx)(`div`,{className:`chat-window`,ref:D,",
      "_cf&&!c.is_huddle&&_chx&&(0,L.jsx)(_ChPanel,{post:c,close:()=>_setChx(!1),openPost:()=>{_setChx(!1);_closeC()}},`chp`),_cf&&!c.is_huddle&&_cff!==`all`&&(0,L.jsxs)(`div`,{className:`chf-strip`,children:[`Showing: `,(0,L.jsx)(`b`,{children:_CHF[_cff]}),(0,L.jsx)(`button`,{type:`button`,onClick:()=>_setCff(`all`),children:`Show all`})]},`chfs`),(0,L.jsx)(`div`,{className:`chat-window`,ref:D,", 'panel + strip')
# filtering the chat list
patch("_nl=_ls.length;_np=_ps.length;_rev=[..._ls,..._ps]}const _R=",
      "_nl=_ls.length;_np=_ps.length;_rev=[..._ls,..._ps]}let _flt=!1;if(_cf&&!c?.is_huddle&&_cff!==`all`){_flt=!0;const _src=_cff===`top`?(_cpTop[r]||[]):_cff===`rep`?(_cpRep[r]||[]):_cff===`media`?_rev.filter(_x=>/\\[ATTACH/.test(_x.content||``)):[];_rev=_cff===`top`||_cff===`rep`?[..._src].reverse():_src}const _R=", 'filter list')
patch("let _pins=[],_solo=new Set();if(!_pv){", "let _pins=[],_solo=new Set();if(!_pv&&!_flt){", 'no pins while filtered')
patch("_pv&&_cpm===`react`?(!c?.is_huddle&&_out.push((0,L.jsx)(_PostReactions,{id:r,bot:_ppIsBot(c)},`prx`))):",
      "_flt?(_cff===`react`?_out.push((0,L.jsx)(_PostReactions,{id:r,bot:_ppIsBot(c)},`fprx`)):!_rev.length&&_out.push((0,L.jsx)(`div`,{className:`cp-empty`,children:_CPE[_cff]||`Nothing here yet`},`fcpe`))):_pv&&_cpm===`react`?(!c?.is_huddle&&_out.push((0,L.jsx)(_PostReactions,{id:r,bot:_ppIsBot(c)},`prx`))):", 'filtered empty / flaps')

patch("body .lb-ic{",
 "body .ch-bar{flex:1;min-width:0;margin-right:6px}"
 "body .ch-th{width:38px;height:38px;border-radius:10px;flex-shrink:0;object-fit:cover;background:#22252e;display:flex;align-items:center;justify-content:center;color:#c084fc;overflow:hidden}"
 "body .ch-th img{width:100%;height:100%;object-fit:cover}"
 "body .ch-tx{min-width:0;display:flex;flex-direction:column;gap:2px}"
 "body .ch-t{font-size:15px;font-weight:800;color:#f1f5f9;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}"
 "body .ch-m{display:flex;align-items:center;gap:6px;font-size:11.5px;font-weight:700;color:#94a3b8;white-space:nowrap;overflow:hidden}"
 "body .ch-m .s{color:#c084fc;letter-spacing:.06em;text-transform:uppercase;font-weight:800;overflow:hidden;text-overflow:ellipsis}"
 "body .ch-m .cv{color:#c084fc;transition:transform .2s;display:inline-block}body .ch-m .cv.up{transform:rotate(180deg)}"
 "body .chf-b{width:34px;height:34px;border-radius:999px;border:1px solid #c084fc;background:transparent;color:#c084fc;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;padding:0;position:relative}"
 "body .chf-b.on{background:#c084fc;color:#fff}body .chf-b svg{width:17px;height:17px}"
 "body .chf-menu{position:fixed;z-index:9000;min-width:210px;background:#1b1d25;border:1px solid #323543;border-radius:14px;box-shadow:0 14px 40px #000c;padding:6px}"
 "body .chf-menu .h{font-size:10.5px;font-weight:900;letter-spacing:.08em;color:#64748b;padding:6px 10px 4px}"
 "body .chf-menu button{display:flex;align-items:center;gap:10px;width:100%;padding:10px;border:0;border-radius:10px;background:none;color:#e2e8f0;font:inherit;font-size:14px;font-weight:700;cursor:pointer;text-align:left}"
 "body .chf-menu button.on{background:#c084fc22}body .chf-menu button .ck{margin-left:auto;color:#c084fc;font-weight:900}"
 "body .chf-menu button .ic{width:20px;display:inline-flex;justify-content:center;color:#c084fc}body .chf-menu button .ic svg{width:16px;height:16px}"
 "body .chf-strip{display:flex;align-items:center;gap:6px;padding:7px 14px;font-size:12px;font-weight:700;color:#94a3b8;border-bottom:1px solid #22252e;background:#15171d}"
 "body .chf-strip b{color:#c084fc}body .chf-strip button{margin-left:auto;border:0;background:none;color:#c084fc;font:inherit;font-weight:800;cursor:pointer;padding:2px 0}"
 "body .chp{border-bottom:1px solid #22252e;background:#15171d;padding:12px 14px 14px;display:flex;flex-direction:column;gap:10px;max-height:62vh;overflow-y:auto;animation:chpIn .2s ease-out}"
 "@keyframes chpIn{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}"
 "body .chp .tg{display:flex;flex-wrap:wrap;gap:6px}"
 "body .chp .im{width:100%;max-height:220px;object-fit:cover;border-radius:12px;background:#22252e}"
 "body .chp .ttl{font-size:17px;font-weight:800;line-height:1.3;color:#f1f5f9}"
 "body .chp .ds{font-size:13.5px;line-height:1.45;color:#b6c2d1;display:-webkit-box;-webkit-line-clamp:5;-webkit-box-orient:vertical;overflow:hidden}"
 "body .chp .row{display:flex;gap:8px}"
 "body .chp .row button{flex:1;height:38px;border-radius:999px;border:1px solid #2e303a;background:#1d2029;color:#e2e8f0;font:inherit;font-size:12.5px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;cursor:pointer}"
 "body .chp .row button.pri{background:#c084fc;border-color:#c084fc;color:#14081d}"
 "body .lb-ic{", 'css')

c += r"""
const _CHF={all:`All chirps`,top:`Top`,rep:`Most replied`,media:`Media`,react:`Flaps`};
function _chImg(post){try{const m=Mr(post.content||``),a=m.attachment,as=m.attachments;if(a&&(a.image||a.poster))return a.image||a.poster;if(a&&a.type===`image`)return _mtThumbOf(a);if(Array.isArray(as)&&as[0]){const f=as[0];return typeof f===`string`?f:(f.poster||f.thumb||f.url||null)}}catch(e){}return null}
function _chSite(post){try{const a=Mr(post.content||``).attachment;if(a&&a.url)return new URL(a.url).hostname.replace(/^www\./,``)}catch(e){}return null}
function _ChThumb({post}){const im=_chImg(post);return(0,L.jsx)(`span`,{className:`ch-th`,children:im?(0,L.jsx)(`img`,{src:im,alt:``,referrerPolicy:`no-referrer`,onError:e=>{e.currentTarget.remove()}}):(0,L.jsx)(`span`,{className:`pp-ic`,dangerouslySetInnerHTML:{__html:_ppIco(`CHAT`)}})})}
function _ChHeadTx({post,title,n,open}){const bot=_ppIsBot(post),site=_chSite(post);
 return(0,L.jsxs)(`span`,{className:`ch-tx`,children:[(0,L.jsx)(`span`,{className:`ch-t`,children:title}),(0,L.jsxs)(`span`,{className:`ch-m`,children:[site&&bot?(0,L.jsx)(`span`,{className:`s`,children:site}):post.username?(0,L.jsx)(`span`,{style:{color:Hn(post.browser_id,post.username),fontWeight:800},children:post.username}):null,(0,L.jsx)(`span`,{children:`· ${n} chirp${n===1?``:`s`}`}),(0,L.jsx)(`span`,{className:`cv`+(open?` up`:``),children:`▾`})]})]})}
function _ChFilter({v,set}){const ref=(0,_.useRef)(null);
 const SV=d=>`<svg class="ri" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">${d}</svg>`;
 const IC={all:_ppIco(`CHAT`),top:_ppIco(`UP`),rep:SV(`<path d="M9 14 4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 6 6v4"/>`),media:SV(`<rect x="3.5" y="4.5" width="17" height="15" rx="2.5"/><circle cx="9" cy="10" r="1.6"/><path d="m20.5 16-5-5-8.5 8.5"/>`),react:_ppIco(`BIRD`)};
 const open=ev=>{ev.stopPropagation();const ex=document.querySelector(`.chf-menu`);if(ex){ex.remove();return}
  const m=document.createElement(`div`);m.className=`chf-menu`;m.innerHTML=`<div class="h">SHOW IN CHAT</div>`;
  Object.entries(_CHF).forEach(([k,l])=>{const b=document.createElement(`button`);b.type=`button`;if(k===v)b.className=`on`;b.innerHTML=`<span class="ic">${IC[k]}</span>${l}${k===v?`<span class="ck">✓</span>`:``}`;b.onclick=e=>{e.stopPropagation();m.remove();set(k)};m.appendChild(b)});
  document.body.appendChild(m);const r=ref.current.getBoundingClientRect();m.style.top=(r.bottom+6)+`px`;m.style.right=Math.max(8,innerWidth-r.right)+`px`;
  const off=e=>{if(!m.contains(e.target)){m.remove();document.removeEventListener(`pointerdown`,off,!0)}};setTimeout(()=>document.addEventListener(`pointerdown`,off,!0),0)};
 return(0,L.jsx)(`button`,{ref,type:`button`,className:`chf-b`+(v!==`all`?` on`:``),"aria-label":`Filter chirps: ${_CHF[v]}`,onClick:open,dangerouslySetInnerHTML:{__html:`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M7 12h10M10 18h4"/></svg>`}})}
function _ChPanel({post,close,openPost}){const m=Mr(post.content||``),a=m.attachment,im=_chImg(post),bn=cr(post),bot=_ppIsBot(post);
 // birds' posts: their own words first (the link's blurb if they wrote nothing); news: the article summary
 const desc=String(bot?((a&&a.description)||m.text||``):(m.text||(a&&a.description)||``)).trim(),ttl=post.title||(a&&a.title)||``;
 return(0,L.jsxs)(`div`,{className:`chp`,onClick:e=>e.stopPropagation(),children:[
  (0,L.jsxs)(`div`,{className:`tg`,children:[bn&&!post.board_auto?(0,L.jsx)(Ar,{boardName:bn,small:!0},`b`):null,(post.country||post.continent)?(0,L.jsx)(kr,{country:post.country,continent:post.continent,small:!0},`c`):null,post.utag?(0,L.jsx)(_UTag,{tag:post.utag,small:!0},`u`):null]}),
  im?(0,L.jsx)(`img`,{className:`im`,src:im,alt:``,referrerPolicy:`no-referrer`,onError:e=>{e.currentTarget.remove()}}):null,
  ttl&&bot?(0,L.jsx)(`div`,{className:`ttl`,children:ttl}):null,
  desc?(0,L.jsx)(`div`,{className:`ds`,children:desc}):null,
  (0,L.jsxs)(`div`,{className:`row`,children:[(0,L.jsx)(`button`,{type:`button`,className:`pri`,onClick:openPost,children:`Open post`}),(0,L.jsx)(`button`,{type:`button`,onClick:()=>{if(!(window._ppShare&&window._ppShare(post.id))){try{navigator.share?navigator.share({url:location.origin+`/post/`+post.id}):navigator.clipboard.writeText(location.origin+`/post/`+post.id)}catch(e){}}},children:`Share`})]})]})}
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
