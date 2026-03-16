import re
from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


TransportType = Literal["http_json", "mcp"]
MethodType = Literal["GET", "POST"]
AuthType = Literal["none", "bearer", "api_key_query"]


class ToolBaseSchema(BaseModel):
    name: str
    description: str
    transport: TransportType = "http_json"
    method: MethodType = "POST"
    url: Optional[str] = None
    input_schema: dict = Field(default_factory=dict)
    headers_template: Optional[dict] = None
    query_template: Optional[dict] = None
    body_template: Optional[dict] = None
    auth_type: AuthType = "none"
    auth_secret_ref: Optional[str] = None
    timeout_sec: int = 15
    max_response_bytes: int = 262144
    is_active: bool = True

    @field_validator("name")
    def validate_name(cls, value):
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]{0,63}$", value):
            raise ValueError("Tool name must match ^[a-zA-Z_][a-zA-Z0-9_]{0,63}$")
        return value

    @field_validator("timeout_sec")
    def validate_timeout(cls, value):
        if value < 1 or value > 60:
            raise ValueError("timeout_sec must be between 1 and 60")
        return value

    @field_validator("max_response_bytes")
    def validate_response_limit(cls, value):
        if value < 1024 or value > 1048576:
            raise ValueError("max_response_bytes must be between 1024 and 1048576")
        return value

    @field_validator("input_schema")
    def validate_input_schema(cls, value):
        if not isinstance(value, dict):
            raise ValueError("input_schema must be an object")
        return value


class ToolCreateSchema(ToolBaseSchema):
    pass


class ToolUpdateSchema(BaseModel):
    description: Optional[str] = None
    transport: Optional[TransportType] = None
    method: Optional[MethodType] = None
    url: Optional[str] = None
    input_schema: Optional[dict] = None
    headers_template: Optional[dict] = None
    query_template: Optional[dict] = None
    body_template: Optional[dict] = None
    auth_type: Optional[AuthType] = None
    auth_secret_ref: Optional[str] = None
    timeout_sec: Optional[int] = None
    max_response_bytes: Optional[int] = None
    is_active: Optional[bool] = None

    @field_validator("timeout_sec")
    def validate_timeout(cls, value):
        if value is not None and (value < 1 or value > 60):
            raise ValueError("timeout_sec must be between 1 and 60")
        return value

    @field_validator("max_response_bytes")
    def validate_response_limit(cls, value):
        if value is not None and (value < 1024 or value > 1048576):
            raise ValueError("max_response_bytes must be between 1024 and 1048576")
        return value


class ToolResponseSchema(ToolBaseSchema):
    uuid: UUID
    account_id: Optional[UUID] = None
    is_deleted: bool
    time_create: datetime
    time_update: datetime


class ToolListSchema(BaseModel):
    result: list[ToolResponseSchema]
    total: int
