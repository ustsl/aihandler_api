import uuid

from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.models import MaintenanceModel, TimeModel


##############################
# BLOCK WITH DATABASE MODELS #
##############################


class PromptModel(MaintenanceModel, TimeModel):
    __tablename__ = "prompts"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    model = Column(String, default="gpt-3.5-turbo", nullable=True)
    is_open = Column(Boolean(), default=False, nullable=True)

    account_id = Column(
        UUID(as_uuid=True), ForeignKey("accounts.account_id"), nullable=False
    )

    # Отношение, указывающее на аккаунт, к которому привязан промпт
    account = relationship("UserAccountModel", back_populates="prompts")
