import asyncio
import os
import httpx
from services.live_data_engine import LiveDataEngine
from dotenv import load_dotenv

load_dotenv()

async def test():
    print("Testing image extraction...")
    img = await LiveDataEngine.extract_exact_image("Ninja Luxe Cafe Premier Series")
    print(f"Extracted image: {img}")

if __name__ == "__main__":
    asyncio.run(test())
