import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, SITE, OUT, Q, SKIP_INTRO
import asyncio,sys,json
from playwright.async_api import async_playwright
URL=URL+''
async def main(w,h,thr):
    async with async_playwright() as p:
        b=await p.chromium.launch(); c=await b.new_context(viewport={'width':w,'height':h},color_scheme='dark')
        await c.add_init_script("try{sessionStorage.setItem('vh','1')}catch(e){};window.__lt=[];new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lt.push([Math.round(e.startTime),Math.round(e.duration)])}).observe({type:'longtask',buffered:true})")
        pg=await c.new_page(); cdp=await c.new_cdp_session(pg)
        await cdp.send('Emulation.setCPUThrottlingRate',{'rate':thr})
        await pg.goto(URL); await pg.wait_for_timeout(9000)
        lt=await pg.evaluate('window.__lt');print('load',lt)
        for k in range(14):
            await pg.evaluate('window.__lt=[]')
            await pg.click('#next'); await pg.wait_for_timeout(2500)
            a=await pg.evaluate('window.__lt')
            await pg.evaluate('window.__lt=[]')
            for s in range(6):
                await pg.mouse.move(w//2,h//2); await pg.mouse.wheel(0,300); await pg.wait_for_timeout(250)
            sc=await pg.evaluate('window.__lt')
            await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(1500)
            print(await pg.evaluate('location.hash'),'switch',a,'scroll',sc)
        await b.close()
asyncio.run(main(int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3])))
