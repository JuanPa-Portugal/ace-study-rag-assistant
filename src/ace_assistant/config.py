from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    project_root: Path = Path(__file__).resolve().parents[2]

    # Documentación base del proyecto
    docs_dir: Path = project_root / "docs"
    data_dir: Path = project_root / "data"

    # Documentación subida desde la interfaz
    uploads_dir: Path = project_root / "data" / "uploads"
    upload_docs_dir: Path = uploads_dir / "docs"
    upload_data_dir: Path = uploads_dir / "data"

    # Vector store
    chroma_dir: Path = project_root / "chroma_db"
    collection_name: str = "ace_study_documents"

    # Modelos
    embedding_model_name: str = os.getenv(
        "EMBEDDING_MODEL_NAME",
        "gemini-embedding-2",
    )
    embedding_output_dimensionality: int = int(
        os.getenv("EMBEDDING_OUTPUT_DIMENSIONALITY", "768")
    )
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # Retrieval
    top_k: int = int(os.getenv("TOP_K", "5"))

    def ensure_directories(self) -> None:
        """Create required local directories if they do not exist."""
        for path in [
            self.docs_dir,
            self.data_dir,
            self.upload_docs_dir,
            self.upload_data_dir,
            self.chroma_dir,
        ]:
            path.mkdir(parents=True, exist_ok=True)


settings = Settings()