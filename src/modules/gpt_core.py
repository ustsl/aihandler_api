import httpx
from fastapi import HTTPException

from src.settings import OPENAI_TOKEN


class GptCalculator:
    def __init__(self):
        pass

    @staticmethod
    def calc(value):
        price = 0.06
        total_cost = (value / 1000) * price
        return total_cost


class CreateGPTQuery:
    OPENAI_API_KEY = OPENAI_TOKEN

    def __init__(self, prompt, message, story, model):
        self._message = message
        self._prompt = prompt
        self._model = model
        self._result = None
        self._price = None
        self._story = story

    async def generate(self):
        try:
            messages = [
                {"role": "system", "content": self._prompt},
                {"role": "user", "content": self._message},
            ]
            if self._story:
                messages = [*messages, *self._story]
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.OPENAI_API_KEY}"},
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
                        c = GptCalculator()
                        self._price = c.calc(int(tokens_amount))
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

    def get_result(self):
        return {"result": self._result, "cost": self._price}


class CreateGPTResponse(CreateGPTQuery):

    def __init__(self, prompt, message, story, model):
        super().__init__(prompt, message, story, model)
