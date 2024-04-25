from sqlalchemy.ext.asyncio import AsyncSession

from src.api.prompts.actions import _show_prompt
from src.api.users.actions import _get_user
from src.api.utils import handle_dal_errors

from src.db.users.dals.transaction import (
    MoneyTransactionUserDal,
    MoneyTransactionRecipientDAL,
)
from src.db.users.models import UserAccountModel

from src.modules.gpt_core import CreateGPTResponse


@handle_dal_errors
async def _create_query(prompt_id: str, telegram_id: str, query: str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            user = await _get_user(telegram_id=telegram_id, db=db)
            prompt = await _show_prompt(
                prompt_id=prompt_id, telegram_id=telegram_id, db=db
            )

            if prompt and prompt != 1:
                user_obj_dal = MoneyTransactionUserDal(session, UserAccountModel)
                check = await user_obj_dal.check_balance(
                    user_account_id=user.accounts.account_id
                )

                if check.get("result"):
                    gpt = CreateGPTResponse(
                        prompt=prompt.prompt,
                        message=query,
                        model="gpt-3.5-turbo",
                    )
                    await gpt.generate()
                    gpt_res = gpt.get_result()
                    cost = gpt_res.get("cost")
                    if cost:
                        decrease = await user_obj_dal.decrease_balance(float(cost))
                        if decrease.get("result"):
                            recipient_obj_dal = MoneyTransactionRecipientDAL(
                                session, UserAccountModel
                            )
                            send = await recipient_obj_dal.send(
                                prompt_account_id=prompt.account_id,
                                money=float(cost),
                            )
                        if send and send["status"] == 201:
                            return gpt_res
                else:
                    return {"error": "wallet it empty", "status": 403}
                return {"result": "fail", "error": 500}