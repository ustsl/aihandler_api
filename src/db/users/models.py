from sqlalchemy import Column, Numeric, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.models import TimeModel, MaintenanceModel, Base
from src.db.users.mixins import UserRelationMixin
import uuid


class UserModel(MaintenanceModel):
    __tablename__ = "users"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(String, unique=True)

    # back relations
    token = relationship("UserTokenModel", back_populates="user", uselist=False)
    accounts = relationship("UserAccountModel", back_populates="user", uselist=False)
    queries = relationship("QueryModel", back_populates="user")
    settings = relationship("UserSettingsModel", back_populates="user", uselist=False)


class UserTokenModel(TimeModel, UserRelationMixin):
    __tablename__ = "tokens"
    _user_back_populates = "token"
    _user_uselist = False
    _user_id_is_inique = True

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String, nullable=False)


class UserAccountModel(TimeModel, UserRelationMixin):
    __tablename__ = "accounts"
    _user_back_populates = "accounts"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(Numeric(11, 5), nullable=False, default=0.5)

    # back relations
    prompts = relationship("PromptModel", back_populates="account", uselist=True)


class UserSettingsModel(Base, UserRelationMixin):
    __tablename__ = "user_settings"
    _user_back_populates = "settings"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.uuid"), nullable=True)

    # back relations
    prompt = relationship("PromptModel", back_populates="settings", uselist=False)
