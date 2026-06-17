from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.tenant import Tenant
from app.models.workspace import Workspace
from app.models.channel import Channel
from app.models.user import User

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db)
):

    tenants = db.query(func.count(Tenant.id)).scalar()

    workspaces = db.query(
        func.count(Workspace.id)
    ).scalar()

    channels = db.query(
        func.count(Channel.id)
    ).scalar()

    users = db.query(
        func.count(User.id)
    ).scalar()

    return {
        "tenants": tenants,
        "workspaces": workspaces,
        "channels": channels,
        "users": users
    }