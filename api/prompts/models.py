import re
import uuid
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator

#########################
# BLOCK WITH API MODELS #
#########################


class GPTPropmptBase(BaseModel):
    title: str
    description: str
    prompt: str

    @field_validator("title")
    def validate_title(cls, value):
        match = re.match(r"^[\w\s-]+$", value)
        if not match:
            raise ValueError(
                "Title must consist only of letters, numbers, dashes, and underscores."
            )
        return value


class GPTPromptShortShow(GPTPropmptBase):
    id: uuid.UUID
    time_create: datetime


class GPTPromptShow(GPTPromptShortShow):
    is_active: bool
    time_update: datetime


class GPTPromptCreate(GPTPropmptBase):
    pass


class GPTPromptUse(BaseModel):
    id: uuid.UUID
    query: str


class GPTPromptUseResult(BaseModel):
    pass
