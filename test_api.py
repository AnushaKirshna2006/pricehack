import httpx
r = httpx.post("http://127.0.0.1:8000/api/search", json={"query": "coffee machine", "limit": 2}, timeout=20.0)
print(r.json())
