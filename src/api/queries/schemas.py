from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

#########################
# BLOCK WITH API MODELS #
#########################


class UserQueryBase(BaseModel):
    prompt_id: UUID
    query: str
    vision: bool = None
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
    uuid: UUID
    result: str


class UserQueryScenarioBase(BaseModel):
    scenario_id: UUID
    query: str

    @field_validator("query")
    def validate_query(cls, value):
        if len(value) > 50000:
            raise ValueError("Query must be lesser 50000 letters")
        return value


class UserQueryScenarioResult(BaseModel):
    results: Optional[List[UserQueryResult]] = None
