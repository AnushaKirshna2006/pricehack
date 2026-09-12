import os
import httpx
from typing import List, Dict, Any

class LiveDataEngine:
    """
    Fetches real-time e-commerce data using SerpApi (Google Shopping)
    to bypass strict bot protections on Amazon/eBay.
    """

    @staticmethod
    async def extract_exact_image(title: str, api_key: str, client) -> str:
        url = "https://google.serper.dev/images"
        payload = {"q": title}
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        
        try:
            r = await client.post(url, json=payload, headers=headers, timeout=10.0)
            if r.status_code == 200:
                data = r.json()
                images = data.get("images", [])
                for img in images:
                    img_url = img.get("imageUrl")
                    if img_url and not img_url.startswith("x-raw-image"):
                        return img_url
        except Exception:
            pass
            
        return "https://placehold.co/500x500/1a1a1a/444444?text=Image+Not\\nAvailable"

    @staticmethod
    def extract_price_from_item(item: Dict[str, Any]) -> float:
        price_dict = item.get("price", {})
        if isinstance(price_dict, dict) and price_dict.get("extracted"):
            return price_dict.get("extracted")
            
        snippet = item.get("snippet", "")
        title = item.get("title", "")
        text_to_search = str(snippet) + " " + str(title)
        
        import re
        # Match AED 1234, AED1234, Dhs 1234
        match = re.search(r'(?:AED|Dhs|Price:?|AED\.)\s*([\d,]+\.?\d*)', text_to_search, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except:
                pass
                
        # Match $1234
        match = re.search(r'\$\s*([\d,]+\.?\d*)', text_to_search)
        if match:
            try:
                return float(match.group(1).replace(",", "")) * 3.67
            except:
                pass
                
        # Match Suffix: 1499 AED
        match2 = re.search(r"([0-9,]+\.?[0-9]*)\s*(?:AED|Dhs|Dirhams|د\.إ)", text_to_search, re.IGNORECASE)
        if match2:
            try: return float(match2.group(1).replace(",", ""))
            except: pass
                
        return 0.0

    @staticmethod
    async def fetch_platform(client, platform: str, query: str, api_key: str, limit: int = 4) -> List[Dict[str, Any]]:
        results = []
        import asyncio
        try:
            if platform == "Amazon":
                url = f"https://www.amazon.ae/s?k={query}"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5"
                }
                r = await client.get(url, headers=headers, timeout=15.0)
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(r.text, "html.parser")
                items = soup.select("[data-component-type='s-search-result']")
                for item in items:
                    title_elem = item.select_one("h2 span")
                    title = title_elem.text if title_elem else "Amazon Product"
                    
                    link_elem = item.select_one("h2 a")
                    link = "https://www.amazon.ae" + link_elem["href"] if link_elem else f"https://www.amazon.ae/s?k={query}"
                    
                    price_whole = item.select_one(".a-price-whole")
                    if not price_whole: continue
                    try:
                        real_price = float(price_whole.text.replace(",", ""))
                        real_usd_price = real_price / 3.67
                    except:
                        continue
                    
                    img_elem = item.select_one(".s-image")
                    image_url = img_elem["src"] if img_elem else None
                    
                    results.append({
                        "platform": "Amazon",
                        "platform_product_id": f"AMZ-{len(results)}",
                        "product_url": link,
                        "title": title,
                        "image_url": image_url,
                        "price": real_usd_price,
                        "star_rating": 4.5,
                        "review_count": 150
                    })
                    if len(results) >= limit: break
                    
            elif platform == "eBay":
                url = "https://google.serper.dev/search"
                payload = {"q": f"site:ebay.com intitle:\"{query}\"", "gl": "ae", "num": 10}
                headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
                r = await client.post(url, json=payload, headers=headers, timeout=30.0)
                data = r.json()
                for item in data.get("organic", []):
                    title = item.get("title", "eBay Product").replace(" | eBay", "")
                    
                    extracted_price = LiveDataEngine.extract_price_from_item(item)
                    if not extracted_price or extracted_price < 5: continue
                    real_usd_price = extracted_price / 3.67
                    
                    results.append({
                        "platform": "eBay",
                        "platform_product_id": f"EBY-{len(results)}",
                        "product_url": item.get("link", f"https://www.ebay.com/sch/i.html?_nkw={query}"),
                        "title": title,
                        "image_url": item.get("imageUrl"),
                        "price": real_usd_price,
                        "star_rating": 4.2,
                        "review_count": 85
                    })
                    if len(results) >= limit: break
                    
            elif platform == "Noon":
                url = f"https://www.noon.com/_svc/catalog/api/v3/u/search?q={query}&limit={limit*2}"
                headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json", "x-cms": "v2", "x-locale": "en-ae"}
                r = await client.get(url, headers=headers, timeout=30.0)
                if r.status_code == 200:
                    data = r.json()
                    for item in data.get("hits", []):
                        title = item.get("name", "Noon Product")
                        pdp_url = item.get('pdp_url') or f"/{item.get('url')}/p/"
                        link = f"https://www.noon.com/uae-en{pdp_url}"
                        image_key = item.get("image_key")
                        image_url = f"https://f.nooncdn.com/products/tr:n-t_400/{image_key}.jpg" if image_key else None
                            
                        real_price = item.get("sale_price") or item.get("price")
                        if not real_price:
                            continue
                            
                        real_usd_price = float(real_price) / 3.67
                        
                        results.append({
                            "platform": "Noon",
                            "platform_product_id": f"NOON-{len(results)}",
                            "product_url": link,
                            "title": title,
                            "image_url": image_url,
                            "price": real_usd_price, 
                            "star_rating": 4.4,
                            "review_count": 120
                        })
                        if len(results) >= limit: break
                    
            elif platform == "Dubizzle":
                url = "https://google.serper.dev/search"
                payload = {"q": f"site:dubizzle.com intitle:\"{query}\" \"AED\"", "gl": "ae", "num": 10}
                headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
                r = await client.post(url, json=payload, headers=headers, timeout=30.0)
                data = r.json()
                for item in data.get("organic", []):
                    link = item.get("link", "")
                    
                    if "/search/" in link or "/s/" in link or link.endswith("-appliances/") or link.endswith("-computers/"):
                        continue
                        
                    title = item.get("title", "Dubizzle Product").replace(" - dubizzle", "")
                        
                    real_price = LiveDataEngine.extract_price_from_item(item)
                    if not real_price or real_price < 5:
                        continue
                        
                    real_usd_price = real_price / 3.67
                    
                    results.append({
                        "platform": "Dubizzle",
                        "platform_product_id": f"DUB-{len(results)}",
                        "product_url": link,
                        "title": title,
                        "image_url": item.get("imageUrl"),
                        "price": real_usd_price,
                        "star_rating": 4.0,
                        "review_count": 45
                    })
                    if len(results) >= limit: break

            async def fetch_missing_image(res):
                if not res.get("image_url"):
                    res["image_url"] = await LiveDataEngine.extract_exact_image(res["title"], api_key, client)

            await asyncio.gather(*(fetch_missing_image(r) for r in results))

        except Exception as e:
            print(f"Error fetching {platform}:", e)
        return results

    @staticmethod
    async def search_all(query: str, limit: int = 16) -> List[Dict[str, Any]]:
        from dotenv import load_dotenv
        import os
        load_dotenv(override=True)
        # Use SERPER_API_KEY for Serper.dev
        api_key = os.getenv("SERPER_API_KEY", "fallback")

        results = []
        import asyncio
        async with httpx.AsyncClient() as client:
            tasks = [
                LiveDataEngine.fetch_platform(client, "Amazon", query, api_key, limit=4),
                LiveDataEngine.fetch_platform(client, "eBay", query, api_key, limit=4),
                LiveDataEngine.fetch_platform(client, "Noon", query, api_key, limit=4),
                LiveDataEngine.fetch_platform(client, "Dubizzle", query, api_key, limit=4)
            ]
            fetched_lists = await asyncio.gather(*tasks)
            for items in fetched_lists:
                results.extend(items)
                    
        return results
