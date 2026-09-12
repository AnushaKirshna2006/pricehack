import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

async def test():
    async with httpx.AsyncClient() as client:
        # Amazon
        params = {"engine": "google", "q": "site:amazon.ae/dp/ OR site:amazon.com/dp/ laptop", "api_key": api_key, "gl": "ae"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=10.0)
        amz = r.json().get("organic_results", [])
        amz_with_price = [i for i in amz if i.get("rich_snippet", {}).get("top", {}).get("detected_extensions", {}).get("price")]
        print(f"AMAZON: {len(amz_with_price)} out of {len(amz)} have price.")

        # Dubizzle
        params = {"engine": "google", "q": "site:dubizzle.com laptop", "api_key": api_key, "gl": "ae"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=10.0)
        dub = r.json().get("organic_results", [])
        dub_with_price = [i for i in dub if i.get("rich_snippet", {}).get("top", {}).get("detected_extensions", {}).get("price")]
        print(f"DUBIZZLE: {len(dub_with_price)} out of {len(dub)} have price.")

if __name__ == "__main__":
    asyncio.run(test())
