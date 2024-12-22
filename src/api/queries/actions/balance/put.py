from src.db.users.dals.transaction import MoneyTransactionRecipientDAL
from src.db.users.models import UserAccountModel


async def _transfer_balance(user_obj_dal, account_id, cost, session):
    decrease = await user_obj_dal.decrease_balance(float(cost))
    if decrease.get("result"):
        recipient_obj_dal = MoneyTransactionRecipientDAL(session, UserAccountModel)
        send = await recipient_obj_dal.send(
            prompt_account_id=account_id,
            money=float(cost),
        )
        return send
    return None
