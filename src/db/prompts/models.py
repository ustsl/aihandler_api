import uuid
from src.db.scenarios.models import ScenarioPromptsModel
from sqlalchemy import Column, ForeignKey, String, Boolean, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.models import MaintenanceModel, TimeModel


################################
###BLOCK WITH DATABASE MODELS###
################################


class PromptModel(MaintenanceModel, TimeModel):
    __tablename__ = "prompts"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    model = Column(String, default="gpt-3.5-turbo", nullable=False)
    is_open = Column(Boolean(), default=True, nullable=True)
    context_story_window = Column(Integer, default=0, nullable=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.uuid"), nullable=False)
    tuning = Column(JSON, nullable=True)

    # Отношение, указывающее на аккаунт, к которому привязан промпт
    account = relationship("UserAccountModel", back_populates="prompts")
    queries = relationship("QueryModel", back_populates="prompt")
    settings = relationship("UserSettingsModel", back_populates="prompt")
    scenario = relationship(
        ScenarioPromptsModel, back_populates="prompt", cascade="all, delete-orphan"
    )
