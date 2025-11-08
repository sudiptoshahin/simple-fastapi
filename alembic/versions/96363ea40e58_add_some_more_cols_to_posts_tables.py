"""add some more cols to posts tables

Revision ID: 96363ea40e58
Revises: c65b15b7cedf
Create Date: 2025-11-09 00:16:27.586033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96363ea40e58'
down_revision: Union[str, Sequence[str], None] = 'c65b15b7cedf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
