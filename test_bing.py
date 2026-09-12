import asyncio
import httpx
import bs4
import urllib.parse

async def test():
    query = "Iphone 15 - Amazon Best Seller"
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query + ' product')}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}, timeout=5.0)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        imgs = soup.find_all('img', class_='mimg')
        print(f"Found {len(imgs)} images with class mimg")
        for img in imgs[:5]:
            print(img.get('src'))

if __name__ == "__main__":
    asyncio.run(test())
