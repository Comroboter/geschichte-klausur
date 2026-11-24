import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, SITE, OUT, Q, SKIP_INTRO
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for ot,dh in [(53,53),(0,53)]:
            c=await b.new_context(viewport={'width':1080,'height':810},is_mobile=True,has_touch=True,color_scheme='dark')
            await c.add_init_script("try{sessionStorage.setItem('vh','1')}catch(e){};Object.defineProperty(window,'visualViewport',{value:{offsetTop:%d,get height(){return innerHeight-%d},scale:1,addEventListener(){}}})"%(ot,dh))
            pg=await c.new_page();await pg.goto(URL+'#kolonien');await pg.wait_for_timeout(2500)
            # Ohne Tastatur: Safari setzt die Leisten selbst, oben darf nichts verschoben werden. Mit Tastatur (Fokus im Textfeld) schon.
            print(ot,dh,await pg.evaluate('[getComputedStyle(document.querySelector(".topbar")).getPropertyValue("--vvt"),getComputedStyle(document.querySelector(".bottombar")).getPropertyValue("--vvb"),Math.round(document.querySelector(".topbar").getBoundingClientRect().top),Math.round(document.querySelector(".bottombar").getBoundingClientRect().bottom)]'))
            await pg.evaluate("(()=>{const i=document.createElement('input');i.id='__t';document.body.appendChild(i);i.focus();window.vvUpdate()})()");await pg.wait_for_timeout(700)
            print('  mit Tastatur',await pg.evaluate('[getComputedStyle(document.querySelector(".topbar")).getPropertyValue("--vvt"),Math.round(document.querySelector(".topbar").getBoundingClientRect().top)]'))
            await c.close()
        await b.close()
asyncio.run(main())
