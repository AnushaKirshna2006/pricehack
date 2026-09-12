import os
import asyncio
import httpx
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

async def test():
    query = "laptop"
    async with httpx.AsyncClient() as client:
        params = {"engine": "amazon", "k": query, "api_key": api_key, "amazon_domain": "amazon.ae"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=10.0)
        data = r.json()
        print("AMAZON ITEMS:")
        for item in data.get("amazon_results", [])[:3]:
            print(item.get("title"))
            print("Price:", item.get("extracted_price"), item.get("price"))

if __name__ == "__main__":
    asyncio.run(test())
