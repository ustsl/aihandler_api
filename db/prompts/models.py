import uuid
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, ForeignKey, Numeric, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.models import MaintenanceModel, TimeModel

from db.users.models import UserAccountModel

##############################
# BLOCK WITH DATABASE MODELS #
##############################


class PromptModel(MaintenanceModel, TimeModel):
    __tablename__ = "prompts"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    model = Column(String, default="gpt-3.5-turbo", nullable=False)
    is_open = Column(Boolean(), default=True, nullable=True)

    account_id = Column(
        UUID(as_uuid=True), ForeignKey("accounts.account_id"), nullable=False
    )

    price_usage = Column(Numeric(10, 2), nullable=False, default=0.00)

    # Отношение, указывающее на аккаунт, к которому привязан промпт
    account = relationship("UserAccountModel", back_populates="prompts")
