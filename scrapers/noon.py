from .base import BaseScraper
from typing import List, Dict, Any
from services.mock_data_engine import MockDataEngine

class NoonScraper(BaseScraper):
    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        return await MockDataEngine.get_results("Noon", query, max_results)
