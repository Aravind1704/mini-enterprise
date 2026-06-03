# app/routes/workspace_routes.py

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from typing import List

from app.database import get_db

from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceUpdate,
    WorkspaceOut
)

from app.services.workspace_service import (
    create_workspace,
    list_workspaces,
    get_workspace,
    update_workspace,
    archive_workspace,
    restore_workspace
)

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspace Management"]
)


# =========================================
# CREATE WORKSPACE
# =========================================

@router.post(
    "/",
    response_model=WorkspaceOut,
    status_code=status.HTTP_201_CREATED
)
def api_create_workspace(
    payload: WorkspaceCreate,
    db: Session = Depends(get_db)
):

    try:

        return create_workspace(
            db,
            payload,
            payload.created_by
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================================
# LIST WORKSPACES
# =========================================

@router.get(
    "/",
    response_model=List[WorkspaceOut]
)
def api_list_workspaces(
    tenant_id: int,
    db: Session = Depends(get_db)
):

    return list_workspaces(
        db,
        tenant_id
    )


# =========================================
# GET WORKSPACE DETAILS
# =========================================

@router.get(
    "/{workspace_id}",
    response_model=WorkspaceOut
)
def api_get_workspace(
    workspace_id: int,
    db: Session = Depends(get_db)
):

    workspace = get_workspace(
        db,
        workspace_id
    )

    if not workspace:

        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return workspace


# =========================================
# UPDATE WORKSPACE
# =========================================

@router.put(
    "/{workspace_id}",
    response_model=WorkspaceOut
)
def api_update_workspace(
    workspace_id: int,
    payload: WorkspaceUpdate,
    db: Session = Depends(get_db)
):

    workspace = get_workspace(
        db,
        workspace_id
    )

    if not workspace:

        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return update_workspace(
        db,
        workspace,
        payload
    )


# =========================================
# ARCHIVE WORKSPACE
# =========================================

@router.patch(
    "/{workspace_id}/archive",
    response_model=WorkspaceOut
)
def api_archive_workspace(
    workspace_id: int,
    db: Session = Depends(get_db)
):

    workspace = get_workspace(
        db,
        workspace_id
    )

    if not workspace:

        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return archive_workspace(
        db,
        workspace
    )


# =========================================
# RESTORE WORKSPACE
# =========================================

@router.patch(
    "/{workspace_id}/restore",
    response_model=WorkspaceOut
)
def api_restore_workspace(
    workspace_id: int,
    db: Session = Depends(get_db)
):

    workspace = get_workspace(
        db,
        workspace_id
    )

    if not workspace:

        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return restore_workspace(
        db,
        workspace
    )