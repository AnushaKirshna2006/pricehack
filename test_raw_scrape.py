import httpx
from bs4 import BeautifulSoup
import asyncio
import re

async def scrape_ebay(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select(".s-item__wrapper")
        results = []
        for item in items[1:3]:  # Skip first 'shop on ebay' item
            title = item.select_one(".s-item__title").text if item.select_one(".s-item__title") else "N/A"
            price = item.select_one(".s-item__price").text if item.select_one(".s-item__price") else "N/A"
            results.append(f"EBAY: {title[:30]} - {price}")
        return results

async def scrape_dubizzle(query):
    url = f"https://uae.dubizzle.com/search/?keywords={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        return f"DUBIZZLE STATUS: {r.status_code}"

async def scrape_amazon(query):
    url = f"https://www.amazon.ae/s?k={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("[data-component-type='s-search-result']")
        results = []
        for item in items[:2]:
            title = item.select_one("h2 span").text if item.select_one("h2 span") else "N/A"
            price_whole = item.select_one(".a-price-whole")
            price = price_whole.text if price_whole else "N/A"
            results.append(f"AMZ: {title[:30]} - {price}")
        return results

async def main():
    q = "coffee"
    print(await scrape_ebay(q))
    print(await scrape_dubizzle(q))
    print(await scrape_amazon(q))

asyncio.run(main())
