from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from services.live_data_engine import LiveDataEngine
from services.mock_data_engine import MockDataEngine
from services.filter import FilterService
from schemas import ProductResponse
import asyncio

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

@router.post("/api/search", response_model=List[ProductResponse])
async def search_products(request: SearchRequest):
    """
    Returns filtered best results. Always uses LiveDataEngine to ensure 
    real-time, accurate pricing.
    """
    query_key = request.query.lower().strip()
    
    # 1. Use LiveDataEngine for accurate, real-world data
    results = await LiveDataEngine.search_all(request.query, limit=request.limit * 2)

    # 2. Filter for the best results (e.g. sorted by price/rating)
    best_results = FilterService.filter_best_results(results, limit=request.limit)

    return best_results
