from sqlalchemy import Column, Numeric, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.models import TimeModel

import uuid


##############################
# BLOCK WITH DATABASE MODELS #
##############################


class QueryModel(TimeModel):
    __tablename__ = "queries"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="CASCADE"))
    prompt_id = Column(
        UUID(as_uuid=True), ForeignKey("prompts.uuid", ondelete="CASCADE")
    )
    query = Column(String, nullable=False)
    result = Column(String, nullable=True)
    user = relationship("UserModel", back_populates="queries", uselist=True)
    prompt = relationship("PromptModel", back_populates="queries", uselist=True)
