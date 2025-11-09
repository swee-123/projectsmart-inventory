import os
from dotenv import load_dotenv

# Load .env file during local development
load_dotenv()

def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

class Settings:
    # App metadata
    APP_NAME: str = _env("APP_NAME", "smart-inventory-api")

    # JWT Settings
    JWT_AUDIENCE: str = _env("JWT_AUDIENCE", "smart-inventory-clients")

    # Key Vault URL (optional in local)
    KEY_VAULT_URL: str = _env("KEY_VAULT_URL", "")

settings = Settings()
