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
        # Amazon SerpApi full response
        params = {"engine": "amazon", "k": query, "api_key": api_key, "amazon_domain": "amazon.ae"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=10.0)
        print("AMZ FULL RESPONSE:", json.dumps(r.json(), indent=2)[:500])
        
        # Dubizzle API?
        try:
            url = f"https://www.dubizzle.com/api/v1/search/?keyword={query}"
            r = await client.get(url, timeout=5.0)
            print("DUB STATUS:", r.status_code)
        except Exception as e:
            print("DUB ERROR:", e)

if __name__ == "__main__":
    asyncio.run(test())
