import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

async def test():
    query = "headphones"
    async with httpx.AsyncClient() as client:
        # Amazon
        params = {"engine": "google", "q": f"site:amazon.ae {query} \"AED\"", "api_key": api_key, "gl": "ae", "num": 20}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=15.0)
        amz = r.json().get("organic_results", [])
        amz_dp = [i for i in amz if "/dp/" in i.get("link", "")]
        print(f"AMAZON ALL: {len(amz)} DP: {len(amz_dp)}")
        for i in amz_dp[:3]:
            print(i.get("title"), "PRICE:", i.get("rich_snippet", {}).get("top", {}).get("detected_extensions", {}).get("price"))
        
        # Dubizzle
        params = {"engine": "google", "q": f"site:dubizzle.com intitle:{query} \"AED\"", "api_key": api_key, "gl": "ae", "num": 20}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=15.0)
        dub = r.json().get("organic_results", [])
        print(f"DUBIZZLE ALL: {len(dub)}")
        for i in dub[:3]:
            print(i.get("title"), "PRICE:", i.get("rich_snippet", {}).get("top", {}).get("detected_extensions", {}).get("price"))
            
if __name__ == "__main__":
    asyncio.run(test())
