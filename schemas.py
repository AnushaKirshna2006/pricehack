from pydantic import BaseModel
from typing import Optional

class ProductResponse(BaseModel):
    platform: str
    platform_product_id: str
    product_url: str
    title: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[float] = None
    star_rating: Optional[float] = None
    review_count: Optional[int] = None
