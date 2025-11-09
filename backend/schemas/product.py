from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    supplier_id: Optional[int] = None
    image_url: Optional[str] = None
    stock_quantity: int
    warehouse_id: int
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    product_id: int

    class Config:
        orm_mode = True
