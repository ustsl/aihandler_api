"""tools module

Revision ID: c31a9c8de421
Revises: 9c9f0d5f93b1
Create Date: 2026-03-17 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c31a9c8de421"
down_revision: Union[str, None] = "9c9f0d5f93b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tools",
        sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("transport", sa.String(length=32), nullable=False, server_default="http_json"),
        sa.Column("method", sa.String(length=8), nullable=False, server_default="POST"),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("input_schema", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("headers_template", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("query_template", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("body_template", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("auth_type", sa.String(length=32), nullable=False, server_default="none"),
        sa.Column("auth_secret_ref", sa.String(), nullable=True),
        sa.Column("timeout_sec", sa.Integer(), nullable=False, server_default="15"),
        sa.Column("max_response_bytes", sa.Integer(), nullable=False, server_default="262144"),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("time_create", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("time_update", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.uuid"]),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("name", name="uq_tools_name"),
    )
    op.create_index(
        "ix_tools_account_active_deleted",
        "tools",
        ["account_id", "is_active", "is_deleted"],
        unique=False,
    )

    op.create_table(
        "prompt_tools",
        sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("prompt_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tool_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_required", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("time_create", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["prompt_id"], ["prompts.uuid"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tool_id"], ["tools.uuid"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("prompt_id", "tool_id", name="uq_prompt_tool"),
    )
    op.create_index(
        "ix_prompt_tools_prompt_sort",
        "prompt_tools",
        ["prompt_id", "sort_order"],
        unique=False,
    )

    op.create_table(
        "tool_call_logs",
        sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("query_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("prompt_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tool_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("tool_name", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("request_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("response_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("error_text", sa.String(), nullable=True),
        sa.Column("time_create", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["prompt_id"], ["prompts.uuid"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["query_id"], ["queries.uuid"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["tool_id"], ["tools.uuid"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_index(
        "ix_tool_call_logs_prompt_time",
        "tool_call_logs",
        ["prompt_id", "time_create"],
        unique=False,
    )
    op.create_index("ix_tool_call_logs_query", "tool_call_logs", ["query_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_tool_call_logs_query", table_name="tool_call_logs")
    op.drop_index("ix_tool_call_logs_prompt_time", table_name="tool_call_logs")
    op.drop_table("tool_call_logs")

    op.drop_index("ix_prompt_tools_prompt_sort", table_name="prompt_tools")
    op.drop_table("prompt_tools")

    op.drop_index("ix_tools_account_active_deleted", table_name="tools")
    op.drop_table("tools")
