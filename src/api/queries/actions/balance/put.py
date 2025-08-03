from src.db.users.dals.transaction import (
    MoneyTransactionUserDal,
)
from src.db.users.models import UserAccountModel


async def _decrease_balance(user_id, cost, session):
    user_obj_dal = MoneyTransactionUserDal(session, UserAccountModel)
    decrease = await user_obj_dal.decrease_balance(user_id=user_id, payment=float(cost))
    return decrease.get("result")


async def _return_cashback(user_id, cost, session):
    user_obj_dal = MoneyTransactionUserDal(session, UserAccountModel)
    return_cash = await user_obj_dal.cashback_balance(
        user_id=user_id, payment=float(cost)
    )
    return return_cash


async def _transfer_balance(query_user_id, prompt_user_id, cost, session):
    user_obj_dal = MoneyTransactionUserDal(session, UserAccountModel)
    await user_obj_dal.decrease_balance(user_id=query_user_id, payment=float(cost))
    cashback = await user_obj_dal.cashback_balance(
        user_id=prompt_user_id, payment=float(cost)
    )
    return cashback
