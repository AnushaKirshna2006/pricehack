import asyncio
from typing import List, Dict, Any

class MockDataEngine:
    """
    Returns high-fidelity product data for demonstrations when live scraping is blocked by CAPTCHAs.
    """

    MOCK_DB = {
        "yoga mat": {
            "Amazon": [
                {
                    "title": "BalanceFrom GoYoga All-Purpose 1/2-Inch Extra Thick High Density Anti-Tear Exercise Yoga Mat",
                    "url": "https://www.amazon.com/dp/B00FO9ZRYQ",
                    "image": "https://m.media-amazon.com/images/I/71R2QZ+6+0L._AC_SL1500_.jpg",
                    "price": 17.99,
                    "rating": 4.6,
                    "reviews": 85000
                },
                {
                    "title": "Gaiam Yoga Mat Premium Print Non Slip Exercise & Fitness Mat",
                    "url": "https://www.amazon.com/dp/B003WJ1B3I",
                    "image": "https://m.media-amazon.com/images/I/91tK0Q-cKKL._AC_SL1500_.jpg",
                    "price": 29.98,
                    "rating": 4.7,
                    "reviews": 23000
                }
            ],
            "eBay": [
                {
                    "title": "Lululemon The Reversible Mat 5mm Yoga Mat Black",
                    "url": "https://www.ebay.com/b/Yoga-Mats/14894/bn_1922709",
                    "image": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500&q=80",
                    "price": 88.00,
                    "rating": 4.8,
                    "reviews": 120
                },
                {
                    "title": "Manduka PRO Yoga Mat 6mm Thick",
                    "url": "https://www.ebay.com/b/Yoga-Mats/14894/bn_1922709",
                    "image": "https://images.unsplash.com/photo-1593810450967-f9c427ce3722?w=500&q=80",
                    "price": 105.00,
                    "rating": 4.9,
                    "reviews": 55
                }
            ],
            "Noon": [
                {
                    "title": "SkyLand High Density Anti-Tear Yoga Mat 10mm Black",
                    "url": "https://www.noon.com/uae-en/high-density-anti-tear-yoga-mat/N14299948A/p/",
                    "image": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=500&q=80",
                    "price": 45.00,
                    "rating": 4.2,
                    "reviews": 310
                }
            ],
            "Dubizzle": [
                {
                    "title": "Lightly Used Lululemon Yoga Mat 5mm",
                    "url": "https://uae.dubizzle.com/classified/sports-equipment/fitness/",
                    "image": "https://images.unsplash.com/photo-1599447421416-3414500d18a5?w=500&q=80",
                    "price": 30.00,
                    "rating": 4.0,
                    "reviews": 2
                }
            ]
        },
        "coffee machine": {
            "Amazon": [
                {
                    "title": "Keurig K-Classic Coffee Maker, Single Serve K-Cup Pod Coffee Brewer",
                    "url": "https://www.amazon.com/dp/B018UQ5AMS",
                    "image": "https://m.media-amazon.com/images/I/61r5TbqxJ3L._AC_SL1500_.jpg",
                    "price": 109.99,
                    "rating": 4.7,
                    "reviews": 104000
                },
                {
                    "title": "Nespresso Vertuo Plus Coffee and Espresso Machine by De'Longhi",
                    "url": "https://www.amazon.com/dp/B01N7T3CUK",
                    "image": "https://m.media-amazon.com/images/I/61u9+52Y0xL._AC_SL1500_.jpg",
                    "price": 139.00,
                    "rating": 4.6,
                    "reviews": 15000
                }
            ],
            "eBay": [
                {
                    "title": "Breville BES870XL Barista Express Espresso Machine - Brushed Stainless Steel",
                    "url": "https://www.ebay.com/b/Espresso-Machines/38252/bn_319760",
                    "image": "https://images.unsplash.com/photo-1517701550927-30cf0b6af758?w=500&q=80",
                    "price": 549.95,
                    "rating": 4.8,
                    "reviews": 412
                }
            ],
            "Noon": [
                {
                    "title": "Philips 2200 Series Fully Automatic Espresso Machine Classic Milk Frother",
                    "url": "https://www.noon.com/uae-en/2200-series-fully-automatic-espresso-machine/N31015694A/p/",
                    "image": "https://images.unsplash.com/photo-1520092359194-9190db9d2b27?w=500&q=80",
                    "price": 329.00,
                    "rating": 4.5,
                    "reviews": 890
                }
            ],
            "Dubizzle": [
                {
                    "title": "Nespresso Pixie (Used, good condition)",
                    "url": "https://uae.dubizzle.com/classified/home-appliances/kitchen/coffee-makers/",
                    "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500&q=80",
                    "price": 85.00,
                    "rating": 4.0,
                    "reviews": 5
                }
            ]
        }
    }

    @staticmethod
    async def extract_exact_image(search_term: str) -> str:
        # Returning a fast, static placeholder. Real-time Bing scraping causes 5s timeouts.
        import urllib.parse
        encoded = urllib.parse.quote(search_term)
        return f"https://placehold.co/500x500/143109/AAAE7F?text={encoded}"

    @staticmethod
    async def get_results(platform: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        query_lower = query.lower()
        results = []
        
        # Match query exactly or partially
        matched_key = None
        for key in MockDataEngine.MOCK_DB:
            if key in query_lower or query_lower in key:
                matched_key = key
                break
                
        if matched_key and platform in MockDataEngine.MOCK_DB[matched_key]:
            data = MockDataEngine.MOCK_DB[matched_key][platform]
            for i, item in enumerate(data[:limit]):
                image_url = item["image"]
                results.append({
                    "platform": platform,
                    "platform_product_id": f"{platform.upper()}-{matched_key[:3]}-{i}",
                    "product_url": item["url"],
                    "title": item["title"],
                    "image_url": image_url,
                    "price": item["price"],
                    "star_rating": item["rating"],
                    "review_count": item["reviews"]
                })
        else:
            for i in range(min(limit, 2)):
                title = f"{query.title()} - {platform} Best Seller"
                image_url = await MockDataEngine.extract_exact_image(query) if platform == "Amazon" else "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"
                
                import urllib.parse
                q_enc = urllib.parse.quote(query)
                if platform == "Amazon":
                    domain = f"amazon.com/s?k={q_enc}"
                elif platform == "eBay":
                    domain = f"ebay.com/sch/i.html?_nkw={q_enc}"
                elif platform == "Noon":
                    domain = f"noon.com/uae-en/search/?q={q_enc}"
                else:
                    domain = f"uae.dubizzle.com/search/?keywords={q_enc}"
                    
                results.append({
                    "platform": platform,
                    "platform_product_id": f"GENERIC-{i}",
                    "product_url": f"https://www.{domain}",
                    "title": title,
                    "image_url": image_url,
                    "price": 99.99 + (i * 10),
                    "star_rating": 4.5,
                    "review_count": 100 * (i + 1)
                })
                
        return results
