from sqlalchemy import Column, Numeric, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.models import TimeModel, MaintenanceModel, Base
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


class UserTokenModel(TimeModel):
    __tablename__ = "tokens"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="CASCADE"), unique=True
    )
    token = Column(String, nullable=False)
    user = relationship(
        "UserModel", back_populates="token", uselist=False, cascade="all"
    )


class UserAccountModel(TimeModel):
    __tablename__ = "accounts"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)
    balance = Column(Numeric(11, 5), nullable=False, default=0.5)

    # back relations
    user = relationship("UserModel", back_populates="accounts", uselist=False)
    prompts = relationship("PromptModel", back_populates="account", uselist=True)


class UserSettingsModel(Base):
    __tablename__ = "user_settings"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.uuid"), nullable=True)

    # back relations
    user = relationship("UserModel", back_populates="settings", uselist=False)
    prompt = relationship("PromptModel", back_populates="settings", uselist=False)
