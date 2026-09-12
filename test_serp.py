import os
import asyncio
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

async def test_serp():
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_shopping",
        "q": "coffee machine",
        "api_key": os.getenv("SERPAPI_KEY"),
        "hl": "en",
        "gl": "us",
        "num": 1
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        data = r.json()
        if "shopping_results" in data:
            print(json.dumps(data['shopping_results'][0], indent=2))
        else:
            print(data)

if __name__ == "__main__":
    asyncio.run(test_serp())
