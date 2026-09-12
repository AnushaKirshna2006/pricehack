import os
import asyncio
import httpx
import json

async def test_noon():
    query = "laptop"
    url = f"https://www.noon.com/_svc/catalog/api/v3/u/search?q={query}&limit=2"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json", "x-cms": "v2", "x-locale": "en-ae"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        data = r.json()
        for hit in data.get("hits", []):
            print("TITLE:", hit.get("name"))
            print("IMAGE KEYS:", hit.keys())
            print("IMAGE_KEY:", hit.get("image_key"))
            print("IMAGE_VERSION:", hit.get("image_version"))
            print("SKU:", hit.get("sku"))
            print("IMAGES:", hit.get("image_keys"))

if __name__ == "__main__":
    asyncio.run(test_noon())
