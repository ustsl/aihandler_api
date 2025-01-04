from sqlalchemy.ext.asyncio import AsyncSession

from src.api.prompts.actions import _show_prompt
from src.api.queries.actions.analytics.post import _save_query
from src.api.queries.actions.balance.put import _transfer_balance
from src.api.queries.modules.story_crop import story_crop_function
from src.api.users.actions.base_user_actions import _get_user
from src.api.utils import handle_dal_errors
from src.db.users.dals.transaction import MoneyTransactionUserDal
from src.db.users.models import UserAccountModel
from src.modules.gpt.handler import gpt_handler


@handle_dal_errors
async def _create_query(
    prompt_id: str,
    telegram_id: str,
    query: str,
    story: list,
    vision: bool,
    db: AsyncSession,
):
    async with db as session:
        async with session.begin():
            user = await _get_user(telegram_id=telegram_id, db=db)
            prompt = await _show_prompt(
                prompt_id=prompt_id, telegram_id=telegram_id, db=db
            )
            if prompt.context_story_window > 0:
                story_crop = await story_crop_function(
                    story, prompt.context_story_window
                )
            else:
                story_crop = []

            if prompt:
                user_obj_dal = MoneyTransactionUserDal(session, UserAccountModel)
                check_balance = await user_obj_dal.check_balance(user.accounts.uuid)
                if check_balance.get("result"):
                    params = {
                        "prompt": prompt.prompt,
                        "message": query,
                        "story": story_crop,
                        "model": prompt.model,
                        "tuning": prompt.tuning,
                        "vision": vision,
                    }

                    result = await gpt_handler(params)
                    if result.get("error"):
                        result["status"] = 500
                        return result

                    cost = result.get("cost")

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
                                result=result.get("result"),
                                db=session,
                            )
                            return result
                else:
                    return {"error": "wallet it empty", "status": 403}
                return {"result": "fail", "error": 500}


@handle_dal_errors
async def _create_query_safe(
    user,
    prompt,
    query: str,
    db: AsyncSession,
):

    user_obj_dal = MoneyTransactionUserDal(db, UserAccountModel)
    check_balance = await user_obj_dal.check_balance(user.accounts.uuid)

    prompt = await _show_prompt(
        prompt_id=prompt.prompt_id, telegram_id=user.telegram_id, db=db
    )

    if check_balance.get("result"):
        params = {
            "prompt": prompt.prompt,
            "message": query,
            "story": [],
            "model": prompt.model,
            "tuning": None,
        }

        result = await gpt_handler(params)
        if result.get("error"):
            result["status"] = 500
            return result

        cost = result.get("cost")
        if cost:
            decrease_proccess = await _transfer_balance(
                user_obj_dal=user_obj_dal,
                account_id=prompt.account_id,
                cost=cost,
                session=db,
            )

        if decrease_proccess and decrease_proccess.get("status") == 201:
            await _save_query(
                user_id=user.uuid,
                prompt_id=prompt.uuid,
                query=query,
                result=result.get("result"),
                db=db,
            )
            await db.commit()
            return result
    else:
        return {"error": "wallet it empty", "status": 403}
    return {"result": "fail", "error": 500}
