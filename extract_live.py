import asyncio
from playwright.async_api import async_playwright

async def extract_image(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        page = await context.new_page()
        try:
            print(f"Navigating to {url}...")
            await page.goto(url, timeout=20000)
            await asyncio.sleep(3) # Wait for JS rendering
            
            # Try to find a prominent image
            img_element = await page.query_selector('meta[property="og:image"]')
            if img_element:
                content = await img_element.get_attribute('content')
                if content:
                    print(f"Found og:image: {content}")
                    return
            
            # Fallback to largest image
            imgs = await page.evaluate('''() => {
                return Array.from(document.images).map(img => img.src).filter(src => src.startsWith('http'));
            }''')
            print(f"Found {len(imgs)} images on page. First 3: {imgs[:3]}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(extract_image("https://uae.dubizzle.com/classified/sports-equipment/fitness/"))
    asyncio.run(extract_image("https://www.noon.com/uae-en/2200-series-fully-automatic-espresso-machine/N31015694A/p/"))
