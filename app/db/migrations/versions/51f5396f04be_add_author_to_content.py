"""Add author to Content

Revision ID: 51f5396f04be
Revises: a65adceb0867
Create Date: 2024-06-21 17:40:21.243147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '51f5396f04be'
down_revision: Union[str, None] = 'a65adceb0867'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('content', sa.Column('user_id', sa.Integer(), nullable=False))
    op.alter_column('content', 'name',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    op.alter_column('content', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.create_foreign_key(None, 'content', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'content', type_='foreignkey')
    op.alter_column('content', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('content', 'name',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    op.drop_column('content', 'user_id')
    # ### end Alembic commands ###
