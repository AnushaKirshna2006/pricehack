import requests

def test():
    r = requests.post("http://127.0.0.1:8000/api/search", json={"query": "coffee machine", "limit": 5})
    print(r.status_code)
    try:
        data = r.json()
        print(f"Got {len(data)} results!")
        for item in data[:3]:
            print(item['title'])
            print(f"Platform: {item['platform']}, Price: {item['price']}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test()
