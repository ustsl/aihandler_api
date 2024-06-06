# Example usage

from src.modules.gpt.modules.AIModels.baseGPT import CreateGPTResponse
from src.modules.gpt.modules.AIModels.dalleeGPT import CreateDaleeResponse
from src.modules.gpt.modules.AIModels.visionGPT import CreateGPTImageResponse


async def factory(response_model: str, params: dict) -> dict:
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
    if params.get("model") == "dall-e-3":
        response_model = CreateDaleeResponse
    elif params.get("model") == "gpt-4o" and params.get("vision") == True:
        response_model = CreateGPTImageResponse
    else:
        response_model = CreateGPTResponse
    result = await factory(response_model=response_model, params=params)
    return result
