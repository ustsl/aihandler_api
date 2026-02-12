import re
from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator

from src.api.scenarios.schemas.post import ScenarioPostSchema

#########################
# BLOCK WITH API MODELS #
#########################


class ScenarioPromptsUpdateBodySchema(BaseModel):
    prompt_id: UUID
    order: int
    independent: bool


class ScenarioUpdateBodySchema(ScenarioPostSchema):
    title: Optional[str]
    description: Optional[str]
    prompts: Optional[List[ScenarioPromptsUpdateBodySchema]] = []

    class Config:
        extra = "forbid"


class ScenarioGetAfterUpdateFullSchema(BaseModel):
    uuid: UUID
    title: str
    description: str
    prompts: Optional[List[ScenarioUpdateBodySchema]] = []
    time_create: datetime
