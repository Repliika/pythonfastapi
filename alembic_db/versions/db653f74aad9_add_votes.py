"""add votes

Revision ID: db653f74aad9
Revises: 0c0e55dcab12
Create Date: 2023-06-03 15:30:33.733252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db653f74aad9'
down_revision = '0c0e55dcab12'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'votes',
        sa.Column('user_id', sa.Integer(),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column('post_id', sa.Integer(),
                  sa.ForeignKey("Music_Posts.id", ondelete="CASCADE"), primary_key=True)
    )


def downgrade() -> None:
    op.drop_table('votes')
