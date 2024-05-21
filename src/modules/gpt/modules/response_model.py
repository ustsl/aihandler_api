import httpx

from src.modules.gpt.modules.calc import GptImageCalculator, GptTokenCalculator
from src.modules.gpt.modules.exception_wrapper import handle_exceptions
from src.modules.gpt.modules.interface import AIQueryInterface
from src.settings import OPENAI_TOKEN


class CreateGPTResponse(AIQueryInterface):
    def __init__(self, params):
        if not OPENAI_TOKEN:
            raise ValueError("OpenAI API key must be defined.")
        self._message = params.get("message")
        self._prompt = params.get("prompt")
        self._model = params.get("model")
        self._story = params.get("story")

        self._amount = None
        self._result = None
        self._price = None

    @handle_exceptions
    async def generate(self):
        messages = [{"role": "system", "content": self._prompt}]
        if self._story:
            messages.extend(self._story)
        messages.append({"role": "user", "content": self._message})

        async with httpx.AsyncClient(timeout=300) as client:
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
            if usage and usage.get("total_tokens"):
                self._amount = usage.get("total_tokens")

    def calc(self):
        calculator = GptTokenCalculator(model=self._model, value=self._amount)
        self._price = calculator.calc()

    def get_result(self):
        return {"result": self._result, "cost": self._price}


class CreateDaleeResponse(AIQueryInterface):
    def __init__(self, params):
        if not OPENAI_TOKEN:
            raise ValueError("OpenAI API key must be defined.")
        self._prompt = params.get("prompt")
        self._message = params.get("message")

        tuning = params.get("tuning", {})
        self._style = tuning.get("style")
        self._size = tuning.get("size")
        self._quality = tuning.get("quality")

        self._result = None

    @handle_exceptions
    async def generate(self):
        headers = {
            "Authorization": f"Bearer {OPENAI_TOKEN}",
            "Content-Type": "application/json",
        }
        json_data = {
            "prompt": f"{self._prompt} {self._message}",
            "num_images": 1,
            "model": "dall-e-3",
        }

        if self._quality:
            json_data["quality"] = self._quality
        if self._size:
            json_data["size"] = self._size
        if self._style:
            json_data["style"] = self._style

        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=json_data,
            )
            response.raise_for_status()
            completion = response.json()
            self._result = completion["data"][0]["url"]

    def calc(self):
        calculator = GptImageCalculator(quality=self._quality, size=self._size)
        self._price = calculator.calc()

    def get_result(self):
        return {"result": self._result, "cost": self._price}
