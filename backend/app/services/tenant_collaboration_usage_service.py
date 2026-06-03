from datetime import datetime
from sqlalchemy.orm import Session

from app.models.tenant_collaboration_usage import (
    TenantCollaborationUsage
)

from app.repositories.tenant_collaboration_usage_repo import (
    TenantCollaborationUsageRepo
)


def get_collaboration_usage(
    db: Session,
    tenant_id: int
):
    return (
        TenantCollaborationUsageRepo
        .get_by_tenant(
            db,
            tenant_id
        )
    )


def recalculate_usage(
    db: Session,
    tenant_id: int
):

    workspace_count = (
        TenantCollaborationUsageRepo
        .get_workspace_count(
            db,
            tenant_id
        )
    )

    channel_count = (
        TenantCollaborationUsageRepo
        .get_channel_count(
            db,
            tenant_id
        )
    )

    member_count = (
        TenantCollaborationUsageRepo
        .get_member_count(
            db,
            tenant_id
        )
    )

    usage = (
        TenantCollaborationUsageRepo
        .get_by_tenant(
            db,
            tenant_id
        )
    )

    if not usage:

        usage = TenantCollaborationUsage(
            tenant_id=tenant_id
        )

        usage = (
            TenantCollaborationUsageRepo
            .create(
                db,
                usage
            )
        )

    usage.workspace_count = workspace_count
    usage.channel_count = channel_count
    usage.member_count = member_count

    usage.last_calculated_at = (
        datetime.utcnow()
    )

    return (
        TenantCollaborationUsageRepo
        .save(
            db,
            usage
        )
    )