import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def debug():
    print("Starting Playwright debug with stealth...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        # Amazon
        print("Fetching Amazon...")
        page = await context.new_page()
        await stealth_async(page)
        try:
            await page.goto("https://www.amazon.com/s?k=yoga+mat", timeout=15000)
            await asyncio.sleep(3)
            html = await page.content()
            with open("amazon_debug.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("Amazon HTML dumped.")
        except Exception as e:
            print(f"Amazon failed: {e}")
        
        # eBay
        print("Fetching eBay...")
        page2 = await context.new_page()
        await stealth_async(page2)
        try:
            await page2.goto("https://www.ebay.com/sch/i.html?_nkw=yoga+mat", timeout=15000)
            await asyncio.sleep(3)
            html2 = await page2.content()
            with open("ebay_debug.html", "w", encoding="utf-8") as f:
                f.write(html2)
            print("eBay HTML dumped.")
        except Exception as e:
            print(f"eBay failed: {e}")
            
        await browser.close()
    print("Done.")

if __name__ == "__main__":
    asyncio.run(debug())
