import re
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.settings import GPTModelName

#########################
# BLOCK WITH API MODELS #
#########################


class ScenarioGetSchema(BaseModel):
    id: UUID
    title: str
    description: str
    time_create: datetime


class ScenariosGetListSchema(BaseModel):
    result: List[ScenarioGetSchema]
    total: int


class ScenarioPromptsGetBodySchema(BaseModel):
    prompt_id: UUID
    title: str
    description: str
    order: int
    independent: bool
    model: GPTModelName


class ScenarioGetFullSchema(BaseModel):
    uuid: UUID
    title: str
    description: str
    prompts: Optional[List[ScenarioPromptsGetBodySchema]] = []
    time_create: datetime
