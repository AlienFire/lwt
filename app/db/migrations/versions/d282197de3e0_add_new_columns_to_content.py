"""Add new columns to content

Revision ID: d282197de3e0
Revises: 51f5396f04be
Create Date: 2024-06-27 18:59:08.472783

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d282197de3e0"
down_revision: Union[str, None] = "51f5396f04be"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "content",
        sa.Column(
            "rewatch",
            sa.Boolean(),
            nullable=False,
            server_default="t",
        ),
    )
    op.add_column(
        "content",
        sa.Column(
            "content_status",
            sa.Enum(
                "finished",
                "is_active",
                "at_plan",
                "dropped",
                name="contentstatusenum",
                native_enum=False,
                length=100,
            ),
            server_default="at_plan",
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("content", "content_status")
    op.drop_column("content", "rewatch")
    # ### end Alembic commands ###
