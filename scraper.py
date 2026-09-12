import requests
from bs4 import BeautifulSoup
import json
import argparse
import random
import time

def get_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US, en;q=0.5",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

def extract_text(soup, selector, is_id=True):
    try:
        if is_id:
            element = soup.find(id=selector)
        else:
            element = soup.select_one(selector)
        return element.text.strip() if element else None
    except Exception:
        return None

def scrape_amazon_product(url):
    print(f"Scraping URL: {url}")
    headers = get_headers()
    
    # Adding a small random delay to mimic human behavior
    time.sleep(random.uniform(1.0, 3.0))
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Check for CAPTCHA
    if "api-services-support@amazon.com" in soup.text or "Enter the characters you see below" in soup.text:
        print("Warning: Amazon blocked the request with a CAPTCHA. Try again later or use a proxy/VPN.")
        return None

    product_data = {
        "url": url,
        "title": extract_text(soup, "productTitle"),
        "price": extract_text(soup, "corePrice_feature_div") or extract_text(soup, "priceblock_ourprice") or extract_text(soup, "priceblock_dealprice"),
        "rating": extract_text(soup, "acrPopover", is_id=False),
        "review_count": extract_text(soup, "acrCustomerReviewText"),
        "availability": extract_text(soup, "availability")
    }

    # Clean up price and rating if they exist
    if product_data["price"]:
        # Remove extra whitespace/newlines that often come with the price block
        product_data["price"] = " ".join(product_data["price"].split())
    if product_data["rating"]:
        product_data["rating"] = product_data["rating"].split(" out of")[0].strip()
    if product_data["review_count"]:
        product_data["review_count"] = product_data["review_count"].split(" ratings")[0].strip()
    if product_data["availability"]:
         product_data["availability"] = " ".join(product_data["availability"].split())


    return product_data

def main():
    parser = argparse.ArgumentParser(description="Scrape Amazon Product Data")
    parser.add_argument("url", help="The Amazon product URL to scrape")
    parser.add_argument("-o", "--output", help="Output JSON file name (default: product_data.json)", default="product_data.json")
    
    args = parser.parse_args()
    
    data = scrape_amazon_product(args.url)
    
    if data:
        print("\n--- Extracted Data ---")
        for key, value in data.items():
            print(f"{key.capitalize()}: {value}")
            
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\nData saved to {args.output}")
    else:
        print("\nFailed to extract data.")

if __name__ == "__main__":
    main()
