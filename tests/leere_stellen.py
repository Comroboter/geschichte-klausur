import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, SITE, OUT, Q, SKIP_INTRO
import asyncio,sys
from playwright.async_api import async_playwright
IDS=["start","plan","revolution","gesellschaft","industrie","sortieren","kolonien","kongo","personen","aufgaben","quiz","kurz-vorher"]
JS="""()=>{const st=document.querySelector('.station.on'),c=st.querySelector(':scope > .content');const kids=[...c.children].filter(e=>!e.matches('.runway,.schwelle')&&e.getClientRects().length);
const cb=c.getBoundingClientRect();const out=[];
const rects=kids.map(e=>({e,r:e.getBoundingClientRect()}));
const bottomAll=Math.max(...rects.map(x=>x.r.bottom));
for(const a of rects){ // look for space below a, within its x-range, until next element overlapping horizontally
  const below=rects.filter(b=>b!==a&&b.r.top>=a.r.bottom-2&&b.r.left<a.r.right-10&&b.r.right>a.r.left+10);
  const nextTop=below.length?Math.min(...below.map(b=>b.r.top)):bottomAll;
  const gap=nextTop-a.r.bottom;
  // only if some other element is beside within this gap (i.e., not full-width blank)
  const beside=rects.filter(b=>b!==a&&(b.r.right<=a.r.left+10||b.r.left>=a.r.right-10)&&b.r.bottom>a.r.bottom+40&&b.r.top<nextTop);
  if(gap>110&&beside.length) out.push([(a.e.className||a.e.tagName).toString().slice(0,30),Math.round(a.r.width),Math.round(gap)]);
}
// also items inside common two-col containers
document.querySelectorAll('.station.on > .content .split, .station.on > .content .vmode, .station.on > .content .stage').forEach(g=>{const ch=[...g.children].filter(e=>e.getClientRects().length);if(ch.length<2)return;const hs=ch.map(e=>e.getBoundingClientRect());const mx=Math.max(...hs.map(r=>r.bottom));hs.forEach((r,i)=>{if(mx-r.bottom>110&&r.width<g.getBoundingClientRect().width*.8)out.push(['in '+g.className.split(' ')[0]+'>'+(ch[i].className||ch[i].tagName).toString().slice(0,20),Math.round(r.width),Math.round(mx-r.bottom)])})});
return out}"""
async def main(w,h):
    async with async_playwright() as p:
        b=await p.chromium.launch(); c=await b.new_context(viewport={'width':w,'height':h},color_scheme='dark')
        await c.add_init_script("try{sessionStorage.setItem('vh','1')}catch(e){}")
        pg=await c.new_page()
        for sid in IDS:
            await pg.goto(URL+'#'+sid); await pg.wait_for_timeout(900)
            r=await pg.evaluate(JS)
            if r: print(sid,r)
        await b.close()
asyncio.run(main(int(sys.argv[1]),int(sys.argv[2])))
