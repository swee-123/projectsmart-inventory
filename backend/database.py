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

# ✅ Optional: SSL CA (only if your MySQL needs it)
SSL_CA_PATH = os.environ.get("SSL_CA_PATH")

# --------------------------------------------------
# ✅ Build MySQL URL with URL-encoded password
# --------------------------------------------------
if SSL_CA_PATH:
    DATABASE_URL = (
        f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl_ca={SSL_CA_PATH}"
    )
else:
    DATABASE_URL = (
        f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# --------------------------------------------------
# ✅ SQLAlchemy engine + session
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

# deploy 5

