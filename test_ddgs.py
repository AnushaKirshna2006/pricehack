from duckduckgo_search import DDGS

try:
    with DDGS() as ddgs:
        results = [r for r in ddgs.text("site:amazon.ae/dp/ coffee", max_results=5)]
        print(results)
except Exception as e:
    print("Error:", e)
