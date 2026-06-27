from __future__ import annotations

import os

from google import genai


class GeminiClient:
    """Minimal Gemini API client using the current Google GenAI SDK."""

    def __init__(self, model_name: str) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured. Create a .env file or export the variable.")
        self._client = genai.Client(api_key=api_key)
        self._model_name = model_name

    def generate(self, prompt: str) -> str:
        response = self._client.models.generate_content(
            model=self._model_name,
            contents=prompt,
        )
        text = getattr(response, "text", None)
        if not text:
            return "No pude generar una respuesta con el modelo configurado."
        return text.strip()
