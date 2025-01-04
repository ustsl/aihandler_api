import re
from pydantic import BaseModel, field_validator


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
