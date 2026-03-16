import uuid

from sqlalchemy import (JSON, Boolean, Column, DateTime, ForeignKey, Index,
                        Integer, String, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.models import Base, MaintenanceModel, TimeModel


class ToolModel(MaintenanceModel, TimeModel):
    __tablename__ = "tools"
    __table_args__ = (
        UniqueConstraint("name", name="uq_tools_name"),
        Index("ix_tools_account_active_deleted", "account_id", "is_active", "is_deleted"),
    )

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64), nullable=False)
    description = Column(String, nullable=False)

    transport = Column(String(32), nullable=False, default="http_json")
    method = Column(String(8), nullable=False, default="POST")
    url = Column(String, nullable=True)

    input_schema = Column(JSON, nullable=False, default=dict)
    headers_template = Column(JSON, nullable=True)
    query_template = Column(JSON, nullable=True)
    body_template = Column(JSON, nullable=True)

    auth_type = Column(String(32), nullable=False, default="none")
    auth_secret_ref = Column(String, nullable=True)

    timeout_sec = Column(Integer, nullable=False, default=15)
    max_response_bytes = Column(Integer, nullable=False, default=262144)

    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.uuid"), nullable=True)

    prompt_links = relationship(
        "PromptToolModel",
        back_populates="tool",
        cascade="all, delete-orphan",
    )
    call_logs = relationship("ToolCallLogModel", back_populates="tool")


class PromptToolModel(Base):
    __tablename__ = "prompt_tools"
    __table_args__ = (
        UniqueConstraint("prompt_id", "tool_id", name="uq_prompt_tool"),
        Index("ix_prompt_tools_prompt_sort", "prompt_id", "sort_order"),
    )

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_id = Column(
        UUID(as_uuid=True),
        ForeignKey("prompts.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    tool_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tools.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    sort_order = Column(Integer, nullable=False, default=0)
    is_required = Column(Boolean, nullable=False, default=False)
    time_create = Column(DateTime(timezone=True), default=func.now())

    prompt = relationship("PromptModel", back_populates="prompt_tools")
    tool = relationship("ToolModel", back_populates="prompt_links")


class ToolCallLogModel(Base):
    __tablename__ = "tool_call_logs"
    __table_args__ = (
        Index("ix_tool_call_logs_prompt_time", "prompt_id", "time_create"),
        Index("ix_tool_call_logs_query", "query_id"),
    )

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(
        UUID(as_uuid=True),
        ForeignKey("queries.uuid", ondelete="SET NULL"),
        nullable=True,
    )
    prompt_id = Column(
        UUID(as_uuid=True),
        ForeignKey("prompts.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    tool_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tools.uuid", ondelete="SET NULL"),
        nullable=True,
    )
    tool_name = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False)
    duration_ms = Column(Integer, nullable=True)
    request_payload = Column(JSON, nullable=True)
    response_payload = Column(JSON, nullable=True)
    error_text = Column(String, nullable=True)
    time_create = Column(DateTime(timezone=True), default=func.now())

    prompt = relationship("PromptModel", back_populates="tool_call_logs")
    tool = relationship("ToolModel", back_populates="call_logs")
