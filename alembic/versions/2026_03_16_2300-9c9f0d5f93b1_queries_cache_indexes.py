"""queries cache indexes

Revision ID: 9c9f0d5f93b1
Revises: bfe9ab3009ee
Create Date: 2026-03-16 23:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9c9f0d5f93b1"
down_revision: Union[str, None] = "bfe9ab3009ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_queries_prompt_id_time_create
        ON queries (prompt_id, time_create DESC)
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_queries_prompt_id_query_hash_time_create
        ON queries (prompt_id, md5(query), time_create DESC)
        """
    )

    # Defensive cleanup: if a result index was previously created manually, remove it.
    op.execute("DROP INDEX IF EXISTS ix_queries_result")
    op.execute("DROP INDEX IF EXISTS queries_result_idx")
    op.execute("DROP INDEX IF EXISTS idx_queries_result")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_queries_prompt_id_query_hash_time_create")
    op.execute("DROP INDEX IF EXISTS ix_queries_prompt_id_time_create")
