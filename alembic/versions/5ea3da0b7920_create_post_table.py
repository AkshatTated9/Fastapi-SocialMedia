"""Create Post Table

Revision ID: 5ea3da0b7920
Revises: 
Create Date: 2024-12-24 19:56:25.555340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ea3da0b7920'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts1',sa.Column("id",sa.Integer(),nullable=False,primary_key=True),sa.Column("title",sa.String(),nullable=False),sa.Column("content",sa.String(),nullable=False),sa.Column("published",sa.Boolean(),server_default='True'),sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_table('posts1')
    pass
