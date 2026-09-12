import os
import requests

api_key = None
with open(".env", "r") as f:
    for line in f:
        if line.startswith("SERPAPI_KEY="):
            api_key = line.strip().split("=")[1].strip('"\'')
            break
print("Current Key:", api_key)

url = "https://serpapi.com/search.json"
params = {"engine": "google", "q": "test", "api_key": api_key, "num": 1}
r = requests.get(url, params=params)
print("Status:", r.status_code)
if r.status_code != 200:
    print(r.text)
