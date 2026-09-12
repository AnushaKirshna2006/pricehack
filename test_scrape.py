import os
import asyncio
import httpx
from bs4 import BeautifulSoup
import re

async def fetch_direct(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        r = await client.get(url, timeout=15.0)
        return r.text, r.status_code

async def test():
    # Test Noon URL
    noon_url = "https://www.noon.com/uae-en/gaming-laptops/home-and-kitchen/home-appliances-31235/small-appliances/coffee-makers/"
    # Wait, let's test a real Dubizzle URL
    dubizzle_url = "https://dubai.dubizzle.com/classified/computers-networking/computers/laptop-computers/s/brand/apple/"
    
    for platform, url in [("Noon", noon_url), ("Dubizzle", dubizzle_url)]:
        html, status = await fetch_direct(url)
        print(f"[{platform}] STATUS: {status} LENGTH: {len(html)}")
        if status == 200:
            # try to find some price
            match = re.search(r"AED\s*([0-9,]+)", html)
            print(f"[{platform}] Found Price: {match.group(1) if match else 'None'}")

if __name__ == "__main__":
    asyncio.run(test())
