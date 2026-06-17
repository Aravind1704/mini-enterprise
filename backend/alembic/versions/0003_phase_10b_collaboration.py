"""phase 10b collaboration messages tasks and documents

Revision ID: 0003_phase_10b_collaboration
Revises: 0002_add_tenant_id_to_users
Create Date: 2026-06-08 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = "0003_phase_10b_collaboration"
down_revision = "0002_add_tenant_id_to_users"
branch_labels = None
depends_on = None


def _table_names(inspector):
    return set(inspector.get_table_names())


def _column_names(inspector, table_name):
    if table_name not in _table_names(inspector):
        return set()
    return {column["name"] for column in inspector.get_columns(table_name)}


def _add_column_if_missing(inspector, table_name, column):
    if column.name in _column_names(inspector, table_name):
        return
    with op.batch_alter_table(table_name) as batch_op:
        batch_op.add_column(column)


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = _table_names(inspector)

    if "tasks" in tables:
        _add_column_if_missing(
            inspector,
            "tasks",
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id"), nullable=True),
        )
        _add_column_if_missing(
            inspector,
            "tasks",
            sa.Column("workspace_id", sa.Integer(), sa.ForeignKey("workspaces.id"), nullable=True),
        )
        _add_column_if_missing(
            inspector,
            "tasks",
            sa.Column("channel_id", sa.Integer(), sa.ForeignKey("channels.id"), nullable=True),
        )

    if "approvals" in tables:
        _add_column_if_missing(
            inspector,
            "approvals",
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id"), nullable=True),
        )
        _add_column_if_missing(
            inspector,
            "approvals",
            sa.Column("workspace_id", sa.Integer(), sa.ForeignKey("workspaces.id"), nullable=True),
        )
        _add_column_if_missing(
            inspector,
            "approvals",
            sa.Column("channel_id", sa.Integer(), sa.ForeignKey("channels.id"), nullable=True),
        )

    tables = _table_names(sa.inspect(bind))

    if "workspace_messages" not in tables:
        op.create_table(
            "workspace_messages",
            sa.Column("id", sa.Integer(), primary_key=True, index=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id"), nullable=False),
            sa.Column("workspace_id", sa.Integer(), sa.ForeignKey("workspaces.id"), nullable=False),
            sa.Column("sender_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("message_type", sa.String(length=50), nullable=True, server_default="TEXT"),
            sa.Column("edited_at", sa.DateTime(), nullable=True),
            sa.Column("deleted_at", sa.DateTime(), nullable=True),
            sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )

    if "channel_messages" not in tables:
        op.create_table(
            "channel_messages",
            sa.Column("id", sa.Integer(), primary_key=True, index=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id"), nullable=False),
            sa.Column("workspace_id", sa.Integer(), sa.ForeignKey("workspaces.id"), nullable=False),
            sa.Column("channel_id", sa.Integer(), sa.ForeignKey("channels.id"), nullable=False),
            sa.Column("sender_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("message_type", sa.String(length=50), nullable=True, server_default="TEXT"),
            sa.Column("edited_at", sa.DateTime(), nullable=True),
            sa.Column("deleted_at", sa.DateTime(), nullable=True),
            sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )

    if "task_documents" not in tables:
        op.create_table(
            "task_documents",
            sa.Column("id", sa.Integer(), primary_key=True, index=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id"), nullable=False),
            sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id"), nullable=False),
            sa.Column("file_name", sa.String(length=255), nullable=False),
            sa.Column("file_path", sa.String(length=500), nullable=False),
            sa.Column("file_size", sa.Integer(), nullable=False),
            sa.Column("mime_type", sa.String(length=255), nullable=True),
            sa.Column("uploaded_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
            sa.Column("document_type", sa.String(length=50), nullable=True, server_default="OTHER"),
            sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        )

    if "approval_documents" not in tables:
        op.create_table(
            "approval_documents",
            sa.Column("id", sa.Integer(), primary_key=True, index=True),
            sa.Column("tenant_id", sa.Integer(), sa.ForeignKey("tenants.id"), nullable=False),
            sa.Column("approval_id", sa.Integer(), sa.ForeignKey("approvals.id"), nullable=False),
            sa.Column("file_name", sa.String(length=255), nullable=False),
            sa.Column("file_path", sa.String(length=500), nullable=False),
            sa.Column("file_size", sa.Integer(), nullable=False),
            sa.Column("mime_type", sa.String(length=255), nullable=True),
            sa.Column("uploaded_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
            sa.Column("document_type", sa.String(length=50), nullable=True, server_default="SUPPORTING"),
            sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = _table_names(inspector)

    for table_name in (
        "approval_documents",
        "task_documents",
        "channel_messages",
        "workspace_messages",
    ):
        if table_name in tables:
            op.drop_table(table_name)

    for table_name in ("approvals", "tasks"):
        if table_name not in _table_names(sa.inspect(bind)):
            continue
        columns = _column_names(sa.inspect(bind), table_name)
        with op.batch_alter_table(table_name) as batch_op:
            for column_name in ("channel_id", "workspace_id", "tenant_id"):
                if column_name in columns:
                    batch_op.drop_column(column_name)
