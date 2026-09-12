import os
import asyncio
import httpx
import json

async def test():
    query = "headphones"
    url = f"https://www.noon.com/_svc/catalog/api/v3/u/search?q={query}&limit=2"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json", "x-cms": "v2", "x-locale": "en-ae"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        data = r.json()
        for hit in data.get("hits", []):
            print("NOON URL KEY:", hit.get("url"))
            print("NOON PDP URL:", hit.get("pdp_url"))
            print("NOON PRICE:", hit.get("price"))
            break
            
if __name__ == "__main__":
    asyncio.run(test())
