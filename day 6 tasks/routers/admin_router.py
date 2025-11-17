from fastapi import APIRouter, Depends
from dependencies.auth_dependencies import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
def admin_dashboard(admin=Depends(require_role("admin"))):
    return {"message": "Admin-only content"}
