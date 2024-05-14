from uuid import UUID
from pydantic import BaseModel, field_validator
from typing import Optional, List

#########################
# BLOCK WITH API MODELS #
#########################


class UserQueryBase(BaseModel):
    prompt_id: UUID
    query: str
    story: Optional[List[dict]] = None

    @field_validator("query")
    def validate_query(cls, value):
        if len(value) > 50000:
            raise ValueError("Query must be lesser 50000 letters")
        return value


class UserQueryResult(BaseModel):
    result: str
    cost: float = None


class UserQueryStore(UserQueryBase):
    user_id: UUID
    result: str
