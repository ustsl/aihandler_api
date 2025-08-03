from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.prompts.actions import _show_prompt
from src.api.queries.actions.analytics.post import _get_last_query, _save_query
from src.api.queries.actions.balance.put import _transfer_balance
from src.api.queries.modules.story_crop import story_crop_function
from src.api.utils import handle_dal_errors
from src.db.users.dals.transaction import MoneyTransactionUserDal
from src.db.users.models import UserAccountModel
from src.modules.gpt.handler import gpt_handler


@handle_dal_errors
async def _create_query(
    prompt_id: str,
    user_id: str,
    query: str,
    db: AsyncSession,
    story: Optional[list] = [],
    vision: Optional[bool] = False,
):

    prompt = await _show_prompt(prompt_id=prompt_id, user_id=user_id, db=db)
    if prompt.context_story_window > 0:
        story = await story_crop_function(story, prompt.context_story_window)
    else:
        story = []

    if story == []:
        last_query = await _get_last_query(prompt=prompt, query=query, db=db)
        if last_query:
            return {"result": last_query.result, "cost": 0}

    if prompt:
        user_obj_dal = MoneyTransactionUserDal(db, UserAccountModel)
        check_balance = await user_obj_dal.check_balance(user_id)

        if check_balance.get("result"):
            params = {
                "prompt": prompt.prompt,
                "message": query,
                "story": story,
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
                await _transfer_balance(
                    query_user_id=user_id,
                    prompt_user_id=prompt.user_id,
                    cost=cost,
                    session=db,
                )

                await _save_query(
                    user_id=user_id,
                    prompt_id=prompt_id,
                    query=query,
                    result=result.get("result"),
                    db=db,
                )

                await db.commit()
                return result

        else:
            return {"error": "wallet it empty", "status": 403}
        return {"result": "fail", "error": 500}
