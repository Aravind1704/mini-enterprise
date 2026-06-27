from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import case, func

from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.core.enterprise_access import (
    require_team_access,
    require_workspace_access,
)
from app.schemas.team import TeamCreate, TeamOut, TeamUpdate
from app.schemas.team_member import TeamMemberCreate, TeamMemberOut
from app.services.team_service import (
    archive_team,
    create_team,
    delete_team,
    get_team,
    list_teams,
    restore_team,
    update_team,
)
from app.services.team_member_service import (
    add_team_member,
    list_team_members,
    remove_team_member,
)
from app.models.task import Task
from app.models.user import User
from app.services.workload_dashboard_service import team_workload

router = APIRouter(prefix="/teams", tags=["Teams"])


def _tenant_id(current_user, requested_tenant_id: int | None):
    if requested_tenant_id is not None:
        return requested_tenant_id
    if current_user and current_user.tenant_id is not None:
        return current_user.tenant_id
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="tenant_id is required",
    )


@router.post("/", response_model=TeamOut, status_code=status.HTTP_201_CREATED)
def api_create_team(
    payload: TeamCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    workspace = require_workspace_access(db, payload.workspace_id, current_user)
    if payload.tenant_id != workspace.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="tenant_id does not match workspace",
        )

    request_payload = payload.model_copy(update={"created_by": current_user.id})
    return create_team(db, request_payload)


@router.get("/", response_model=list[TeamOut])
def api_list_teams(
    tenant_id: int | None = None,
    workspace_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    tenant_id = _tenant_id(current_user, tenant_id)
    if workspace_id is not None:
        require_workspace_access(db, workspace_id, current_user)
    return list_teams(db, tenant_id, workspace_id)


@router.get("/{team_id}", response_model=TeamOut)
def api_get_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    team = require_team_access(db, team_id, current_user)
    return team


@router.put("/{team_id}", response_model=TeamOut)
def api_update_team(
    team_id: int,
    payload: TeamUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    team = require_team_access(db, team_id, current_user)
    return update_team(db, team, payload)


@router.delete("/{team_id}", response_model=TeamOut)
def api_archive_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    team = require_team_access(db, team_id, current_user)
    return archive_team(db, team)


@router.patch("/{team_id}/restore", response_model=TeamOut)
def api_restore_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    team = require_team_access(db, team_id, current_user)
    return restore_team(db, team)


@router.post("/{team_id}/members", response_model=TeamMemberOut, status_code=status.HTTP_201_CREATED)
def api_add_team_member(
    team_id: int,
    payload: TeamMemberCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    team = require_team_access(db, team_id, current_user)
    if payload.team_id != team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="team_id does not match path parameter",
        )
    request_payload = payload.model_copy(
        update={"tenant_id": team.tenant_id}
    )
    try:
        return add_team_member(
            db,
            team_id,
            request_payload.user_id,
            request_payload.role,
            request_payload.tenant_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/{team_id}/members", response_model=list[TeamMemberOut])
def api_list_team_members(
    team_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_team_access(db, team_id, current_user)
    return list_team_members(db, team_id)


@router.delete("/{team_id}/members/{user_id}")
def api_remove_team_member(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_team_access(db, team_id, current_user)
    try:
        return remove_team_member(db, team_id, user_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/{team_id}/workload")
def api_team_workload(
    team_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    team = require_team_access(db, team_id, current_user)
    rows = team_workload(db)
    match = next((row for row in rows if row["team_id"] == team.id), None)

    user_rows = (
        db.query(
            Task.assigned_to_id,
            func.count(Task.id),
            func.sum(case((Task.status == "DONE", 1), else_=0)),
            func.sum(case((Task.status.in_(["TODO", "IN_PROGRESS"]), 1), else_=0)),
            func.sum(case((Task.due_date < datetime.utcnow(), 1), else_=0)),
        )
        .filter(Task.team_id == team.id)
        .group_by(Task.assigned_to_id)
        .all()
    )

    by_user = []
    for user_id, total, completed, pending, overdue in user_rows:
        user = db.query(User).filter(User.id == user_id).first() if user_id else None
        by_user.append(
            {
                "user_id": user_id,
                "user_name": user.name if user else "Unassigned",
                "total_tasks": int(total or 0),
                "completed_tasks": int(completed or 0),
                "pending_tasks": int(pending or 0),
                "overdue_tasks": int(overdue or 0),
            }
        )

    return {
        "team_id": team.id,
        "team_name": team.name,
        "workload": match or {
            "team_id": team.id,
            "team_name": team.name,
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "overdue_tasks": 0,
        },
        "by_user": by_user,
    }
