import sys
from duckduckgo_search import DDGS
import json

def test_ddg():
    query = 'site:dubizzle.com/en/category/ intitle:"iphone" "AED"'
    print(f"Searching DuckDuckGo for: {query}")
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(r)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_ddg()
