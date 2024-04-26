"""comment

Revision ID: 195f0b70e16a
Revises: 89aab1181c9b
Create Date: 2024-04-26 15:02:27.188304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '195f0b70e16a'
down_revision: Union[str, None] = '89aab1181c9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('queries', sa.Column('result', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('queries', 'result')
    # ### end Alembic commands ###
