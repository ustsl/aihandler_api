import httpx

from src.modules.gpt.modules.calc import GptTokenCalculator
from src.modules.gpt.modules.exception_wrapper import handle_exceptions
from src.modules.gpt.modules.interface import AIQueryInterface

from src.settings import OPENAI_TOKEN


class CreateGPTImageResponse(AIQueryInterface):
    def __init__(self, params):
        if not OPENAI_TOKEN:
            raise ValueError("OpenAI API key must be defined.")

        self._message = params.get("message")
        self._prompt = params.get("prompt")
        self._model = params.get("model")

        if self._model != "gpt-4o":
            raise ValueError("OpenAI model must be gpt-4o.")

        self._amount = None
        self._result = None
        self._price = None

    @handle_exceptions
    async def generate(self):

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self._prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": self._message,
                            },
                        },
                    ],
                }
            ],
        }

        headers = {"Authorization": f"Bearer {OPENAI_TOKEN}"}

        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            completion = response.json()
            self._result = completion["choices"][0]["message"]["content"]
            usage = completion.get("usage")
            if usage and usage.get("total_tokens"):
                self._amount = usage.get("total_tokens")

    def calc(self):
        calculator = GptTokenCalculator(model=self._model, value=self._amount)
        self._price = calculator.calc()

    def get_result(self):
        return {"result": self._result, "cost": self._price}
