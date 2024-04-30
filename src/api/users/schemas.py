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


class SettingsData(BaseModel):
    uuid: UUID
    prompt_id: Optional[UUID] = None


class TokenData(BaseModel):
    token_id: UUID
    token: str


class AccountData(BaseModel):
    account_id: UUID
    balance: Decimal


class UserDataExtend(UserDataWithId):

    token: TokenData
    accounts: AccountData
    settings: SettingsData
    is_active: bool


class UserBalance(BaseModel):
    balance: Decimal
