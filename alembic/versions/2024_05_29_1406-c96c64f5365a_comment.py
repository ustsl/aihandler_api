"""comment

Revision ID: c96c64f5365a
Revises: 2898981fbf31
Create Date: 2024-05-29 14:06:52.017792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c96c64f5365a'
down_revision: Union[str, None] = '2898981fbf31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tokens', 'user_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tokens', 'user_id',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###
