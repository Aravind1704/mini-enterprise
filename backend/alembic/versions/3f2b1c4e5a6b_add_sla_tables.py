"""add approval_escalations, approval_delegations, notification_preferences, audit fields, sla fields

Revision ID: 3f2b1c4e5a6b
Revises: <prev_rev>
Create Date: 2026-05-21 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '3f2b1c4e5a6b'
down_revision = '<prev_rev>'
branch_labels = None
depends_on = None


def upgrade():
    # 1) Create approval_escalations table
    op.create_table(
        'approval_escalations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('approval_id', sa.Integer(), sa.ForeignKey('approvals.id'), nullable=False),
        sa.Column('escalated_from', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('escalated_to', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('escalation_level', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default=sa.text("'pending'")),
        sa.Column('escalated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
    )

    # 2) Create approval_delegations table
    op.create_table(
        'approval_delegations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('delegator_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('delegatee_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # 3) Create notification_preferences table
    op.create_table(
        'notification_preferences',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, unique=True),
        sa.Column('in_app_enabled', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('email_enabled', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('task_notifications', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('approval_notifications', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('escalation_notifications', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('document_notifications', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    # 4) Alter audit_logs: add enhanced fields if not present
    # Note: Alembic autogenerate may already detect these; adding defensively.
    with op.batch_alter_table('audit_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('module_name', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('action_type', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('record_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('old_data', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('new_data', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('ip_address', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('user_agent', sa.String(length=300), nullable=True))

    # 5) Alter tasks table: add SLA fields
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sla_status', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('sla_due_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('is_sla_breached', sa.Boolean(), nullable=False, server_default=sa.text('0')))

    # 6) Alter approvals table: add SLA and escalation fields
    with op.batch_alter_table('approvals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sla_status', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('sla_due_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('is_escalated', sa.Boolean(), nullable=False, server_default=sa.text('0')))
        batch_op.add_column(sa.Column('current_escalation_to', sa.Integer(), sa.ForeignKey('users.id'), nullable=True))

    # 7) Optional: add notifications table fields if you have a notifications table schema to extend
    # If your project has a 'notifications' table and you want to add notification_type/priority:
    try:
        with op.batch_alter_table('notifications', schema=None) as batch_op:
            batch_op.add_column(sa.Column('notification_type', sa.String(length=100), nullable=True))
            batch_op.add_column(sa.Column('priority', sa.String(length=50), nullable=True))
    except Exception:
        # If notifications table does not exist or columns already present, skip silently
        pass


def downgrade():
    # Reverse changes in reverse order

    # 1) Remove optional notifications columns if present
    try:
        with op.batch_alter_table('notifications', schema=None) as batch_op:
            batch_op.drop_column('priority')
            batch_op.drop_column('notification_type')
    except Exception:
        pass

    # 2) Revert approvals table changes
    with op.batch_alter_table('approvals', schema=None) as batch_op:
        # drop columns if exist
        try:
            batch_op.drop_column('current_escalation_to')
        except Exception:
            pass
        try:
            batch_op.drop_column('is_escalated')
        except Exception:
            pass
        try:
            batch_op.drop_column('sla_due_time')
        except Exception:
            pass
        try:
            batch_op.drop_column('sla_status')
        except Exception:
            pass

    # 3) Revert tasks table changes
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        try:
            batch_op.drop_column('is_sla_breached')
        except Exception:
            pass
        try:
            batch_op.drop_column('sla_due_time')
        except Exception:
            pass
        try:
            batch_op.drop_column('sla_status')
        except Exception:
            pass

    # 4) Revert audit_logs changes
    with op.batch_alter_table('audit_logs', schema=None) as batch_op:
        try:
            batch_op.drop_column('user_agent')
        except Exception:
            pass
        try:
            batch_op.drop_column('ip_address')
        except Exception:
            pass
        try:
            batch_op.drop_column('new_data')
        except Exception:
            pass
        try:
            batch_op.drop_column('old_data')
        except Exception:
            pass
        try:
            batch_op.drop_column('record_id')
        except Exception:
            pass
        try:
            batch_op.drop_column('action_type')
        except Exception:
            pass
        try:
            batch_op.drop_column('module_name')
        except Exception:
            pass

    # 5) Drop notification_preferences table
    op.drop_table('notification_preferences')

    # 6) Drop approval_delegations table
    op.drop_table('approval_delegations')

    # 7) Drop approval_escalations table
    op.drop_table('approval_escalations')
