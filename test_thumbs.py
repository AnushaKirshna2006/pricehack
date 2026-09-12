import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

async def test_engines():
    async with httpx.AsyncClient() as client:
        # Test eBay
        print("Testing eBay...")
        r = await client.get("https://serpapi.com/search.json", params={"engine": "ebay", "_nkw": "coffee machine", "api_key": api_key})
        data = r.json()
        item = data.get("organic_results", [{}])[0]
        print("eBay Title:", item.get("title"))
        print("eBay Thumbnail:", item.get("thumbnail"))

        # Test Noon (Google)
        print("\nTesting Noon...")
        r = await client.get("https://serpapi.com/search.json", params={"engine": "google", "q": "site:noon.com coffee machine", "api_key": api_key})
        data = r.json()
        item = data.get("organic_results", [{}])[0]
        print("Noon Title:", item.get("title"))
        print("Noon Thumbnail:", item.get("thumbnail"))

if __name__ == "__main__":
    asyncio.run(test_engines())
