from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ace_assistant.chunking import build_chunks
from ace_assistant.config import settings
from ace_assistant.embeddings import GeminiEmbeddingModel
from ace_assistant.loaders import load_sources
from ace_assistant.vector_store import ChromaVectorStore


def main() -> None:
    raw_items = load_sources(settings.docs_dir, settings.data_dir)
    chunks = build_chunks(raw_items)
    if not chunks:
        raise RuntimeError("No chunks were generated from the source files.")

    embedding_model = GeminiEmbeddingModel(
    model_name=settings.embedding_model_name,
    output_dimensionality=settings.embedding_output_dimensionality,
)
    embeddings = embedding_model.embed_documents([chunk.text for chunk in chunks])

    store = ChromaVectorStore(settings.chroma_dir, settings.collection_name)
    store.reset_collection()
    store.add_chunks(chunks, embeddings)

    print(f"Index built successfully: {len(chunks)} chunks stored in {settings.chroma_dir}")


if __name__ == "__main__":
    main()
