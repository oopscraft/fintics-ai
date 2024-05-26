import nest_asyncio
import asyncio
from pyppeteer import launch
from playwright.async_api import async_playwright

# apply nest_asyncio
nest_asyncio.apply()

async def fetch_page_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until='domcontentloaded', timeout=60000)
        content = await page.content()
        await browser.close()
        return content

def get_html_content(url):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        return loop.run_until_complete(fetch_page_content(url))
    else:
        return asyncio.run(fetch_page_content(url))
