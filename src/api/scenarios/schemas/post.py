import re
from typing import List, Optional, Union
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from src.settings import ALLOWED_MODELS

#########################
# BLOCK WITH API MODELS #
#########################


class ScenarioPostSchema(BaseModel):
    title: str
    description: str

    @field_validator("title")
    def validate_title(cls, value):
        match = re.match(r"^[\w\s.-]+$", value)

        if not match:
            raise ValueError(
                "Title must consist only of letters, numbers, dashes, and underscores."
            )
        return value

    class Config:
        extra = "forbid"
