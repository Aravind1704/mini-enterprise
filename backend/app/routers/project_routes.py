from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.core.enterprise_access import (
    require_project_access,
    require_team_access,
    require_workspace_access,
)
from app.models.task import Task
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.schemas.project_team import ProjectTeamCreate, ProjectTeamOut
from app.schemas.project_document import ProjectDocumentOut
from app.services.calendar_service import project_calendar
from app.services.project_document_service import (
    list_project_documents,
    upload_project_document,
)
from app.services.project_service import (
    archive_project,
    create_project,
    delete_project,
    get_project,
    list_projects,
    restore_project,
    update_project,
)
from app.services.project_team_service import (
    assign_team_to_project,
    list_project_teams,
    remove_project_team,
)

router = APIRouter(prefix="/projects", tags=["Projects"])


def _tenant_id(current_user, requested_tenant_id: int | None):
    if requested_tenant_id is not None:
        return requested_tenant_id
    if current_user and current_user.tenant_id is not None:
        return current_user.tenant_id
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="tenant_id is required",
    )


@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def api_create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    workspace = require_workspace_access(db, payload.workspace_id, current_user)
    if payload.tenant_id != workspace.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="tenant_id does not match workspace",
        )
    return create_project(db, payload)


@router.get("/", response_model=list[ProjectOut])
def api_list_projects(
    tenant_id: int | None = None,
    workspace_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    tenant_id = _tenant_id(current_user, tenant_id)
    if workspace_id is not None:
        require_workspace_access(db, workspace_id, current_user)
    return list_projects(db, tenant_id, workspace_id)


@router.get("/{project_id}", response_model=ProjectOut)
def api_get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = require_project_access(db, project_id, current_user)
    return project


@router.put("/{project_id}", response_model=ProjectOut)
def api_update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = require_project_access(db, project_id, current_user)
    return update_project(db, project, payload)


@router.delete("/{project_id}", response_model=ProjectOut)
def api_archive_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = require_project_access(db, project_id, current_user)
    return archive_project(db, project)


@router.patch("/{project_id}/restore", response_model=ProjectOut)
def api_restore_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = require_project_access(db, project_id, current_user)
    return restore_project(db, project)


@router.post("/{project_id}/teams", response_model=ProjectTeamOut, status_code=status.HTTP_201_CREATED)
def api_assign_team_to_project(
    project_id: int,
    payload: ProjectTeamCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = require_project_access(db, project_id, current_user)
    team = require_team_access(db, payload.team_id, current_user)
    if payload.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="project_id does not match path parameter",
        )
    request_payload = payload.model_copy(update={"tenant_id": project.tenant_id})
    try:
        return assign_team_to_project(
            db,
            request_payload.project_id,
            team.id,
            request_payload.tenant_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/{project_id}/teams", response_model=list[ProjectTeamOut])
def api_list_project_teams(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_project_access(db, project_id, current_user)
    return list_project_teams(db, project_id)


@router.delete("/{project_id}/teams/{team_id}")
def api_remove_project_team(
    project_id: int,
    team_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_project_access(db, project_id, current_user)
    require_team_access(db, team_id, current_user)
    try:
        return remove_project_team(db, project_id, team_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/{project_id}/documents", response_model=ProjectDocumentOut, status_code=status.HTTP_201_CREATED)
def api_upload_project_document(
    project_id: int,
    file: UploadFile = File(...),
    uploaded_by: int | None = Form(None),
    document_type: str = Form("OTHER"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = require_project_access(db, project_id, current_user)
    return upload_project_document(
        db,
        project.id,
        file,
        current_user.id,
        project.tenant_id,
        document_type,
    )


@router.get("/{project_id}/documents", response_model=list[ProjectDocumentOut])
def api_list_project_documents(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_project_access(db, project_id, current_user)
    return list_project_documents(db, project_id)


@router.get("/{project_id}/calendar")
def api_project_calendar(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = require_project_access(db, project_id, current_user)
    data = project_calendar(db, project.id)
    return {
        "project_id": project.id,
        "project_name": project.name,
        **data,
    }


@router.get("/{project_id}/workload")
def api_project_workload(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = require_project_access(db, project_id, current_user)
    tasks = (
        db.query(Task)
        .filter(Task.project_id == project.id)
        .all()
    )

    by_team = defaultdict(lambda: {
        "team_id": None,
        "team_name": "Unassigned",
        "total_tasks": 0,
        "completed_tasks": 0,
        "pending_tasks": 0,
        "overdue_tasks": 0,
    })
    by_user = defaultdict(lambda: {
        "user_id": None,
        "user_name": "Unassigned",
        "total_tasks": 0,
        "completed_tasks": 0,
        "pending_tasks": 0,
        "overdue_tasks": 0,
    })

    for task in tasks:
        team_key = task.team_id or 0
        user_key = task.assigned_to_id or 0

        team_row = by_team[team_key]
        team_row["team_id"] = task.team_id
        team_row["team_name"] = task.team.name if task.team else "Unassigned"
        team_row["total_tasks"] += 1
        team_row["completed_tasks"] += 1 if task.status == "DONE" else 0
        team_row["pending_tasks"] += 1 if task.status in {"TODO", "IN_PROGRESS"} else 0
        team_row["overdue_tasks"] += 1 if task.due_date and task.due_date < datetime.utcnow() else 0

        user_row = by_user[user_key]
        user_row["user_id"] = task.assigned_to_id
        user_row["user_name"] = task.assignee.name if task.assignee else "Unassigned"
        user_row["total_tasks"] += 1
        user_row["completed_tasks"] += 1 if task.status == "DONE" else 0
        user_row["pending_tasks"] += 1 if task.status in {"TODO", "IN_PROGRESS"} else 0
        user_row["overdue_tasks"] += 1 if task.due_date and task.due_date < datetime.utcnow() else 0

    return {
        "project_id": project.id,
        "project_name": project.name,
        "total_tasks": len(tasks),
        "by_team": list(by_team.values()),
        "by_user": list(by_user.values()),
    }
