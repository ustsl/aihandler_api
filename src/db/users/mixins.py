from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declared_attr, relationship


class UserRelationMixin:

    _user_id_is_inique: bool = False
    _user_back_populates: str | None = None
    _user_id_is_nullable: bool = False
    _user_uselist = False

    @declared_attr
    def user_id(cls) -> Mapped[UUID]:
        return Column(
            UUID(as_uuid=True),
            ForeignKey("users.uuid", ondelete="CASCADE"),
            nullable=cls._user_id_is_nullable,
            unique=cls._user_id_is_inique,
        )

    @declared_attr
    def user(cls):
        return relationship(
            "UserModel",
            back_populates=cls._user_back_populates,
            uselist=cls._user_uselist,
        )
