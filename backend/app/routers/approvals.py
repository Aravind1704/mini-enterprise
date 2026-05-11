from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db

from app.models.approval import (
    Approval,
    ApprovalHistory
)

from app.models.user import User

from app.schemas.approval import (
    ApprovalCreate,
    ApprovalAction,
    ApprovalOut,
    ApprovalHistoryOut
)

from app.core.dependencies import (
    get_current_user,
    require_role
)

from app.services.notification_service import (
    notify_approval_requested
)

router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"]
)


@router.post(
    "/",
    response_model=ApprovalOut
)
def submit_approval(
    data: ApprovalCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    approval = Approval(
        title=data.title,
        description=data.description,
        requested_by=current_user.id
    )

    db.add(approval)

    db.commit()

    db.refresh(approval)


    stmt = (
        select(User)
        .where(User.role == "manager")
    )

    result = db.execute(stmt)

    manager = result.scalar_one_or_none()

    

    if not manager:

        stmt = (
            select(User)
            .where(User.role == "admin")
        )

        result = db.execute(stmt)

        manager = result.scalar_one_or_none()

   

    if manager:

        notify_approval_requested(
            approval_id=approval.id,
            approver_id=manager.id,
            requester_name=current_user.name,
            db=db
        )

    return approval



@router.get(
    "/",
    response_model=list[ApprovalOut]
)
def list_approvals(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    stmt = select(Approval)

    

    if current_user.role == "manager":

        stmt = stmt.where(
            Approval.current_level == "manager"
        )



    elif current_user.role != "admin":

        stmt = stmt.where(
            Approval.requested_by == current_user.id
        )

    result = db.execute(stmt)

    approvals = result.scalars().all()

    return approvals


@router.patch(
    "/{id}/action",
    response_model=ApprovalOut
)
def action_approval(
    id: int,
    data: ApprovalAction,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("admin", "manager")
    )
):

    stmt = (
        select(Approval)
        .where(Approval.id == id)
    )

    result = db.execute(stmt)

    approval = result.scalar_one_or_none()

    if not approval:

        raise HTTPException(
            status_code=404,
            detail="Approval not found"
        )

    
    if (
        data.action == "rejected"
        and not data.comment
    ):

        raise HTTPException(
            status_code=400,
            detail="Comment required"
        )

    approval.status = data.action

    

    history = ApprovalHistory(
        approval_id=id,
        action_by=current_user.id,
        action=data.action,
        comment=data.comment
    )

    db.add(history)

    db.commit()

    db.refresh(approval)

    return approval




@router.get(
    "/{id}/history",
    response_model=list[ApprovalHistoryOut]
)
def approval_history(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    stmt = (
        select(ApprovalHistory)
        .where(
            ApprovalHistory.approval_id == id
        )
    )

    result = db.execute(stmt)

    history = result.scalars().all()

    return history
