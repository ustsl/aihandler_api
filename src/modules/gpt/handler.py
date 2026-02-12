from src.modules.gpt.modules.AIModels.baseGPT import CreateGPTResponse
from src.modules.gpt.modules.AIModels.dalleeGPT import CreateDaleeResponse
from src.modules.gpt.modules.AIModels.visionGPT import CreateGPTImageResponse


def _resolve_response_model(params: dict):
    if params.get("model") == "dall-e-3":
        return CreateDaleeResponse
    if params.get("model") == "gpt-4o" and params.get("vision") is True:
        return CreateGPTImageResponse
    return CreateGPTResponse


async def factory(response_model, params: dict) -> dict:
    try:
        query = response_model(params)
        await query.generate()
        query.calc()
        return query.get_result()
    except Exception as e:
        return {
            "error": str(e),
        }


async def gpt_handler(params):
    response_model = _resolve_response_model(params=params)
    return await factory(response_model=response_model, params=params)
