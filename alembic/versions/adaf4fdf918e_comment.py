"""comment

Revision ID: adaf4fdf918e
Revises: 964dc893948c
Create Date: 2024-04-26 14:17:35.698914

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'adaf4fdf918e'
down_revision: Union[str, None] = '964dc893948c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('queries', sa.Column('user', sa.UUID(), nullable=True))
    op.add_column('queries', sa.Column('prompt', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'queries', 'users', ['user'], ['uuid'], ondelete='CASCADE')
    op.create_foreign_key(None, 'queries', 'prompts', ['prompt'], ['uuid'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'queries', type_='foreignkey')
    op.drop_constraint(None, 'queries', type_='foreignkey')
    op.drop_column('queries', 'prompt')
    op.drop_column('queries', 'user')
    # ### end Alembic commands ###
