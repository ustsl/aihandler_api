from decimal import Decimal
import uuid
from pydantic import BaseModel, field_validator

#########################
# BLOCK WITH API MODELS #
#########################


class UserDataId(BaseModel):
    id: uuid.UUID


class UserDataBase(BaseModel):
    telegram_id: str


class UserDataWithId(UserDataBase, UserDataId):
    pass


class TokenData(BaseModel):
    token_id: uuid.UUID
    token: str


class AccountData(BaseModel):
    account_id: uuid.UUID
    balance: str


class UserDataExtend(UserDataWithId):
    token: TokenData
    account: AccountData
