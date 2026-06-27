from fastapi import HTTPException


def require_project_member(
    project,
    user_id: int
):
    member_ids = [
        t.team_id
        for t in project.teams
    ]

    if not member_ids:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )