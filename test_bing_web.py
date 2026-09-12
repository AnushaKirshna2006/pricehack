import asyncio
import httpx
import bs4
import urllib.parse

async def test_bing_web():
    query = "site:amazon.com iphone 15"
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}, timeout=10.0)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all('li', class_='b_algo')
        print(f"Found {len(results)} results")
        for res in results[:3]:
            h2 = res.find('h2')
            title = h2.text if h2 else 'No Title'
            a = h2.find('a') if h2 else None
            link = a['href'] if a and a.has_attr('href') else 'No Link'
            snippet = res.find('div', class_='b_caption')
            desc = snippet.text if snippet else 'No Desc'
            print(f"Title: {title}\nLink: {link}\nDesc: {desc}\n")

if __name__ == "__main__":
    asyncio.run(test_bing_web())
