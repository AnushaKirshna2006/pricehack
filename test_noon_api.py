import os
import asyncio
import httpx

async def test_noon_api():
    query = "laptop"
    # Noon search API
    url = f"https://www.noon.com/_svc/catalog/api/v3/u/search?q={query}&limit=5"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "x-cms": "v2",
        "x-locale": "en-ae"
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        print("NOON API STATUS:", r.status_code)
        if r.status_code == 200:
            print("NOON API SUCCESS! Length:", len(r.text))
            data = r.json()
            hits = data.get("hits", [])
            for hit in hits:
                print(hit.get("name"), "PRICE:", hit.get("price"))

if __name__ == "__main__":
    asyncio.run(test_noon_api())
