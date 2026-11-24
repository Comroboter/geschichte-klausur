import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, SITE, OUT, Q, SKIP_INTRO
import asyncio,sys
from playwright.async_api import async_playwright
LOG="""window.__log=[];(function f(){var t=performance.now();var ks=[...document.querySelectorAll('.station.on .rw-sheet .kicker,.peek.on .peek-in .kicker,.station.on .hero > .kicker')].filter(k=>{var r=k.getBoundingClientRect();return r.height>0&&r.top<innerHeight&&r.bottom>0});
 var vis=ks.map(k=>[k.closest('.rw-in')?'rw':k.closest('.peek-in')?'ov':'real',Math.round(k.getBoundingClientRect().top*10)/10, k.textContent.slice(0,14)]);window.__log.push([Math.round(t),vis]);requestAnimationFrame(f)})()"""
async def main(mode):
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':384,'height':832},has_touch=True,is_mobile=True,color_scheme='dark')
        await c.add_init_script("try{sessionStorage.setItem('vh','1')}catch(e){}")
        pg=await c.new_page(); pg.on('pageerror',lambda x:errs.append(str(x)))
        await pg.goto(URL+'#plan'); await pg.wait_for_timeout(1200)
        cdp=await c.new_cdp_session(pg)
        async def T(t,y=500): await cdp.send('Input.dispatchTouchEvent',{'type':t,'touchPoints':[] if t=='touchEnd' else [{'x':8,'y':y}]})
        if mode=='pull':
            await T('touchStart'); await T('touchMove',480)
            for k in range(8): await pg.evaluate("window.scrollBy(0,600)"); await pg.wait_for_timeout(12)
            await T('touchEnd'); await pg.wait_for_timeout(700)
            await T('touchStart'); await T('touchMove',480)
            for k in range(24): await pg.evaluate("window.scrollBy(0,10)"); await pg.wait_for_timeout(16)
            await pg.evaluate(LOG)
            await T('touchEnd')
        else:
            await pg.evaluate(LOG); await pg.click('#next')
        shots=[]
        for k,ms in enumerate([120,200,250,300,700]):
            await pg.wait_for_timeout(ms); await pg.screenshot(path=OUT+f'/r_{mode}_{k}.png')
        log=await pg.evaluate("window.__log")
        prev=None
        for t,v in log:
            s=' '.join(f'{a}:{y}' for a,y,_ in v)
            print(t,s)
        print('hash',await pg.evaluate('location.hash'),'ERR',errs); await b.close()
asyncio.run(main(sys.argv[1]))
