from uuid import UUID
from pydantic import BaseModel, EmailStr, field_validator

#########################
# BLOCK WITH API MODELS #
#########################


class UserQueryBase(BaseModel):
    prompt_id: UUID
    query: str

    @field_validator("query")
    def validate_query(cls, value):
        if len(value) > 1000:
            raise ValueError("Query must be lesser 1000 letters")
        return value


class UserQueryResult(BaseModel):
    result: str
    cost: float = None


class UserQueryStore(UserQueryBase):
    user_id: UUID
    result: str
