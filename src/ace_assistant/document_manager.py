from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from ace_assistant.config import settings


DOC_EXTENSIONS = {".pdf", ".md", ".txt"}
DATA_EXTENSIONS = {".csv"}
SUPPORTED_EXTENSIONS = DOC_EXTENSIONS | DATA_EXTENSIONS


@dataclass(frozen=True)
class ManagedDocument:
    name: str
    path: Path
    category: str
    origin: str
    size_kb: float
    deletable: bool


def ensure_upload_dirs() -> None:
    """Ensure upload directories exist."""
    settings.ensure_directories()


def save_uploaded_files(uploaded_files: Iterable[Any]) -> list[Path]:
    """
    Save files uploaded from Streamlit into controlled upload folders.

    PDF, TXT and MD files go to data/uploads/docs.
    CSV files go to data/uploads/data.
    """
    ensure_upload_dirs()
    saved_paths: list[Path] = []

    for uploaded in uploaded_files:
        filename = Path(uploaded.name).name
        suffix = Path(filename).suffix.lower()

        if suffix in DOC_EXTENSIONS:
            target = settings.upload_docs_dir / filename
        elif suffix in DATA_EXTENSIONS:
            target = settings.upload_data_dir / filename
        else:
            raise ValueError(f"Tipo de archivo no soportado: {filename}")

        target.write_bytes(uploaded.getbuffer())
        saved_paths.append(target)

    return saved_paths


def list_documents() -> list[ManagedDocument]:
    """Return base and uploaded documents visible to the assistant."""
    ensure_upload_dirs()
    items: list[ManagedDocument] = []

    directories = [
        (settings.docs_dir, "base"),
        (settings.data_dir, "base"),
        (settings.upload_docs_dir, "subido"),
        (settings.upload_data_dir, "subido"),
    ]

    for directory, origin in directories:
        if not directory.exists():
            continue

        for path in sorted(directory.iterdir()):
            if not path.is_file():
                continue

            suffix = path.suffix.lower()
            if suffix not in SUPPORTED_EXTENSIONS:
                continue

            category = "documento" if suffix in DOC_EXTENSIONS else "dataset"

            items.append(
                ManagedDocument(
                    name=path.name,
                    path=path,
                    category=category,
                    origin=origin,
                    size_kb=round(path.stat().st_size / 1024, 2),
                    deletable=(origin == "subido"),
                )
            )

    return items


def delete_uploaded_document(path_str: str) -> None:
    """Delete only files located inside controlled upload folders."""
    path = Path(path_str).resolve()

    allowed_dirs = [
        settings.upload_docs_dir.resolve(),
        settings.upload_data_dir.resolve(),
    ]

    if not any(str(path).startswith(str(base)) for base in allowed_dirs):
        raise ValueError("Solo se pueden eliminar archivos subidos desde la interfaz.")

    if path.exists():
        path.unlink()