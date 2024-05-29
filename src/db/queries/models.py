from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.users.mixins import UserRelationMixin
from src.db.prompts.mixins import PromptRelationMixin
from src.db.models import Base

import uuid


##############################
# BLOCK WITH DATABASE MODELS #
##############################


class QueryModel(Base, UserRelationMixin, PromptRelationMixin):
    __tablename__ = "queries"
    _user_back_populates = "queries"
    _prompt_back_populates = "queries"
    _prompt_uselist = True

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    query = Column(String, nullable=False)
    result = Column(String, nullable=True)
    time_create = Column(DateTime(timezone=True), default=func.now())
