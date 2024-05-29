"""comment

Revision ID: 2898981fbf31
Revises: b252f18b0fc6
Create Date: 2024-05-29 13:50:56.972954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2898981fbf31'
down_revision: Union[str, None] = 'b252f18b0fc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('accounts_user_id_fkey', 'accounts', type_='foreignkey')
    op.create_foreign_key(None, 'accounts', 'users', ['user_id'], ['uuid'], ondelete='CASCADE')
    op.alter_column('queries', 'user_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('user_settings_user_id_fkey', 'user_settings', type_='foreignkey')
    op.create_foreign_key(None, 'user_settings', 'users', ['user_id'], ['uuid'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_settings', type_='foreignkey')
    op.create_foreign_key('user_settings_user_id_fkey', 'user_settings', 'users', ['user_id'], ['uuid'])
    op.alter_column('queries', 'user_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_constraint(None, 'accounts', type_='foreignkey')
    op.create_foreign_key('accounts_user_id_fkey', 'accounts', 'users', ['user_id'], ['uuid'])
    # ### end Alembic commands ###
