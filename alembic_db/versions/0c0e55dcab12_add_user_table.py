"""add user table

Revision ID: 0c0e55dcab12
Revises: dd8ac05d9d62
Create Date: 2023-06-03 15:28:38.014332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c0e55dcab12'
down_revision = 'dd8ac05d9d62'
branch_labels = None
depends_on = None


def upgrade() -> None:
        op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )



def downgrade() -> None:
     op.drop_table('users')
