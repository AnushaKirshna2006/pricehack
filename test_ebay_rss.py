import httpx

url = "https://www.ebay.com/sch/i.html?_nkw=iphone&_rss=1"
r = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"})
print("Status:", r.status_code)
if r.status_code == 200:
    print(r.text[:1000])
else:
    print(r.text[:500])
