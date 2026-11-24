import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, SITE, OUT, Q, SKIP_INTRO
import asyncio,sys,json,collections
from playwright.async_api import async_playwright
async def run(b,mode,station):
    c=await b.new_context(viewport={'width':1440,'height':900},color_scheme='dark')
    await c.add_init_script("try{sessionStorage.setItem('vh','1')}catch(e){}")
    pg=await c.new_page();await pg.goto(URL+'#'+station);await pg.wait_for_timeout(3000)
    if mode=='nosmil':await pg.evaluate('document.querySelectorAll("svg").forEach(s=>{try{s.pauseAnimations()}catch(e){}})')
    if mode=='nocss':await pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
    if mode=='nopath':await pg.evaluate('document.querySelectorAll("#path svg, #path *").forEach(e=>{e.getAnimations&&e.getAnimations().forEach(a=>a.pause())})')
    await b.start_tracing(page=pg,path=OUT+'/l.json',categories=['devtools.timeline','blink'])
    await pg.wait_for_timeout(2000)
    await b.stop_tracing();await c.close()
    d=json.load(open(OUT+'/l.json'));ev=d['traceEvents'] if isinstance(d,dict) else d
    L=[e for e in ev if e.get('name')=='Layout' and e.get('ph')=='X'];S=[e for e in ev if e.get('name')=='UpdateLayoutTree']
    A=sum(e.get('dur',0) for e in ev if e.get('name')=='Blink.Animate.UpdateTime')/1000
    print(station,mode,'layouts',len(L),'style',len(S),'animate ms',round(A))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for st in sys.argv[1:]:
            for m in ['asis','nosmil','nocss']:await run(b,m,st)
        await b.close()
asyncio.run(main())
