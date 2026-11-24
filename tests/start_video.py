import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import URL, SITE, OUT, Q, SKIP_INTRO
import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();w,h=int(sys.argv[1]),int(sys.argv[2])
        c=await b.new_context(viewport={'width':w,'height':h},color_scheme='dark',record_video_dir=OUT+'/vid',record_video_size={'width':w//2,'height':h//2})
        if len(sys.argv)>3: await c.add_init_script("try{sessionStorage.setItem('vh','1')}catch(e){}")
        pg=await c.new_page();await pg.goto(URL+''+(sys.argv[4] if len(sys.argv)>4 else ''),wait_until='commit')
        await pg.wait_for_timeout(4000);await c.close();await b.close()
asyncio.run(main())
