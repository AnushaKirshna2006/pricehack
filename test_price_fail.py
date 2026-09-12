import os
import asyncio
import httpx
import json
from dotenv import load_dotenv
import re

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")

def extract(item):
    try:
        price = item.get("rich_snippet", {}).get("top", {}).get("detected_extensions", {}).get("price")
        if price is not None: return float(price), "rich_snippet_top"
    except: pass
    try:
        price = item.get("rich_snippet", {}).get("bottom", {}).get("detected_extensions", {}).get("price")
        if price is not None: return float(price), "rich_snippet_bottom"
    except: pass
    text = str(item.get("snippet", "")) + " " + str(item.get("title", ""))
    match = re.search(r"(?:AED|AED\s+|AED\.|د\.إ|\$)\s*([0-9,]+\.?[0-9]*)", text, re.IGNORECASE)
    if match: return float(match.group(1).replace(",", "")), "regex1"
    
    match2 = re.search(r"([0-9,]+\.?[0-9]*)\s*(?:AED|Dhs|د\.إ)", text, re.IGNORECASE)
    if match2: return float(match2.group(1).replace(",", "")), "regex2"
    return None, "FAILED"

async def test_search():
    query = "laptop"
    async with httpx.AsyncClient() as client:
        print("--- NOON ---")
        params = {"engine": "google", "q": f"site:noon.com/uae-en/ {query}", "api_key": api_key, "gl": "ae"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=20.0)
        for item in r.json().get("organic_results", [])[:10]:
            print(f"{item.get('title')}")
            val, method = extract(item)
            print(f"Price: {val} (via {method})")
            if method == "FAILED":
                print(f"  Snippet: {item.get('snippet')}")
                
        print("\n--- DUBIZZLE ---")
        params = {"engine": "google", "q": f"site:dubizzle.com {query}", "api_key": api_key, "gl": "ae"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=20.0)
        for item in r.json().get("organic_results", [])[:10]:
            if "dubai.dubizzle.com/classified" not in item.get("link","") and "uae.dubizzle.com/classified" not in item.get("link",""): continue
            print(f"{item.get('title')}")
            val, method = extract(item)
            print(f"Price: {val} (via {method})")
            if method == "FAILED":
                print(f"  Snippet: {item.get('snippet')}")
                
        print("\n--- AMAZON ---")
        params = {"engine": "google", "q": f"site:amazon.ae/dp/ OR site:amazon.com/dp/ {query}", "api_key": api_key, "gl": "ae"}
        r = await client.get("https://serpapi.com/search.json", params=params, timeout=20.0)
        for item in r.json().get("organic_results", [])[:10]:
            print(f"{item.get('title')}")
            val, method = extract(item)
            print(f"Price: {val} (via {method})")
            if method == "FAILED":
                print(f"  Snippet: {item.get('snippet')}")

if __name__ == "__main__":
    asyncio.run(test_search())
