import re
from typing import List, Literal
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
    account_id: uuid.UUID

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


class GPTPromptCreate(BaseModel):
    id: uuid.UUID
    time_create: datetime


class GPTPromptShow(GPTPromptBase):
    uuid: uuid.UUID
    is_active: bool
    time_update: datetime
    is_open: bool


class GPTPromptList(BaseModel):
    total: int
    result: List[GPTPromptShow]
