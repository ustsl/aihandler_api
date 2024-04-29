from decimal import Decimal
import uuid
from pydantic import BaseModel, field_validator

#########################
# BLOCK WITH API MODELS #
#########################


class UserDataId(BaseModel):
    uuid: uuid.UUID


class UserDataBase(BaseModel):
    telegram_id: str


class UserDataWithId(UserDataBase, UserDataId):
    pass


class TokenData(BaseModel):
    token_id: uuid.UUID
    token: str


class AccountData(BaseModel):
    account_id: uuid.UUID
    balance: Decimal


class UserDataExtend(UserDataWithId):

    token: TokenData
    accounts: AccountData
    is_active: bool


class UserBalance(BaseModel):
    balance: Decimal
