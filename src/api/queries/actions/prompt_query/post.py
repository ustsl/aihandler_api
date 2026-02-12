from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.prompts.actions import _show_prompt
from src.api.queries.actions.analytics.post import _get_last_query, _save_query
from src.api.queries.actions.balance.put import _transfer_balance
from src.api.queries.modules.quality_metrics import build_query_quality_metrics
from src.api.queries.modules.story_crop import story_crop_function
from src.api.utils import handle_dal_errors
from src.db.users.dals.transaction import MoneyTransactionUserDal
from src.db.users.models import UserAccountModel
from src.modules.gpt.handler import gpt_handler


def _build_query_payload(
    query: str, result: str, cost: float = 0.0, cached: bool = False
) -> dict:
    return {
        "result": result,
        "cost": round(float(cost), 6),
        "quality_metrics": build_query_quality_metrics(
            query=query, result=result, cached=cached
        ),
    }


@handle_dal_errors
async def _create_query(
    prompt_id: str,
    user_id: str,
    query: str,
    db: AsyncSession,
    story: Optional[list] = None,
    vision: Optional[bool] = False,
):
    prompt = await _show_prompt(prompt_id=prompt_id, user_id=user_id, db=db)
    prepared_story = story or []

    if prompt.context_story_window > 0:
        prepared_story = await story_crop_function(
            prepared_story, prompt.context_story_window
        )
    else:
        prepared_story = []

    if not prepared_story:
        last_query = await _get_last_query(prompt=prompt, query=query, db=db)
        if last_query and last_query.result:
            return _build_query_payload(
                query=query,
                result=last_query.result,
                cost=0.0,
                cached=True,
            )

    user_obj_dal = MoneyTransactionUserDal(db, UserAccountModel)
    check_balance = await user_obj_dal.check_balance(user_id)
    if not check_balance.get("result"):
        return {"error": "wallet it empty", "status": 403}

    params = {
        "prompt": prompt.prompt,
        "message": query,
        "story": prepared_story,
        "model": prompt.model,
        "tuning": prompt.tuning,
        "vision": vision,
    }

    model_response = await gpt_handler(params)

    if model_response.get("error"):
        return {"error": model_response.get("error"), "status": 500}

    result_text = model_response.get("result")
    if not result_text:
        return {"error": "Empty model response", "status": 500}

    cost = float(model_response.get("cost") or 0)

    if cost > 0:
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
        result=result_text,
        db=db,
    )
    await db.commit()

    return _build_query_payload(query=query, result=result_text, cost=cost, cached=False)
