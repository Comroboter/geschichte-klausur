import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, SITE, OUT, Q, SKIP_INTRO
import asyncio,json
from playwright.async_api import async_playwright
N=json.load(open(os.path.join(Q,'narration.json'),encoding='utf-8'))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']); c=await b.new_context(viewport={'width':1287,'height':1000},color_scheme='dark')
        await c.add_init_script("try{sessionStorage.setItem('vh','1')}catch(e){}")
        pg=await c.new_page(); errs=[]; pg.on('pageerror',lambda x:errs.append(str(x))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        miss=[]
        for sid,segs in N.items():
            await pg.goto(URL+'#'+sid); await pg.wait_for_timeout(700)
            for sel,_ in segs:
                ok=await pg.evaluate("""(sel)=>{const st=document.querySelector('.station.on');return [...st.querySelectorAll(sel)].some(e=>!e.closest('.runway')&&e.getClientRects().length)}""",sel)
                if not ok: miss.append((sid,sel))
        print('fehlende Ziele',miss)
        await pg.goto(URL+'#plan'); await pg.wait_for_timeout(1200)
        await pg.click('#narr'); 
        for k in range(5):
            await pg.wait_for_timeout(3000)
            print(await pg.evaluate("[location.hash,document.querySelector('.narr-hl')?.className.slice(0,30),document.getElementById('narrtx').textContent.slice(0,50),document.getElementById('narrcap').className,Math.round(scrollY)]"))
            if k==2: await pg.screenshot(path=OUT+'/narr.png')
        print(errs); await b.close()
asyncio.run(main())
