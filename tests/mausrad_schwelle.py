import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, SITE, OUT, Q, SKIP_INTRO
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();c=await b.new_context(viewport={'width':1440,'height':900},color_scheme='dark')
        await c.add_init_script("try{sessionStorage.setItem('vh','1')}catch(e){}")
        pg=await c.new_page();await pg.goto(URL+'#plan');await pg.wait_for_timeout(2500)
        await pg.mouse.move(800,450)
        H=lambda: pg.evaluate('location.hash')
        # A: scroll down to the end, pause 250ms, one notch
        for k in range(40):
            await pg.mouse.wheel(0,100);await pg.wait_for_timeout(60)
            if await H()!='#plan':break
        print('A during scroll-down hash',await H())
        await pg.wait_for_timeout(250);await pg.mouse.wheel(0,100);await pg.wait_for_timeout(1600);print('A after notch',await H())
        # B: arrival, then notch 350ms later on whatever page; scroll page to end first
        h0=await H()
        await pg.evaluate('window.scrollTo(0,document.documentElement.scrollHeight)');await pg.wait_for_timeout(900)
        await pg.mouse.wheel(0,100);await pg.wait_for_timeout(1700);print('B from',h0,'->',await H())
        # C: fast continuous spin of 60 events at 25ms, starting at end of page
        h1=await H();await pg.evaluate('window.scrollTo(0,document.documentElement.scrollHeight)');await pg.wait_for_timeout(900)
        for k in range(60):
            await pg.mouse.wheel(0,100);await pg.wait_for_timeout(25)
        await pg.wait_for_timeout(1500);print('C from',h1,'->',await H())
        # D: bounce check: armed at rest, notch -> record max over-pull without crossing? log scrollY
        await b.close()
asyncio.run(main())
