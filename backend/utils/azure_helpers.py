import os
from functools import lru_cache
from typing import Optional

from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

KV_URL_ENV = "KEY_VAULT_URL"         # e.g. https://my-smartvault.vault.azure.net/
JWT_SECRET_ENV = "JWT_SECRET_KEY"    # local fallback only

@lru_cache(maxsize=1)
def _kv_client() -> Optional[SecretClient]:
    url = os.getenv(KV_URL_ENV, "").strip()
    if not url:
        return None
    # DefaultAzureCredential works locally (Azure CLI login) and in Azure (Managed Identity)
    cred = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
    return SecretClient(vault_url=url, credential=cred)

def get_secret(name: str, fallback_env: Optional[str]=None) -> Optional[str]:
    # 1) Try Key Vault
    client = _kv_client()
    if client:
        try:
            return client.get_secret(name).value
        except Exception:
            pass
    # 2) Fallback to env var (useful for local dev)
    if fallback_env:
        return os.getenv(fallback_env)
    return None
