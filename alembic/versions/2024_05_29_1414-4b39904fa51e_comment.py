"""comment

Revision ID: 4b39904fa51e
Revises: aee1ce50bf6d
Create Date: 2024-05-29 14:14:37.238072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b39904fa51e'
down_revision: Union[str, None] = 'aee1ce50bf6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_settings', sa.Column('language', sa.String(length=2), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_settings', 'language')
    # ### end Alembic commands ###