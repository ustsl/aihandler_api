import httpx
from fastapi import HTTPException

from settings import OPENAI_TOKEN


class CreateGPTQuery:
    OPENAI_API_KEY = OPENAI_TOKEN
    CLIENT = httpx.AsyncClient()

    def __init__(self, prompt, message, model):
        self._message = message
        self._prompt = prompt
        self._model = model
        self._result = None

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
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

    def get_result(self):
        return {"result": self._result}


class CreateGPTResponse(CreateGPTQuery):

    def __init__(self, prompt, message, model):
        super().__init__(prompt, message, model)
