import re
from typing import List, Optional, Union
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from src.settings import ALLOWED_MODELS

#########################
# BLOCK WITH API MODELS #
#########################


class GPTPromptBase(BaseModel):
    title: str
    description: str
    prompt: str
    model: str
    is_open: bool
    context_story_window: Optional[Union[int, None]]

    @field_validator("model")
    def validate_model(cls, value):
        if not value in ALLOWED_MODELS:
            raise ValueError("Model must be a real GPT model")
        return value

    @field_validator("title")
    def validate_title(cls, value):
        match = re.match(r"^[\w\s-]+$", value)
        if not match:
            raise ValueError(
                "Title must consist only of letters, numbers, dashes, and underscores."
            )
        return value

    # @field_validator("context_story_window")
    # def validate_context_story_window(cls, value):
    #     if type(value) != int or value < 0 or value > 30:
    #         raise ValueError("context_story_window must be lesser 30 and more 0")
    #     return value


class GPTPromptCreate(BaseModel):
    id: UUID
    time_create: datetime


class GPTPromptShow(GPTPromptBase):
    uuid: UUID
    account_id: UUID
    is_active: bool
    time_update: datetime


class GPTPromptList(BaseModel):
    total: int
    result: List[GPTPromptShow]
