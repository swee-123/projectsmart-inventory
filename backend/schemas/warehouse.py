from pydantic import BaseModel

class WarehouseBase(BaseModel):
    name: str
    location: str | None = None

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseOut(WarehouseBase):
    warehouse_id: int

    class Config:
        orm_mode = True
