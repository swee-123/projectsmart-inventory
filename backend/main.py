from fastapi import FastAPI
from dotenv import load_dotenv
import os

# ✅ Import DB engine + Base
from backend.database import engine, Base

# ✅ Import all models so SQLAlchemy knows them
from backend.models.product import Product
from backend.models.warehouse import Warehouse
from backend.models.order import Order
from backend.models.user import User  # ✅ Add user model

# ✅ Import routers
from backend.api.v1.endpoints import products, warehouses, orders
from backend.api.v1.endpoints import auth  # ✅ Add auth router


# ✅ Load .env file
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# ✅ Auto-create tables (only for development)
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")

# ✅ FastAPI App
app = FastAPI(
    title="Smart Inventory API",
    version="1.0.0"
)

# ✅ Root endpoint
@app.get("/")
def root():
    print(" Root endpoint called")
    return {"message": "Smart Inventory API running!", "status": "ok"}

# ✅ Health endpoint
@app.get("/health")
def health():
    print("💚 Health check called")
    return {"status": "healthy"}

# ✅ Register Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])   # ✅ Added
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(warehouses.router, prefix="/api/v1/warehouses", tags=["Warehouses"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
