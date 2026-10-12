"""adding rest columns in posts 

Revision ID: 5834fe10e27d
Revises: 04b9407586d1
Create Date: 2026-10-12 18:07:47.239803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5834fe10e27d'
down_revision: Union[str, Sequence[str], None] = '04b9407586d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
      'posts',
      sa.Column(
          'published', sa.Boolean(), nullable=True, server_default='TRUE'
      ),
    )
    op.add_column(
      'posts',
      sa.Column(
          'created_at',
          sa.TIMESTAMP(timezone=True),
          nullable=False,
          server_default=sa.text('NOW()'),
      ),
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass
