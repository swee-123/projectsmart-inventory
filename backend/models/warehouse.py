from sqlalchemy import Column, Integer, String
from backend.database import Base

class Warehouse(Base):
    __tablename__ = "warehouses"

    warehouse_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    location = Column(String(255), nullable=True)
