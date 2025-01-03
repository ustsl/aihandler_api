"""comment

Revision ID: 475df8f9c7cd
Revises: a30ebaffd887
Create Date: 2024-04-30 14:45:48.043674

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '475df8f9c7cd'
down_revision: Union[str, None] = 'a30ebaffd887'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_settings', 'time_update')
    op.drop_column('user_settings', 'time_create')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_settings', sa.Column('time_create', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.add_column('user_settings', sa.Column('time_update', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
