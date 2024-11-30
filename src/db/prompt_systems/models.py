import uuid

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.models import MaintenanceModel, TimeModel


################################
###BLOCK WITH DATABASE MODELS###
################################


class PromptSystemModel(MaintenanceModel, TimeModel):
    __tablename__ = "prompt_systems"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.uuid"), nullable=False)


class PromptSystemPromptModel(MaintenanceModel, TimeModel):
    __tablename__ = "prompt_system_prompts"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_system_id = Column(
        UUID(as_uuid=True), ForeignKey("prompt_systems.uuid"), nullable=False
    )
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.uuid"), nullable=False)
    order = Column(Integer, nullable=False, default=0)

    prompt = relationship("PromptModel", back_populates="systems")
