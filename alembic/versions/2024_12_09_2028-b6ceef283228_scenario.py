"""scenario

Revision ID: b6ceef283228
Revises: 8f951580d532
Create Date: 2024-12-09 20:28:46.796795

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b6ceef283228'
down_revision: Union[str, None] = '8f951580d532'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('scenario_prompts_relation_scenario_id_fkey', 'scenario_prompts_relation', type_='foreignkey')
    op.create_foreign_key(None, 'scenario_prompts_relation', 'scenario', ['scenario_id'], ['uuid'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'scenario_prompts_relation', type_='foreignkey')
    op.create_foreign_key('scenario_prompts_relation_scenario_id_fkey', 'scenario_prompts_relation', 'scenario', ['scenario_id'], ['uuid'])
    # ### end Alembic commands ###
