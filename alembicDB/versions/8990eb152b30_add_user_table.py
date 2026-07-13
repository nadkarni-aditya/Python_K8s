"""add user table

Revision ID: 8990eb152b30
Revises: 760eb483b1e8
Create Date: 2026-07-13 11:48:03.881268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8990eb152b30'
down_revision: Union[str, Sequence[str], None] = '760eb483b1e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True, nullable=False), # Changed to user_id
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    )

    op.create_table(
        'votes',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True), # Pointing to users.user_id
        sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.post_id', ondelete='CASCADE'), primary_key=True)  # Pointing to posts.post_id
    )   

def downgrade() -> None:
    op.drop_table('votes')
    op.drop_table('users')
