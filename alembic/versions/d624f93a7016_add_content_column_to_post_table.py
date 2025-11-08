"""add content column to post table

Revision ID: d624f93a7016
Revises: 3e578eaaafa3
Create Date: 2025-11-08 22:59:10.474921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd624f93a7016'
down_revision: Union[str, Sequence[str], None] = '3e578eaaafa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
