import httpx
from fastapi import HTTPException

from src.settings import OPENAI_TOKEN


model_price = {
    "gpt-3.5-turbo": 0.03,
    "gpt-3.5-turbo-0125": 0.03,
    "gpt-4-turbo": 0.08,
    "gpt-4-turbo-2024-04-09": 0.08,
    "gpt-4o": 0.08,
}


class GptCalculator:
    def __init__(self, model):
        self.model = model
        self.price_per_unit = self._get_price_for_model()

    def _get_price_for_model(self):
        default_price = 0.07
        return model_price.get(self.model, default_price)

    def calc(self, value):
        total_cost = (value / 1000) * self.price_per_unit
        return total_cost


class CreateGPTQuery:
    def __init__(self, prompt, message, story, model):
        if not OPENAI_TOKEN:
            raise ValueError("OpenAI API key must be defined.")

        self._message = message
        self._prompt = prompt
        self._model = model
        self._result = None
        self._price = None
        self._story = story

    async def generate(self):
        try:
            messages = [{"role": "system", "content": self._prompt}]
            if self._story:
                messages.extend(self._story)
            messages.append({"role": "user", "content": self._message})

            async with httpx.AsyncClient(timeout=180) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {OPENAI_TOKEN}"},
                    json={
                        "model": self._model,
                        "messages": messages,
                    },
                )
                response.raise_for_status()
                completion = response.json()

                self._result = completion["choices"][0]["message"]["content"]
                usage = completion.get("usage")
                if usage:
                    tokens_amount = usage.get("total_tokens")
                    if tokens_amount:
                        c = GptCalculator(self._model)
                        self._price = c.calc(int(tokens_amount))
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An unexpected error occurred: {str(e)}"
            )

    def get_result(self):
        return {"result": self._result, "cost": self._price}


class CreateGPTResponse(CreateGPTQuery):

    def __init__(self, prompt, message, story, model):
        super().__init__(prompt, message, story, model)
