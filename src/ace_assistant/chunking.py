from __future__ import annotations

import re
from hashlib import sha1

from ace_assistant.models import DocumentChunk


def normalize_text(text: str) -> str:
    """Clean extracted text while preserving meaning."""
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    """Split text into overlapping chunks without external dependencies."""
    clean_text = normalize_text(text)
    if not clean_text:
        return []
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks: list[str] = []
    start = 0
    while start < len(clean_text):
        end = min(start + chunk_size, len(clean_text))
        chunk = clean_text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(clean_text):
            break
        start = end - overlap
    return chunks


def build_chunks(raw_items: list[tuple[str, dict[str, str]]]) -> list[DocumentChunk]:
    """Create stable chunk IDs and metadata."""
    chunks: list[DocumentChunk] = []
    for source_idx, (text, metadata) in enumerate(raw_items):
        for chunk_idx, chunk_text in enumerate(split_text(text)):
            base = f"{metadata.get('source_file', 'unknown')}:{source_idx}:{chunk_idx}:{chunk_text[:80]}"
            chunk_id = sha1(base.encode("utf-8")).hexdigest()
            chunk_metadata = {**metadata, "chunk_index": str(chunk_idx)}
            chunks.append(DocumentChunk(id=chunk_id, text=chunk_text, metadata=chunk_metadata))
    return chunks
