from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DocumentChunk:
    """A normalized piece of source knowledge ready for embedding."""

    id: str
    text: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class RetrievedChunk:
    """A chunk returned by the vector store."""

    text: str
    metadata: dict[str, Any]
    distance: float | None = None


@dataclass(frozen=True)
class RagAnswer:
    """Final response shown to the user."""

    answer: str
    sources: list[RetrievedChunk]
