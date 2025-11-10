from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func
from backend.database import Base

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # only essential fields
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    warehouse_id = Column(Integer, nullable=False)

    status = Column(String(40), default="created")

    # ✅ NEW FIELD
    invoice_url = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
#swe