from sqlalchemy import Column, Integer, String, DECIMAL
from backend.database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sku = Column(String(40), unique=True, nullable=False)
    name = Column(String(120), nullable=False)
    description = Column(String(255))
    category = Column(String(80))
    price = Column(DECIMAL(10,2), nullable=False)
    supplier_id = Column(Integer)
    image_url = Column(String(255))
    stock_quantity = Column(Integer, nullable=False)
    warehouse_id = Column(Integer, nullable=False)
    image_url = Column(String(500), nullable=True)

