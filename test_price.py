import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

async def check():
    async with httpx.AsyncClient() as client:
        # Check Noon
        url = "https://serpapi.com/search.json"
        params = {"engine": "google", "q": "site:noon.com coffee machine", "api_key": api_key, "gl": "ae"}
        r = await client.get(url, params=params)
        data = r.json()
        for item in data.get("organic_results", [])[:2]:
            print("NOON Snippet:", item.get("snippet"))
            print("NOON Rich Snippet:", item.get("rich_snippet"))
            print("NOON Price:", item.get("price"))
            
        # Check Dubizzle
        params = {"engine": "google", "q": "site:dubizzle.com coffee machine", "api_key": api_key, "gl": "ae"}
        r = await client.get(url, params=params)
        data = r.json()
        for item in data.get("organic_results", [])[:2]:
            print("DUBIZZLE Snippet:", item.get("snippet"))
            print("DUBIZZLE Rich Snippet:", item.get("rich_snippet"))
            print("DUBIZZLE Price:", item.get("price"))

if __name__ == "__main__":
    asyncio.run(check())
