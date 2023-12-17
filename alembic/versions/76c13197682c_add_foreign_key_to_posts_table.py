"""ADD FOREIGN KEY TO POSTS TABLE

Revision ID: 76c13197682c
Revises: 82096abcd093
Create Date: 2023-12-17 18:36:41.203617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "76c13197682c"
down_revision: Union[str, None] = "82096abcd093"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("ownerId", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["ownerId"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", "posts", type_="foreignkey")
    op.drop_column("posts", "ownerId")
    pass
