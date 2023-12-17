"""ADD DESCRIPTION COLUMN TO POST TABLE

Revision ID: 470b6eb42f08
Revises: d66179eb685e
Create Date: 2023-12-17 18:27:08.535393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "470b6eb42f08"
down_revision: Union[str, None] = "d66179eb685e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("description", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "description")
    pass
