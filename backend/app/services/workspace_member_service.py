# app/services/workspace_member_service.py

from sqlalchemy.orm import Session

from app.models.workspace_member import (
    WorkspaceMember
)

from app.repositories.workspace_member_repo import (
    WorkspaceMemberRepo
)


# =========================================
# ADD MEMBER
# =========================================

def add_workspace_member(
    db: Session,
    workspace_id: int,
    user_id: int,
    role: str
):

    existing = (
        WorkspaceMemberRepo
        .get_member(
            db,
            workspace_id,
            user_id
        )
    )

    if existing:

        raise ValueError(
            "User already exists in workspace"
        )

    member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=user_id,
        role=role,
        is_active=True
    )

    return (
        WorkspaceMemberRepo
        .create(
            db,
            member
        )
    )


# =========================================
# LIST MEMBERS
# =========================================

def list_workspace_members(
    db: Session,
    workspace_id: int
):

    return (
        WorkspaceMemberRepo
        .list_members(
            db,
            workspace_id
        )
    )


# =========================================
# SEARCH MEMBER
# =========================================

def search_workspace_member(
    db: Session,
    workspace_id: int,
    user_id: int
):

    return (
        WorkspaceMemberRepo
        .get_member(
            db,
            workspace_id,
            user_id
        )
    )


# =========================================
# UPDATE ROLE
# =========================================

def update_member_role(
    db: Session,
    workspace_id: int,
    user_id: int,
    role: str
):

    member = (
        WorkspaceMemberRepo
        .get_member(
            db,
            workspace_id,
            user_id
        )
    )

    if not member:

        raise ValueError(
            "Member not found"
        )

    member.role = role

    return (
        WorkspaceMemberRepo
        .save(
            db,
            member
        )
    )


# =========================================
# REMOVE MEMBER
# =========================================

def remove_workspace_member(
    db: Session,
    workspace_id: int,
    user_id: int
):

    member = (
        WorkspaceMemberRepo
        .get_member(
            db,
            workspace_id,
            user_id
        )
    )

    if not member:

        raise ValueError(
            "Member not found"
        )

    WorkspaceMemberRepo.delete(
        db,
        member
    )

    return {
        "message":
        "Member removed successfully"
    }


# =========================================
# DEACTIVATE MEMBER
# =========================================

def deactivate_member(
    db: Session,
    workspace_id: int,
    user_id: int
):

    member = (
        WorkspaceMemberRepo
        .get_member(
            db,
            workspace_id,
            user_id
        )
    )

    if not member:

        raise ValueError(
            "Member not found"
        )

    member.is_active = False

    return (
        WorkspaceMemberRepo
        .save(
            db,
            member
        )
    )