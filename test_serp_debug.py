import os
import requests

api_key = None
with open(".env", "r") as f:
    for line in f:
        if line.startswith("SERPAPI_KEY="):
            api_key = line.strip().split("=")[1].strip('"\'')
            break
print("Key:", api_key)

url = "https://serpapi.com/search.json"
params = {"engine": "google", "q": "site:amazon.ae/dp/ coffee", "api_key": api_key, "gl": "ae", "num": 1}
r = requests.get(url, params=params)
print("Status:", r.status_code)
print("Response:", r.text[:500])
