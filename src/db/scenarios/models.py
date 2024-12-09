import uuid

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.models import MaintenanceModel, TimeModel


################################
###BLOCK WITH DATABASE MODELS###
################################


class ScenarioModel(MaintenanceModel, TimeModel):
    __tablename__ = "scenario"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.uuid"), nullable=False)

    scenario_prompts = relationship(
        "ScenarioPromptsModel",
        backref="scenario",
        cascade="all, delete-orphan",
    )


class ScenarioPromptsModel(MaintenanceModel, TimeModel):
    __tablename__ = "scenario_prompts_relation"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id = Column(
        UUID(as_uuid=True),
        ForeignKey("scenario.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.uuid"), nullable=False)
    order = Column(Integer, nullable=False, default=0)

    prompt = relationship("PromptModel", back_populates="scenario")
