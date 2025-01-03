"""scenario

Revision ID: 8a933bb6b5b9
Revises: 31381da05866
Create Date: 2024-12-09 14:59:52.256228

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8a933bb6b5b9'
down_revision: Union[str, None] = '31381da05866'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scenario',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('account_id', sa.UUID(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('time_create', sa.DateTime(timezone=True), nullable=True),
    sa.Column('time_update', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('scenario_prompts_relation',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('scenario_id', sa.UUID(), nullable=False),
    sa.Column('prompt_id', sa.UUID(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('time_create', sa.DateTime(timezone=True), nullable=True),
    sa.Column('time_update', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['prompt_id'], ['prompts.uuid'], ),
    sa.ForeignKeyConstraint(['scenario_id'], ['scenario.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.drop_table('prompt_system_prompts')
    op.drop_table('prompt_systems')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prompt_systems',
    sa.Column('uuid', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('account_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('time_create', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('time_update', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.uuid'], name='prompt_systems_account_id_fkey'),
    sa.PrimaryKeyConstraint('uuid', name='prompt_systems_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('prompt_system_prompts',
    sa.Column('uuid', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('prompt_system_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('prompt_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('order', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('time_create', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('time_update', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['prompt_id'], ['prompts.uuid'], name='prompt_system_prompts_prompt_id_fkey'),
    sa.ForeignKeyConstraint(['prompt_system_id'], ['prompt_systems.uuid'], name='prompt_system_prompts_prompt_system_id_fkey'),
    sa.PrimaryKeyConstraint('uuid', name='prompt_system_prompts_pkey')
    )
    op.drop_table('scenario_prompts_relation')
    op.drop_table('scenario')
    # ### end Alembic commands ###
