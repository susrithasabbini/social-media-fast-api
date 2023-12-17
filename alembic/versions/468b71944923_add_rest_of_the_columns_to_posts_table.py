"""ADD REST OF THE COLUMNS TO POSTS TABLE

Revision ID: 468b71944923
Revises: 76c13197682c
Create Date: 2023-12-17 18:49:10.654843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "468b71944923"
down_revision: Union[str, None] = "76c13197682c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "createdAt",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )

    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "createdAt")
    pass
