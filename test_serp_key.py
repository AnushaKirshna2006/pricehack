import os
from dotenv import load_dotenv
import httpx

load_dotenv(override=True)
api_key = os.getenv("SERPAPI_KEY")
print("Key length:", len(api_key) if api_key else "None")

url = "https://serpapi.com/search.json"
params = {"engine": "ebay", "_nkw": "coffee", "api_key": api_key}
r = httpx.get(url, params=params)
print("Ebay Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    print("Ebay results:", len(data.get("organic_results", [])))
else:
    print(r.text[:500])

params = {"engine": "google", "q": "site:dubizzle.com intitle:coffee \"AED\"", "api_key": api_key}
r = httpx.get(url, params=params)
print("Dubizzle Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    print("Dubizzle results:", len(data.get("organic_results", [])))

