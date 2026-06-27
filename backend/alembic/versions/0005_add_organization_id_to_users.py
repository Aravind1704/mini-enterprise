"""add organization_id to users

Revision ID: 0005_add_organization_id_to_users
Revises: 3370b5564a93_add_project_and_team_relationships
Create Date: 2026-06-22 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0005_add_organization_id_to_users"
down_revision = "3370b5564a93_add_project_and_team_relationships"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {c["name"] for c in inspector.get_columns("users")}

    if "organization_id" not in columns:
        op.add_column(
            "users",
            sa.Column("organization_id", sa.Integer(), nullable=True),
        )
        try:
            op.create_foreign_key(
                "fk_users_organization_id",
                "users",
                "organizations",
                ["organization_id"],
                ["id"],
            )
        except Exception:
            pass


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {c["name"] for c in inspector.get_columns("users")}

    if "organization_id" in columns:
        try:
            op.drop_constraint("fk_users_organization_id", "users", type_="foreignkey")
        except Exception:
            pass
        op.drop_column("users", "organization_id")
