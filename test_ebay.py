import requests
r = requests.get('https://www.ebay.com/sch/i.html?_nkw=iphone+15', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
with open('ebay.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
