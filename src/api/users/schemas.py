from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

#########################
# BLOCK WITH API MODELS #
#########################


class UserDataId(BaseModel):
    uuid: UUID


class UserDataBase(BaseModel):
    telegram_id: str


class UserDataWithId(UserDataBase, UserDataId):
    pass


class SettingsGetData(BaseModel):
    prompt_id: Optional[UUID] = None
    language: Optional[str] = None


class SettingsData(SettingsGetData):
    uuid: UUID


class TokenData(BaseModel):
    uuid: UUID
    token: str


class AccountData(BaseModel):
    uuid: UUID
    balance: Decimal


class TokenData(BaseModel):
    uuid: UUID
    token: UUID


class UserBalance(BaseModel):
    balance: Decimal


class UserDataExtend(UserDataWithId):
    token: TokenData
    accounts: AccountData
    settings: SettingsData
    is_active: bool
