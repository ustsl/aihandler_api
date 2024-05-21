# Example usage


from src.modules.gpt.modules.response_model import (
    CreateDaleeResponse,
    CreateGPTResponse,
)


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
    else:
        response_model = CreateGPTResponse
    result = await factory(response_model=response_model, params=params)
    return result
