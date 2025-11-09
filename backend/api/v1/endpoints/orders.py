from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.order import OrderCreate, OrderOut
from backend.models.order import Order
from backend.services.servicebus_producer import send_order_event

# ✅ NEW IMPORTS FOR INVOICE

from backend.services.blob_service import upload_local_file

from fastapi import UploadFile, File
from backend.services.blob_service import upload_file_to_container
from backend.services.invoice_service import generate_invoice_pdf

router = APIRouter()   # ✅ NO PREFIX


@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    
    # ✅ Create order directly (single product order)
    new_order = Order(
        product_id=order.product_id,
        quantity=order.quantity,
        warehouse_id=order.warehouse_id
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # ✅ ✅ AUTO-INVOICE GENERATION (ADDED)
    invoice_file = generate_invoice_pdf(
    new_order.order_id,
    new_order.product_id,
    new_order.quantity,
    new_order.warehouse_id
)

    # ✅ Upload generated invoice to Azure Blob Storage
    invoice_url = upload_local_file("invoices", invoice_file)

    # ✅ Save in DB
    new_order.invoice_url = invoice_url
    db.commit()
    db.refresh(new_order)
    # ✅ ✅ END OF NEW CODE

    # ✅ Send correct message to Service Bus
    send_order_event({
        "product_id": new_order.product_id,
        "quantity": new_order.quantity
    })

    return new_order


@router.get("/", response_model=list[OrderOut])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.post("/upload-invoice")
async def upload_invoice(file: UploadFile = File(...)):
    invoice_url = upload_file_to_container("invoices", file)
    return {"invoice_url": invoice_url}
