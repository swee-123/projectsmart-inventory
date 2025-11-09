from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    product_id: int
    quantity: int
    warehouse_id: int


class OrderOut(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    warehouse_id: int
    status: str

    # ✅ NEW FIELD
    invoice_url: Optional[str] = None

    class Config:
        orm_mode = True
