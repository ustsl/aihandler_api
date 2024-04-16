import re
from typing import Literal
import uuid
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator

from settings import ALLOWED_MODELS

#########################
# BLOCK WITH API MODELS #
#########################


class GPTPromptBase(BaseModel):
    title: str
    description: str
    prompt: str
    model: str
    account_id: str

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


class GPTPromptShortShow(GPTPromptBase):
    id: uuid.UUID
    time_create: datetime


class GPTPromptShow(GPTPromptShortShow):
    is_active: bool
    time_update: datetime
    model: str


class GPTPromptCreate(GPTPromptBase):
    pass
