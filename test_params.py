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
        # Test 1: term only
        params = {"engine": "amazon", "term": query, "api_key": api_key, "amazon_domain": "amazon.com"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=20.0)
        print("TEST 1 term only:", r.json().get("error", "SUCCESS - " + str(len(r.json().get("amazon_results", []))) + " results"))
        
        # Test 2: k only
        params = {"engine": "amazon", "k": query, "api_key": api_key, "amazon_domain": "amazon.com"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=20.0)
        print("TEST 2 k only:", r.json().get("error", "SUCCESS - " + str(len(r.json().get("amazon_results", []))) + " results"))
        
        # Test 3: site:dubizzle.com
        params = {"engine": "google", "q": f"site:dubizzle.com {query}", "api_key": api_key, "gl": "ae"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=20.0)
        print("TEST 3 dubizzle:", "SUCCESS - " + str(len(r.json().get("organic_results", []))) + " results")

if __name__ == "__main__":
    asyncio.run(test_search())
