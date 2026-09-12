import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth

async def test_amazon():
    print("Testing Amazon...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = await context.new_page()
            await stealth(page)
            
            await page.goto("https://www.amazon.com/s?k=laptop", timeout=20000)
            await asyncio.sleep(2)
            title = await page.title()
            print("Amazon Title:", title)
            
            # Try finding a product
            products = await page.query_selector_all("div[data-component-type='s-search-result']")
            print(f"Found {len(products)} products on Amazon")
            if products:
                price = await products[0].query_selector(".a-price-whole")
                if price:
                    print("First product price:", await price.inner_text())
            await browser.close()
    except Exception as e:
        print("Amazon Error:", e)

if __name__ == "__main__":
    asyncio.run(test_amazon())
