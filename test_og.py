import asyncio
import httpx
from bs4 import BeautifulSoup

async def get_og_image(url):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, timeout=10.0)
            print(f"{url} Status: {r.status_code}")
            soup = BeautifulSoup(r.text, 'html.parser')
            og_img = soup.find('meta', property='og:image')
            if og_img:
                return og_img.get('content')
            
            # fallback: find first big image
            img = soup.find('img')
            return img.get('src') if img else None
    except Exception as e:
        print(f"Error {url}: {e}")
        return None

async def test():
    urls = [
        "https://www.ebay.com/sch/i.html?_nkw=coffee+machine",
        "https://www.noon.com/uae-en/search/?q=coffee%20machine",
        "https://uae.dubizzle.com/search/?keywords=coffee%20machine"
    ]
    for u in urls:
        img = await get_og_image(u)
        print(f"Image for {u}: {img}")

if __name__ == "__main__":
    asyncio.run(test())
