from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


class GeminiEmbeddingModel:
    """Embedding model using Gemini API to avoid local PyTorch dependencies."""

    def __init__(self, model_name: str, output_dimensionality: int = 768) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key or api_key == "your_api_key_here":
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Create a .env file and add your Gemini API key."
            )

        self._client = genai.Client(api_key=api_key)
        self._model_name = model_name
        self._output_dimensionality = output_dimensionality

    def _embed_text(self, text: str) -> list[float]:
        response = self._client.models.embed_content(
            model=self._model_name,
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=self._output_dimensionality
            ),
        )

        if not response.embeddings:
            raise RuntimeError("Gemini did not return embeddings.")

        return list(response.embeddings[0].values)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        embeddings: list[list[float]] = []

        for text in texts:
            prepared_text = f"title: ACE Study Assistant | text: {text}"
            embeddings.append(self._embed_text(prepared_text))

        return embeddings

    def embed_query(self, text: str) -> list[float]:
        normalized_text = text.strip()

        if not normalized_text:
            raise ValueError("Cannot embed an empty query.")

        prepared_query = f"task: question answering | query: {normalized_text}"
        return self._embed_text(prepared_query)
