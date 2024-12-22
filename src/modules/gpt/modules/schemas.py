from typing import Dict, Optional

from pydantic import BaseModel, Field, field_validator

from src.modules.gpt.modules.param import (dalee_quality, dalee_size,
                                           dalee_style)


class TuningModel(BaseModel):
    style: Optional[str] = Field(None)
    size: Optional[str] = Field(None)
    quality: Optional[str] = Field(None)

    @field_validator("style")
    def validate_style(cls, value):
        if value is not None and value not in dalee_style:
            raise ValueError(f"Invalid style value: {value}")
        return value

    @field_validator("size")
    def validate_size(cls, value):
        if value is not None and value not in dalee_size:
            raise ValueError(f"Invalid size value: {value}")
        return value

    @field_validator("quality")
    def validate_quality(cls, value):
        if value is not None and value not in dalee_quality:
            raise ValueError(f"Invalid quality value: {value}")
        return value
