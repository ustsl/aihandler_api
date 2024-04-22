from api.prompts.actions import _show_prompt
from sqlalchemy.ext.asyncio import AsyncSession
from api.users.actions import _get_user
from api.utils import handle_dal_errors
from modules.gpt_core import CreateGPTResponse
from db.users.dals.transaction import MoneyTransactionDAL
from db.users.models import UserAccountModel


@handle_dal_errors
async def _create_query(prompt_id: str, telegram_id: str, query: str, db: AsyncSession):
    async with db as session:
        async with session.begin():

            user = await _get_user(telegram_id=telegram_id, db=db)
            prompt = await _show_prompt(prompt_id, telegram_id, db)

            if prompt:
                obj_dal = MoneyTransactionDAL(session, UserAccountModel)
                check = await obj_dal.check_balance(
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
                        send = await obj_dal.send(
                            user_account_id=user.accounts.account_id,
                            prompt_account_id=prompt.account_id,
                            money=float(cost),
                        )
                        if send and send["status"] == 201:
                            return gpt_res
                return {"result": "ommm"}
