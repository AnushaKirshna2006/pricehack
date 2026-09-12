import os
import asyncio
import httpx
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

async def test_search():
    query = "laptop"
    async with httpx.AsyncClient() as client:
        # Test Amazon Google
        params = {"engine": "google", "q": f"site:amazon.ae {query}", "api_key": api_key, "gl": "ae"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=20.0)
        data = r.json()
        print("AMAZON ORGANIC:")
        for item in data.get("organic_results", [])[:3]:
            print(item.get("title"))
            print(item.get("rich_snippet", {}).get("top", {}).get("detected_extensions", {}).get("price"))
            print(item.get("link"))
            
        print("\n\nDUBIZZLE ORGANIC:")
        params = {"engine": "google", "q": f"site:dubizzle.com {query}", "api_key": api_key, "gl": "ae"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=20.0)
        data = r.json()
        for item in data.get("organic_results", [])[:3]:
            print(item.get("title"))
            print(item.get("link"))

if __name__ == "__main__":
    asyncio.run(test_search())
