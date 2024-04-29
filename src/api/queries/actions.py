from sqlalchemy.ext.asyncio import AsyncSession

from src.api.prompts.actions import _show_prompt
from src.api.queries.modules.story_crop import story_crop_function
from src.api.users.actions import _get_user, _get_user_account
from src.api.utils import handle_dal_errors

from src.db.queries.models import QueryModel
from src.db.users.dals.transaction import (
    MoneyTransactionUserDal,
    MoneyTransactionRecipientDAL,
)
from src.db.users.models import UserAccountModel
from src.db.queries.dals import QueryDAL


from src.modules.gpt_core import CreateGPTResponse

from uuid import UUID


async def _save_query(
    user_id: UUID, prompt_id: UUID, query: str, result: str, db: AsyncSession
):
    query_dal = QueryDAL(db_session=db, model=QueryModel)
    result = await query_dal.create(
        user_id=user_id, prompt_id=prompt_id, query=query, result=result
    )


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


@handle_dal_errors
async def _create_query(
    prompt_id: str, telegram_id: str, query: str, story: list, db: AsyncSession
):
    async with db as session:
        async with session.begin():
            user = await _get_user(telegram_id=telegram_id, db=db)
            prompt = await _show_prompt(
                prompt_id=prompt_id, telegram_id=telegram_id, db=db
            )

            story_crop = await story_crop_function(story, prompt.context_story_window)

            if prompt:
                user_obj_dal = MoneyTransactionUserDal(session, UserAccountModel)
                check = await user_obj_dal.check_balance(user.accounts.account_id)
                if check.get("result"):

                    gpt = CreateGPTResponse(
                        prompt=prompt.prompt,
                        message=query,
                        story=story_crop,
                        model=prompt.model,
                    )

                    await gpt.generate()
                    gpt_res = gpt.get_result()
                    cost = gpt_res.get("cost")
                    if cost:

                        decrease_proccess = await _transfer_balance(
                            user_obj_dal=user_obj_dal,
                            account_id=prompt.account_id,
                            cost=cost,
                            session=session,
                        )

                        if decrease_proccess and decrease_proccess.get("status") == 201:

                            await _save_query(
                                user_id=user.uuid,
                                prompt_id=prompt_id,
                                query=query,
                                result=gpt_res.get("result"),
                                db=session,
                            )
                            return gpt_res
                else:
                    return {"error": "wallet it empty", "status": 403}
                return {"result": "fail", "error": 500}


@handle_dal_errors
async def _show_queries(
    db: AsyncSession,
    telegram_id: str = None,
    offset: int = 0,
):
    if telegram_id:
        user = await _get_user(telegram_id=telegram_id, db=db)
        # TODO: create logic
    obj_dal = QueryDAL(db, QueryModel)
    results = await obj_dal.list(offset=offset, order_param="time_create")
    return results
