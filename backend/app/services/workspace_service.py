from sqlalchemy.orm import Session
from slugify import slugify

from app.models.workspace import Workspace
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceUpdate
)

from app.repositories.workspace_repo import (
    WorkspaceRepo
)


def create_workspace(
    db: Session,
    payload: WorkspaceCreate,
    created_by: int
):

    workspace = Workspace(
        tenant_id=payload.tenant_id,
        name=payload.name,
        slug=slugify(payload.name),
        description=payload.description,
        avatar_url=payload.avatar_url,
        visibility=payload.visibility,
        created_by=created_by
    )

    return WorkspaceRepo.create(
        db,
        workspace
    )


def list_workspaces(
    db: Session,
    tenant_id: int
):
    return WorkspaceRepo.list_by_tenant(
        db,
        tenant_id
    )


def get_workspace(
    db: Session,
    workspace_id: int
):
    return WorkspaceRepo.get(
        db,
        workspace_id
    )


def update_workspace(
    db: Session,
    workspace: Workspace,
    payload: WorkspaceUpdate
):

    update_data = payload.model_dump(
        exclude_unset=True
    )

    if "name" in update_data:
        update_data["slug"] = slugify(
            update_data["name"]
        )

    for key, value in update_data.items():

        setattr(
            workspace,
            key,
            value
        )

    return WorkspaceRepo.save(
        db,
        workspace
    )


def archive_workspace(
    db: Session,
    workspace: Workspace
):

    workspace.status = "ARCHIVED"

    return WorkspaceRepo.save(
        db,
        workspace
    )


def restore_workspace(
    db: Session,
    workspace: Workspace
):

    workspace.status = "ACTIVE"

    return WorkspaceRepo.save(
        db,
        workspace
    )