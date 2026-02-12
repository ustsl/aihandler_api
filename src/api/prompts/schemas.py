import re
from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator

from src.settings import GPTModelName

#########################
# BLOCK WITH API MODELS #
#########################


class GPTPromptBase(BaseModel):
    title: str
    description: str
    prompt: str
    model: GPTModelName
    is_open: bool
    context_story_window: Optional[Union[int, None]]
    tuning: Optional[Union[dict, None]] = None

    @field_validator("title")
    def validate_title(cls, value):
        match = re.match(r"^[\w\s.-]+$", value)

        if not match:
            raise ValueError(
                "Title must consist only of letters, numbers, dashes, and underscores."
            )
        return value

    @field_validator("context_story_window")
    def validate_context_story_window(cls, value):
        if value:
            if value < 0 or value > 50:
                raise ValueError("context_story_window must be lesser 50 and more 0")
        return value


class GPTPromptCreate(BaseModel):
    id: UUID
    time_create: datetime


class GPTPromptShow(GPTPromptBase):
    uuid: UUID
    account_id: UUID
    is_active: bool
    time_update: datetime


class GPTPromptShowFull(GPTPromptShow):
    user_id: UUID


class GPTPromptList(BaseModel):
    total: int
    result: List[GPTPromptShow]
