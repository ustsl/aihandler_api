"""constr

Revision ID: c594f54d8e0a
Revises: 2e38a5a7775b
Create Date: 2024-12-11 22:10:58.511259

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c594f54d8e0a'
down_revision: Union[str, None] = '2e38a5a7775b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_scenario_prompt', 'scenario_prompts_relation', ['scenario_id', 'prompt_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_scenario_prompt', 'scenario_prompts_relation', type_='unique')
    # ### end Alembic commands ###