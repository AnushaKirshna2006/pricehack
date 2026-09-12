from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseScraper(ABC):
    """
    Abstract base class for all platform scrapers.
    """
    
    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search the platform for a given query and return a list of product dictionaries.
        """
        pass
