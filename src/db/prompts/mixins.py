from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr, Mapped, relationship
from sqlalchemy import Column, ForeignKey


class PromptRelationMixin:

    _prompt_id_is_inique: bool = False
    _prompt_back_populates: str | None = None
    _prompt_id_is_nullable: bool = False
    _prompt_uselist = False

    @declared_attr
    def prompt_id(cls) -> Mapped[UUID]:
        return Column(
            UUID(as_uuid=True),
            ForeignKey("prompts.uuid", ondelete="CASCADE"),
            nullable=cls._prompt_id_is_nullable,
            unique=cls._prompt_id_is_inique,
        )

    @declared_attr
    def prompt(cls):
        return relationship(
            "PromptModel",
            back_populates=cls._prompt_back_populates,
            uselist=cls._prompt_uselist,
        )
