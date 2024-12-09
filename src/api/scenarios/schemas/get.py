import re
from typing import List, Optional, Union
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

from src.settings import ALLOWED_MODELS

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
