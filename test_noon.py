import os
import asyncio
import httpx
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

async def check():
    async with httpx.AsyncClient() as client:
        url = "https://serpapi.com/search.json"
        params = {"engine": "google", "q": "site:noon.com coffee machine", "api_key": api_key, "gl": "ae"}
        r = await client.get(url, params=params)
        data = r.json()
        
        valid_items = []
        for item in data.get("organic_results", []):
            link = item.get("link", "")
            if "/p/" in link or "-item" in link:
                valid_items.append(item)
                
        with open("noon_valid_items.json", "w", encoding="utf-8") as f:
            json.dump(valid_items, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(check())
