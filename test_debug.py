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
        params = {"engine": "amazon", "q": query, "api_key": api_key, "amazon_domain": "amazon.ae"}
        r = await client.get("https://serpapi.com/search.json", params=params)
        amz_data = r.json().get("amazon_results", [])[:3]
        
        # 2. Test Dubizzle
        params = {"engine": "google", "q": f"site:dubizzle.com/ae/ {query}", "api_key": api_key, "gl": "ae"}
        r = await client.get("https://serpapi.com/search.json", params=params)
        dub_data = r.json().get("organic_results", [])[:5]
        
        # 3. Test Noon
        params = {"engine": "google", "q": f"site:noon.com/uae-en/ {query}", "api_key": api_key, "gl": "ae"}
        r = await client.get("https://serpapi.com/search.json", params=params)
        noon_data = r.json().get("organic_results", [])[:5]

        with open("debug_results.json", "w", encoding="utf-8") as f:
            json.dump({
                "amazon": amz_data,
                "dubizzle": dub_data,
                "noon": noon_data
            }, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(test_search())
