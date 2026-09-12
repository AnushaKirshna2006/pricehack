import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

async def test():
    query = "laptop"
    async with httpx.AsyncClient() as client:
        params = {"engine": "google", "q": "site:dubizzle.com laptop", "api_key": api_key, "gl": "ae"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=10.0)
        dub = r.json().get("organic_results", [])
        for item in dub:
            snippet = item.get("snippet", "").encode("ascii", "ignore").decode("ascii")
            print(f"TITLE: {item.get('title')}")
            print(f"SNIPPET: {snippet}\n")

if __name__ == "__main__":
    asyncio.run(test())
