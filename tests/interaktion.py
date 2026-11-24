"""Klickt Quiz, Sortierübung, Quellen-Stellen, Kartenstapel, Häkchen und Etappen einmal durch und meldet JS-Fehler."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, OUT, SKIP_INTRO
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); c=await b.new_context(viewport={'width':1280,'height':900},color_scheme='dark')
        await c.add_init_script(SKIP_INTRO); pg=await c.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(URL+'#quiz'); await pg.wait_for_timeout(1500)
        for k in range(25):
            await pg.click('#s-quiz .opt >> nth=0'); await pg.wait_for_timeout(60); await pg.click('#s-quiz .qnav .btn'); await pg.wait_for_timeout(60)
        print('Quiz-Ende:', (await pg.inner_text('#s-quiz .qcard'))[:80].replace('\n',' '))
        await pg.goto(URL+'#sortieren'); await pg.wait_for_timeout(1300)
        for k in range(6):
            await pg.click('#pool .sitem >> nth=0 >> button.o'); await pg.wait_for_timeout(700)
        print('Sortieren:', await pg.inner_text('#sortscore'))
        await pg.goto(URL+'#industrie'); await pg.wait_for_timeout(1300)
        await pg.click('#s-industrie .items .ck >> nth=0'); await pg.click('#s-industrie .deck .deck-ctrl .yes'); await pg.wait_for_timeout(500)
        await pg.goto(URL+'#plan'); await pg.wait_for_timeout(1300)
        print('Plan:', (await pg.inner_text('#gl .glb >> nth=1'))[:40].replace('\n',' '))
        await pg.goto(URL+'#aufgaben'); await pg.wait_for_timeout(1300)
        print('Aufgaben:', (await pg.inner_text('#s-aufgaben .baustein >> nth=0'))[:60].replace('\n',' '))
        await pg.goto(URL+'#kurz-vorher'); await pg.wait_for_timeout(1500)
        print('Offen:', await pg.locator('#todo .chip').count(), '|', await pg.inner_text('#stats2'))
        await pg.goto(URL+'#start'); await pg.wait_for_timeout(1300); print('Start:', await pg.inner_text('#startline'))
        print('Fehler:', errs or 'keine'); await b.close()
asyncio.run(main())
