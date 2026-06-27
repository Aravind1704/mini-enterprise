from datetime import datetime

from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories.project_repo import (
    ProjectRepo
)


def _ensure_project_timestamps(project: Project | None) -> Project | None:
    if not project:
        return project

    now = datetime.utcnow()
    if project.created_at is None:
        project.created_at = now
    if project.updated_at is None:
        project.updated_at = project.created_at or now
    return project


def create_project(
    db: Session,
    payload
):
    project = Project(
        tenant_id=payload.tenant_id,
        workspace_id=payload.workspace_id,
        name=payload.name,
        description=payload.description,
        owner_id=payload.owner_id,
        status=payload.status,
        priority=payload.priority,
        start_date=payload.start_date,
        end_date=payload.end_date,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    return ProjectRepo.create(
        db,
        project
    )


def update_project(
    db: Session,
    project: Project,
    payload
):
    update_data = payload.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(project, key, value)

    project.updated_at = datetime.utcnow()

    return ProjectRepo.save(
        db,
        project
    )


def get_project(
    db: Session,
    project_id: int
):
    return _ensure_project_timestamps(ProjectRepo.get(
        db,
        project_id
    ))


def list_projects(
    db: Session,
    tenant_id: int,
    workspace_id: int | None = None
):
    return [
        _ensure_project_timestamps(project)
        for project in ProjectRepo.list(
            db,
            tenant_id,
            workspace_id
        )
    ]


def delete_project(
    db: Session,
    project_id: int
):
    project = ProjectRepo.get(
        db,
        project_id
    )

    if not project:
        raise ValueError(
            "Project not found"
        )

    ProjectRepo.delete(
        db,
        project
    )

    return {
        "message":
        "Project deleted"
    }


def archive_project(
    db: Session,
    project: Project
):
    project.status = "CANCELLED"
    project.updated_at = datetime.utcnow()

    return ProjectRepo.save(
        db,
        project
    )


def restore_project(
    db: Session,
    project: Project
):
    if project.status == "CANCELLED":
        project.status = "ACTIVE"
    project.updated_at = datetime.utcnow()

    return ProjectRepo.save(
        db,
        project
    )
