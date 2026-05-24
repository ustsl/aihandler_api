import httpx

from src.modules.gpt.modules.calc import GptTokenCalculator
from src.modules.gpt.modules.exception_wrapper import handle_exceptions
from src.modules.gpt.modules.interface import AIQueryInterface
from src.settings import OPENAI_TOKEN


class CreateGPTAudioTranscriptionResponse(AIQueryInterface):
    def __init__(self, params):
        if not OPENAI_TOKEN:
            raise ValueError("OpenAI API key must be defined.")

        self._file_bytes = params.get("file_bytes")
        self._filename = params.get("filename") or "audio"
        self._content_type = params.get("content_type") or "application/octet-stream"
        self._prompt = params.get("prompt")
        self._message = params.get("message")
        self._model = params.get("model")

        self._amount = 0
        self._result = None
        self._price = None

    def _build_prompt(self) -> str | None:
        parts = [part for part in (self._prompt, self._message) if part]
        if not parts:
            return None
        return "\n\n".join(parts)

    @handle_exceptions
    async def generate(self):
        data = {
            "model": self._model,
            "response_format": "json",
        }
        prompt = self._build_prompt()
        if prompt:
            data["prompt"] = prompt

        files = {
            "file": (self._filename, self._file_bytes, self._content_type),
        }

        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {OPENAI_TOKEN}"},
                data=data,
                files=files,
            )
            response.raise_for_status()
            completion = response.json()

            self._result = completion.get("text")
            usage = completion.get("usage") or {}
            self._amount = int(usage.get("total_tokens") or 0)

    def calc(self):
        calculator = GptTokenCalculator(model=self._model, value=self._amount)
        self._price = calculator.calc()

    def get_result(self):
        return {"result": self._result, "cost": self._price}
