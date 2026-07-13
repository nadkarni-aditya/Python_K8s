"""empty message

Revision ID: ca993c6dfb15
Revises: 8990eb152b30
Create Date: 2026-07-13 12:19:04.315125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca993c6dfb15'
down_revision: Union[str, Sequence[str], None] = '8990eb152b30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    # Remote cols points to 'user_id' now instead of 'id'
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['user_id'], ondelete='CASCADE')

def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
