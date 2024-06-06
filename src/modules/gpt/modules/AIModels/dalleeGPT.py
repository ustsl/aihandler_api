import httpx

from src.modules.gpt.modules.calc import GptImageCalculator
from src.modules.gpt.modules.exception_wrapper import handle_exceptions
from src.modules.gpt.modules.interface import AIQueryInterface
from src.modules.gpt.modules.schemas import TuningModel
from src.settings import OPENAI_TOKEN


class CreateDaleeResponse(AIQueryInterface):
    def __init__(self, params):
        if not OPENAI_TOKEN:
            raise ValueError("OpenAI API key must be defined.")
        self._prompt = params.get("prompt")
        self._message = params.get("message")

        tuning = params.get("tuning", {})

        validated_tuning = TuningModel(**tuning)

        self._style = validated_tuning.style
        self._size = validated_tuning.size
        self._quality = validated_tuning.quality

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
