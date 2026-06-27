from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb

from ace_assistant.models import DocumentChunk, RetrievedChunk


class ChromaVectorStore:
    """Persistent Chroma vector store wrapper."""

    def __init__(self, persist_dir: Path, collection_name: str) -> None:
        self._client = chromadb.PersistentClient(path=str(persist_dir))
        self._collection = self._client.get_or_create_collection(name=collection_name)

    def reset_collection(self) -> None:
        name = self._collection.name
        self._client.delete_collection(name)
        self._collection = self._client.get_or_create_collection(name=name)

    def add_chunks(self, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings must have the same length")
        if not chunks:
            return

        self._collection.add(
            ids=[chunk.id for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            metadatas=[chunk.metadata for chunk in chunks],
            embeddings=embeddings,
        )

    def query(self, query_embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        result: dict[str, Any] = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        return [
            RetrievedChunk(text=doc, metadata=meta or {}, distance=dist)
            for doc, meta, dist in zip(documents, metadatas, distances)
        ]

    def count(self) -> int:
        return int(self._collection.count())
