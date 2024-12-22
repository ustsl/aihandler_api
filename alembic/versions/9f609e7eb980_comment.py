"""comment

Revision ID: 9f609e7eb980
Revises: 475df8f9c7cd
Create Date: 2024-05-12 18:07:59.086075

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9f609e7eb980'
down_revision: Union[str, None] = '475df8f9c7cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('prompts_title_key', 'prompts', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('prompts_title_key', 'prompts', ['title'])
    # ### end Alembic commands ###
