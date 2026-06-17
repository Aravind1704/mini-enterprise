from sqlalchemy.orm import Session
from app.models.workspace import Workspace
from app.core.slug import make_slug
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceUpdate
)

from app.repositories.workspace_repo import (
    WorkspaceRepo
)

from app.services.tenant_collaboration_settings_service import (
    get_collaboration_settings,
    create_default_settings,
    validate_workspace_limit,
    check_workspace_enabled
)

from app.repositories.tenant_collaboration_usage_repo import (
    TenantCollaborationUsageRepo
)


def create_workspace(
    db: Session,
    payload: WorkspaceCreate,
    created_by: int
):

    # ensure collaboration settings exist for tenant
    settings = get_collaboration_settings(
        db,
        payload.tenant_id
    )

    if not settings:
        settings = create_default_settings(
            db,
            payload.tenant_id
        )

    # check feature enabled
    check_workspace_enabled(settings)

    # enforce workspace limit
    current_count = (
        TenantCollaborationUsageRepo.get_workspace_count(
            db,
            payload.tenant_id
        )
    )

    validate_workspace_limit(
        settings,
        current_count
    )

    workspace = Workspace(
        tenant_id=payload.tenant_id,
        name=payload.name,
        slug=make_slug(payload.name),
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
    tenant_id: int | None = None
):
    if tenant_id is None:
        return WorkspaceRepo.list_all(db)

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
        update_data["slug"] = make_slug(
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

    workspace.is_archived = True

    return WorkspaceRepo.save(
        db,
        workspace
    )


def restore_workspace(
    db: Session,
    workspace: Workspace
):

    workspace.is_archived = False

    return WorkspaceRepo.save(
        db,
        workspace
    )
