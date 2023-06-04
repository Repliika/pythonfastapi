"""create music table

Revision ID: dd8ac05d9d62
Revises: 
Create Date: 2023-06-03 15:26:15.397718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd8ac05d9d62'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'Music_Posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('song', sa.String(), nullable=False),
        sa.Column('artist', sa.String(), nullable=False),
        sa.Column('genre', sa.String(), nullable=False),
        sa.Column('opinion', sa.Text(), nullable=True),
        sa.Column('spotify', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()')),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')

    )
    
def downgrade() -> None:
     op.drop_table('Music_Posts')
