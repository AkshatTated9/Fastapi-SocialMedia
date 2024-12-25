"""Create Vote  Table

Revision ID: c31a2a8b6b78
Revises: e9ebdf4ba0af
Create Date: 2024-12-24 22:46:20.697355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c31a2a8b6b78'
down_revision: Union[str, None] = 'e9ebdf4ba0af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts1.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    pass


def downgrade() -> None:
    op.drop_table('votes')
    pass
