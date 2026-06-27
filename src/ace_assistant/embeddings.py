from __future__ import annotations

from sentence_transformers import SentenceTransformer


class LocalEmbeddingModel:
    """Small local embedding model for a zero-cost RAG prototype."""

    def __init__(self, model_name: str) -> None:
        self._model = SentenceTransformer(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return vectors.tolist()

    def embed_query(self, text: str) -> list[float]:
        vectors = self.embed_documents([text])
        if not vectors:
            raise ValueError("Cannot embed an empty query")
        return vectors[0]
