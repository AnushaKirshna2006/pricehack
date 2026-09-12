import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

async def test():
    query = "laptop"
    async with httpx.AsyncClient() as client:
        params = {"engine": "google_shopping", "q": query, "api_key": api_key, "gl": "ae", "hl": "en"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=10.0)
        data = r.json()
        print("GOOGLE SHOPPING UAE:")
        for item in data.get("shopping_results", [])[:10]:
            print(f"[{item.get('source')}] {item.get('title')} - {item.get('extracted_price')} {item.get('price')}")

if __name__ == "__main__":
    asyncio.run(test())
