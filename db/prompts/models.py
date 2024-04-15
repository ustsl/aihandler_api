import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from db.models import MaintenanceModel


##############################
# BLOCK WITH DATABASE MODELS #
##############################


class PromptModel(MaintenanceModel):
    __tablename__ = "prompts"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
