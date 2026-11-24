"""Schnelltest: Konsolenfehler, jede Station einmal als Screenshot (PC und Handy)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, OUT, SKIP_INTRO
import asyncio
from playwright.async_api import async_playwright
IDS=["start","plan","revolution","gesellschaft","industrie","sortieren","kolonien","kongo","personen","aufgaben","quiz","kurz-vorher"]
async def main():
    th=os.environ.get('TH','dark'); only=sys.argv[1:] or IDS
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w,h,mob,tag in [(1440,900,False,'pc'),(390,844,True,'ph')]:
            c=await b.new_context(viewport={'width':w,'height':h},is_mobile=mob,has_touch=mob,color_scheme=th)
            await c.add_init_script(SKIP_INTRO)
            pg=await c.new_page(); errs=[]
            pg.on('console',lambda m:errs.append(m.text) if m.type in('error','warning') else None)
            pg.on('pageerror',lambda e:errs.append('PAGEERROR '+str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(1500)
            for st in only:
                await pg.evaluate(f"location.hash='#{st}'"); await pg.wait_for_timeout(1900)
                await pg.screenshot(path=f'{OUT}/sm_{tag}_{th}_{st}.png', full_page=False)
            print(tag, 'Fehler:', errs[:8] if errs else 'keine')
            await c.close()
        await b.close()
asyncio.run(main())
