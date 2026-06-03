# app/routes/workspace_member_routes.py

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from typing import List

from app.database import get_db

from app.schemas.workspace_member import (
    WorkspaceMemberCreate,
    WorkspaceMemberUpdateRole,
    WorkspaceMemberOut
)

from app.services.workspace_member_service import (
    add_workspace_member,
    list_workspace_members,
    update_member_role,
    remove_workspace_member
)

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspace Members"]
)


# =========================================
# ADD MEMBER
# =========================================

@router.post(
    "/{workspace_id}/members",
    response_model=WorkspaceMemberOut,
    status_code=status.HTTP_201_CREATED
)
def api_add_member(
    workspace_id: int,
    payload: WorkspaceMemberCreate,
    db: Session = Depends(get_db)
):

    try:

        return add_workspace_member(
            db=db,
            workspace_id=workspace_id,
            user_id=payload.user_id,
            role=payload.role
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================================
# LIST MEMBERS
# =========================================

@router.get(
    "/{workspace_id}/members",
    response_model=List[WorkspaceMemberOut]
)
def api_list_members(
    workspace_id: int,
    db: Session = Depends(get_db)
):

    return list_workspace_members(
        db,
        workspace_id
    )


# =========================================
# UPDATE MEMBER ROLE
# =========================================

@router.patch(
    "/{workspace_id}/members/{user_id}/role",
    response_model=WorkspaceMemberOut
)
def api_update_role(
    workspace_id: int,
    user_id: int,
    payload: WorkspaceMemberUpdateRole,
    db: Session = Depends(get_db)
):

    member = update_member_role(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id,
        role=payload.role
    )

    if not member:

        raise HTTPException(
            status_code=404,
            detail="Workspace member not found"
        )

    return member


# =========================================
# REMOVE MEMBER
# =========================================

@router.delete(
    "/{workspace_id}/members/{user_id}"
)
def api_remove_member(
    workspace_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    success = remove_workspace_member(
        db=db,
        workspace_id=workspace_id,
        user_id=user_id
    )

    if not success:

        raise HTTPException(
            status_code=404,
            detail="Workspace member not found"
        )

    return {
        "message":
        "Member removed successfully"
    }