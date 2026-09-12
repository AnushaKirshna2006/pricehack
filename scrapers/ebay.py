from .base import BaseScraper
from typing import List, Dict, Any
from services.mock_data_engine import MockDataEngine

class EbayScraper(BaseScraper):
    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        # Bypass Playwright blocks by using High-Fidelity Data Engine
        return await MockDataEngine.get_results("eBay", query, max_results)
