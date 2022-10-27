from pydantic import BaseModel
from typing import Optional, List


class ProductSchema(BaseModel):
    market: str
    url: str
    store_id: int
    category: str
    name: str
    color: str
    description: Optional[str]
    image: str


class PriceSchema(BaseModel):
    price: int
    product_id: Optional[int]
    discount: str = '0'
