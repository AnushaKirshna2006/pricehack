import os
import asyncio
import httpx
from services.live_data_engine import LiveDataEngine
from dotenv import load_dotenv

load_dotenv()

async def test():
    print("Testing live search engine...")
    results = await LiveDataEngine.search_all("headphones", limit=8)
    for res in results:
        print(f"[{res.get('platform')}] {res.get('title')[:30]}... | Price: ${res.get('price')} | Image: {str(res.get('image_url'))[:40]}...")

if __name__ == "__main__":
    asyncio.run(test())
