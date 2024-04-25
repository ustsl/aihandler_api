import httpx
from fastapi import HTTPException

from settings import OPENAI_TOKEN


class GptCalculator:
    def __init__(self):
        pass

    @staticmethod
    def calc(value):
        price = 0.05
        total_cost = (value / 1000) * price
        return total_cost


class CreateGPTQuery:
    OPENAI_API_KEY = OPENAI_TOKEN
    CLIENT = httpx.AsyncClient()

    def __init__(self, prompt, message, model):
        self._message = message
        self._prompt = prompt
        self._model = model
        self._result = None
        self._price = None

    async def generate(self):
        try:
            response = await self.CLIENT.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.OPENAI_API_KEY}"},
                json={
                    "model": self._model,
                    "messages": [
                        {"role": "system", "content": self._prompt},
                        {"role": "user", "content": self._message},
                    ],
                },
            )
            response.raise_for_status()
            completion = response.json()

            self._result = completion["choices"][0]["message"]["content"]
            usage = completion.get("usage")
            if usage:
                tokens_amount = usage.get("total_tokens")
                if tokens_amount:
                    c = GptCalculator()
                    self._price = c.calc(int(tokens_amount))
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

    def get_result(self):
        return {"result": self._result, "cost": self._price}


class CreateGPTResponse(CreateGPTQuery):

    def __init__(self, prompt, message, model):
        super().__init__(prompt, message, model)
