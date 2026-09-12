import requests
import xml.etree.ElementTree as ET

r = requests.get('https://www.ebay.com/sch/i.html?_nkw=iphone+15&_rss=1', headers={'User-Agent': 'Mozilla/5.0'})
print(r.status_code)
try:
    root = ET.fromstring(r.text)
    for item in root.findall('.//item')[:3]:
        title = item.find('title').text
        link = item.find('link').text
        print(title, link)
except Exception as e:
    print("Error parsing XML", e)
