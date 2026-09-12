import asyncio
import httpx
import bs4
import urllib.parse

async def test(query):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}, timeout=5.0)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        imgs = soup.find_all('img', class_='mimg')
        print(f"Results for '{query}':")
        for img in imgs[:3]:
            src = img.get('src') or img.get('data-src')
            print(src)
        print("-" * 20)

if __name__ == "__main__":
    asyncio.run(test("Iphone 15"))
    asyncio.run(test("BalanceFrom GoYoga All-Purpose 1/2-Inch Extra Thick High Density Anti-Tear Exercise Yoga Mat"))
