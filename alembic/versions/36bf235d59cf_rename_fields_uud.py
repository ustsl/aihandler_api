"""rename fields uud

Revision ID: 36bf235d59cf
Revises: 7542b171cf93
Create Date: 2024-05-20 17:45:16.825734

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "36bf235d59cf"
down_revision: Union[str, None] = "7542b171cf93"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Переименовываем столбец account_id в uuid
    op.alter_column(
        "accounts",
        "account_id",
        new_column_name="uuid",
        existing_type=sa.UUID(),
        nullable=False,
    )

    # Обновляем внешний ключ в таблице prompts
    op.drop_constraint("prompts_account_id_fkey", "prompts", type_="foreignkey")
    op.create_foreign_key(None, "prompts", "accounts", ["account_id"], ["uuid"])

    # Переименовываем столбец token_id в uuid
    op.alter_column(
        "tokens",
        "token_id",
        new_column_name="uuid",
        existing_type=sa.UUID(),
        nullable=False,
    )


def downgrade() -> None:
    # Переименовываем столбец uuid обратно в account_id
    op.alter_column(
        "accounts",
        "uuid",
        new_column_name="account_id",
        existing_type=sa.UUID(),
        nullable=False,
    )

    # Обновляем внешний ключ в таблице prompts
    op.drop_constraint(None, "prompts", type_="foreignkey")
    op.create_foreign_key(
        "prompts_account_id_fkey", "prompts", "accounts", ["account_id"], ["account_id"]
    )

    # Переименовываем столбец uuid обратно в token_id
    op.alter_column(
        "tokens",
        "uuid",
        new_column_name="token_id",
        existing_type=sa.UUID(),
        nullable=False,
    )
