from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.approval import (
    ApprovalOut
)

from app.core.dependencies import (
    get_current_user
)

from app.services.approval_service import (
    list_approvals_service
)

router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"]
)


# =====================================================
# LIST APPROVALS
# =====================================================

@router.get(
    "/",
    response_model=list[ApprovalOut]
)
def list_approvals(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return list_approvals_service(
        db,
        user
    )