import requests
from bs4 import BeautifulSoup

def test_dubizzle():
    print("Testing Dubizzle...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    r = requests.get('https://uae.dubizzle.com/search/?keywords=coffee', headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Just dump some img tags
    imgs = soup.find_all('img')
    print(f"Dubizzle returned {len(imgs)} images.")
    for img in imgs[:5]:
        print(img.get('src'))

def test_noon():
    print("\nTesting Noon...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    r = requests.get('https://www.noon.com/uae-en/search/?q=coffee', headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    imgs = soup.find_all('img')
    print(f"Noon returned {len(imgs)} images.")
    for img in imgs[:5]:
        print(img.get('src'))

if __name__ == '__main__':
    test_dubizzle()
    test_noon()
