import os
import asyncio
import httpx
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

async def test_search():
    query = "coffee machine"
    async with httpx.AsyncClient() as client:
        # 1. Test Amazon
        params = {"engine": "amazon", "q": query, "api_key": api_key, "amazon_domain": "amazon.com"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=20.0)
        print("AMAZON FULL RESPONSE:")
        print(json.dumps(r.json(), indent=2))

if __name__ == "__main__":
    asyncio.run(test_search())
