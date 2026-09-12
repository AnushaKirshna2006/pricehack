import httpx
import asyncio

async def scrape_dubizzle(query):
    url = f"https://uae.dubizzle.com/search/?keywords={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        print("STATUS:", r.status_code)
        print("HTML PREVIEW:", r.text[:1000])

asyncio.run(scrape_dubizzle("iphone"))
