from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    project_root: Path = Path(__file__).resolve().parents[2]
    docs_dir: Path = project_root / "docs"
    data_dir: Path = project_root / "data"
    chroma_dir: Path = project_root / "chroma_db"
    collection_name: str = "ace_study_documents"
    embedding_model_name: str = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    top_k: int = int(os.getenv("TOP_K", "5"))


settings = Settings()
