from fastapi import Depends
from typing import Dict, Any

# ✅ Import JWT validation + RBAC helper
from backend.utils.security import get_current_user, require_role


# ✅ Type alias for cleaner code
CurrentUser = Dict[str, Any]


# ✅ Returns the authenticated user (claims)
def get_user(claims: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    return claims


# ✅ RBAC role guards
admin_only = require_role("Admin")
manager_or_admin = require_role("Manager", "Admin")
staff_or_above = require_role("Staff", "Manager", "Admin")
