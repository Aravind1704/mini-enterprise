"""add tenant_id to users

Revision ID: 0002_add_tenant_id_to_users
Revises: 3f2b1c4e5a6b
Create Date: 2026-06-03 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_add_tenant_id_to_users'
down_revision = '3f2b1c4e5a6b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('tenant_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_users_tenant_id',
        'users', 'tenants', ['tenant_id'], ['id']
    )


def downgrade():
    op.drop_constraint('fk_users_tenant_id', 'users', type_='foreignkey')
    op.drop_column('users', 'tenant_id')
