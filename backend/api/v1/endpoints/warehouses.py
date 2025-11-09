from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.warehouse import Warehouse
from backend.schemas.warehouse import WarehouseCreate, WarehouseOut

router = APIRouter()   # ✅ NO PREFIX

@router.post("/", response_model=WarehouseOut)
def create_warehouse(warehouse: WarehouseCreate, db: Session = Depends(get_db)):
    new_wh = Warehouse(**warehouse.dict())
    db.add(new_wh)
    db.commit()
    db.refresh(new_wh)
    return new_wh


@router.get("/", response_model=list[WarehouseOut])
def get_warehouses(db: Session = Depends(get_db)):
    return db.query(Warehouse).all()
