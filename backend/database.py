import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

# --------------------------------------------------
# ✅ Load DB values from Azure App Settings
# --------------------------------------------------
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]

# --------------------------------------------------
# ✅ Build MySQL URL (SSL must be enabled for Azure)
# --------------------------------------------------
# Azure requires ssl=true for secure MySQL connections
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl=true"
)

# --------------------------------------------------
# ✅ SQLAlchemy Engine — FIXES "MySQL server has gone away"
# --------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,     # ✅ Checks stale connections automatically
    pool_recycle=280,       # ✅ Recycle before Azure kills idle connections
    pool_timeout=30,        # ✅ Prevents hanging connections
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

# --------------------------------------------------
# ✅ FastAPI dependency
# --------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
