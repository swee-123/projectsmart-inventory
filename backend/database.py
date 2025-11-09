import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus  # ✅ ADD THIS IMPORT

# --------------------------------------------------
# ✅ Correct .env path (project root)
# backend/database.py → backend/ → go up 1 level
# --------------------------------------------------
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

print("🔍 Looking for .env at:", ENV_PATH)

if not ENV_PATH.exists():
    raise RuntimeError(f"❌ .env file not found at: {ENV_PATH}")

load_dotenv(ENV_PATH)

# --------------------------------------------------
# ✅ Load DB values
# --------------------------------------------------
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
SSL_CA_PATH = os.getenv("SSL_CA_PATH")

# --------------------------------------------------
# ✅ Validate required values
# --------------------------------------------------
missing = [k for k, v in {
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_NAME": DB_NAME,
    "SSL_CA_PATH": SSL_CA_PATH,
}.items() if not v]

if missing:
    raise RuntimeError(f"❌ Missing DB values in .env → {missing}")

# --------------------------------------------------
# ✅ Build MySQL URL with URL-encoded password
# --------------------------------------------------
DB_URL = (
    f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?ssl_ca={SSL_CA_PATH}"
)

print("✅ Using DB URL:", DB_URL)

engine = create_engine(DB_URL)

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