import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, SITE, OUT, Q, SKIP_INTRO
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':384,'height':832},has_touch=True,is_mobile=True,color_scheme='dark')
        await c.add_init_script("try{sessionStorage.setItem('vh','1')}catch(e){}")
        pg=await c.new_page(); pg.on('pageerror',lambda x:errs.append(str(x)))
        await pg.goto(URL+'#kolonien'); await pg.wait_for_timeout(1300)
        cdp=await c.new_cdp_session(pg)
        async def T(t,y=300): await cdp.send('Input.dispatchTouchEvent',{'type':t,'touchPoints':[] if t=='touchEnd' else [{'x':200,'y':y}]})
        # kurzer Zug: zurückfedern
        await T('touchStart',300)
        for k in range(8): await T('touchMove',300+k*15); await pg.wait_for_timeout(16)
        await pg.screenshot(path=OUT+'/bk_0.png'); await T('touchEnd'); await pg.wait_for_timeout(500)
        print('kurz:',await pg.evaluate('location.hash'))
        await T('touchStart',250)
        for k in range(16): await T('touchMove',250+k*20); await pg.wait_for_timeout(16)
        await pg.screenshot(path=OUT+'/bk_1.png'); await T('touchEnd')
        for k in range(3): await pg.wait_for_timeout(150); await pg.screenshot(path=OUT+f'/bk_{k+2}.png')
        await pg.wait_for_timeout(600)
        print('lang:',await pg.evaluate('location.hash'),'scrollY',await pg.evaluate('scrollY'),'max',await pg.evaluate('document.documentElement.scrollHeight-innerHeight'))
        await c.close()
        c=await b.new_context(viewport={'width':1287,'height':900},color_scheme='dark')
        await c.add_init_script("try{sessionStorage.setItem('vh','1')}catch(e){}")
        pg=await c.new_page(); pg.on('pageerror',lambda x:errs.append(str(x)))
        await pg.goto(URL+'#kolonien'); await pg.wait_for_timeout(1300)
        await pg.mouse.move(700,400); await pg.mouse.wheel(0,-100); await pg.wait_for_timeout(250); await pg.screenshot(path=OUT+'/bk_d.png'); await pg.wait_for_timeout(800)
        print('rad:',await pg.evaluate('location.hash'))
        await pg.click('#pathlist a[href="#gesellschaft"]'); await pg.wait_for_timeout(250); await pg.screenshot(path=OUT+'/bk_s.png'); await pg.wait_for_timeout(800)
        print('leiste:',await pg.evaluate('location.hash'))
        await pg.click('#pathlist a[href="#kongo"]'); await pg.wait_for_timeout(1300); print('leiste vor:',await pg.evaluate('location.hash'))
        await pg.go_back(); await pg.wait_for_timeout(1300); print('browser zurück:',await pg.evaluate('location.hash'))
        print('ERR',errs); await b.close()
asyncio.run(main())
