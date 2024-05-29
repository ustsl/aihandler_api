"""comment

Revision ID: a7bf824aea8a
Revises: daf6f19b6eb3
Create Date: 2024-05-21 18:41:43.451974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7bf824aea8a'
down_revision: Union[str, None] = 'daf6f19b6eb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prompts', sa.Column('tuning', sa.JSON(), nullable=True))
    op.drop_column('prompts', 'price_usage')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prompts', sa.Column('price_usage', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=False))
    op.drop_column('prompts', 'tuning')
    # ### end Alembic commands ###