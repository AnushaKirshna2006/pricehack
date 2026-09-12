import asyncio
from services.live_data_engine import LiveDataEngine
import json

async def test():
    results = await LiveDataEngine.search_all("iphone 15 pro", limit=8)
    
    platforms = set([r["platform"] for r in results])
    print(f"Found platforms: {platforms}")
    
    for r in results:
        print(f"[{r['platform']}] {r['title'][:50]}... | Price: {r['price']} | URL: {r['product_url'][:30]}...")

if __name__ == "__main__":
    asyncio.run(test())
