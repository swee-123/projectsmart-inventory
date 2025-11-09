from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.product import Product
from backend.schemas.product import ProductCreate, ProductOut
from backend.services.servicebus_producer import send_order_event
from backend.services.blob_service import upload_file_to_container

# ✅ RBAC dependencies
from backend.api.deps import admin_only, manager_or_admin, get_user


router = APIRouter()


# ✅ Only Admin can create products
@router.post("/", response_model=ProductOut, dependencies=[Depends(admin_only)])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    print("Received product data:", product.dict())

    try:
        # ✅ Create product
        new_product = Product(**product.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        print("✅ Product created successfully")

        # ✅ Send event to Service Bus
        event = {
            "event_type": "product_created",
            "product_id": new_product.product_id,
            "sku": new_product.sku,
            "name": new_product.name,
            "warehouse_id": new_product.warehouse_id,
            "stock_quantity": new_product.stock_quantity,
            "image_url": new_product.image_url
        }

        send_order_event(event)   # ✅ Trigger service bus
        print("Service Bus event sent")

        return new_product

    except Exception as e:
        print("❌ Error creating product:", str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Any authenticated user can read products
@router.get("/", response_model=list[ProductOut], dependencies=[Depends(get_user)])
def get_products(db: Session = Depends(get_db)):
    print("📋 Fetching all products...")
    try:
        products = db.query(Product).all()
        print(f"✅ Found {len(products)} products")
        return products
    except Exception as e:
        print("❌ Error fetching products:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Managers or Admins can upload product images
@router.post("/upload-image", dependencies=[Depends(manager_or_admin)])
async def upload_product_image(file: UploadFile = File(...)):
    url = upload_file_to_container("product-images", file)
    return {"image_url": url}
