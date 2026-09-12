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
        # 1. Test Amazon
        params = {"engine": "amazon", "k": query, "term": query, "api_key": api_key, "amazon_domain": "amazon.com"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=20.0)
        print("AMAZON RESPONSE:")
        print(json.dumps(r.json().get("amazon_results", [])[:1], indent=2))
        if "error" in r.json():
            print("AMZ ERROR:", r.json()["error"])
            
        # 2. Test Dubizzle
        params = {"engine": "google", "q": f"site:dubizzle.com/ae/ {query}", "api_key": api_key, "gl": "ae"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=20.0)
        print("\nDUBIZZLE RESPONSE:")
        print(json.dumps(r.json().get("organic_results", [])[:2], indent=2))

if __name__ == "__main__":
    asyncio.run(test_search())
