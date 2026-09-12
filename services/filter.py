from typing import List, Dict, Any

class FilterService:
    @staticmethod
    def filter_best_results(products: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Takes a list of raw products from multiple scrapers and returns the best results.
        Currently sorts by a simple heuristic: highest rating, then lowest price.
        """
        
        # Group products by platform
        platform_groups = {}
        for p in products:
            plat = p.get("platform")
            if plat not in platform_groups:
                platform_groups[plat] = []
            platform_groups[plat].append(p)
            
        final_results = []
        
        # 1. Guarantee at least 1 from each platform (the most relevant one)
        for plat, items in platform_groups.items():
            if items:
                final_results.append(items.pop(0))
                
        # 2. Fill the rest by interleaving from platforms to maintain relevance order
        target_limit = max(limit, 9)
        
        while len(final_results) < target_limit:
            added = False
            for plat, items in platform_groups.items():
                if items and len(final_results) < target_limit:
                    final_results.append(items.pop(0))
                    added = True
            if not added:
                break
                
        return final_results
