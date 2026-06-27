from sqlalchemy.orm import Session

from app.models.team_member import TeamMember


class TeamMemberRepo:

    @staticmethod
    def create(
        db: Session,
        member: TeamMember
    ):
        db.add(member)
        db.commit()
        db.refresh(member)
        return member

    @staticmethod
    def get_member(
        db: Session,
        team_id: int,
        user_id: int
    ):
        return (
            db.query(TeamMember)
            .filter(
                TeamMember.team_id == team_id,
                TeamMember.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def list_members(
        db: Session,
        team_id: int
    ):
        return (
            db.query(TeamMember)
            .filter(
                TeamMember.team_id == team_id,
                TeamMember.is_active == True
            )
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        member: TeamMember
    ):
        db.delete(member)
        db.commit()

    @staticmethod
    def save(
        db: Session,
        member: TeamMember
    ):
        db.commit()
        db.refresh(member)
        return member
