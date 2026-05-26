from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.audit import (
    AuditLogOut
)

from app.core.dependencies import (
    get_current_user
)

from app.services.audit_service import (
    list_logs_service
)

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


# =====================================================
# LIST AUDIT LOGS
# =====================================================

@router.get(
    "/",
    response_model=list[AuditLogOut]
)
def list_logs(
    db: Session = Depends(get_db),
<<<<<<< HEAD
    user=Depends(get_current_user)
=======
    user = Depends(get_current_user)
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
):

    return list_logs_service(
        db
    )