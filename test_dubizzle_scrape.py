import httpx
from bs4 import BeautifulSoup
import asyncio

async def scrape_dubizzle(query):
    url = f"https://uae.dubizzle.com/search/?keywords={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        # Find all script tags that might contain the __NEXT_DATA__ or json
        script = soup.find("script", id="__NEXT_DATA__")
        if script:
            print("Found NEXT_DATA")
            import json
            data = json.loads(script.string)
            print("Keys in props:", data["props"].keys())
        
        # Alternatively, just look for links
        links = soup.select("a[href*='/ad/']")
        print("Ad links found:", len(links))
        if links:
            print("First link:", links[0].get("href"))

asyncio.run(scrape_dubizzle("iphone 15"))
