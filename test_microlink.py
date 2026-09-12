import httpx
import asyncio

async def test_microlink():
    url = "https://www.ebay.com/itm/325778841753" # random ebay item
    api_url = f"https://api.microlink.io/?url={url}"
    async with httpx.AsyncClient() as client:
        r = await client.get(api_url, timeout=10.0)
        data = r.json()
        print(data.get("data", {}).get("image", {}).get("url"))

if __name__ == "__main__":
    asyncio.run(test_microlink())
