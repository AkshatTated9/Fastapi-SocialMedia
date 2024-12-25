"""Adding foregin key contraints post

Revision ID: e9ebdf4ba0af
Revises: 18506a8239a4
Create Date: 2024-12-24 20:32:40.703347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9ebdf4ba0af'
down_revision: Union[str, None] = '18506a8239a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts1', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts1", referent_table="user", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts1")
    op.drop_column('posts', 'owner_id')
    pass
