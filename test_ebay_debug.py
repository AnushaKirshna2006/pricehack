import httpx
from bs4 import BeautifulSoup
import asyncio

async def scrape_ebay(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        print("Status:", r.status_code)
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select(".s-item__wrapper")
        print("Items found:", len(items))
        if items:
            print("First item HTML:", items[0].prettify()[:500])

asyncio.run(scrape_ebay("coffee"))
