from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader

from ace_assistant.models import DocumentChunk


def read_pdf(path: Path) -> list[tuple[str, dict[str, str]]]:
    """Extract text from each PDF page with basic metadata."""
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    reader = PdfReader(str(path))
    pages: list[tuple[str, dict[str, str]]] = []
    for idx, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append((text, {"source_file": path.name, "document_type": "pdf", "page": str(idx)}))
    return pages


def read_csv_as_rows(path: Path) -> list[tuple[str, dict[str, str]]]:
    """Convert CSV rows into natural-language records for embedding."""
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    records: list[tuple[str, dict[str, str]]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for idx, row in enumerate(reader, start=1):
            text = "; ".join(f"{key}: {value}" for key, value in row.items() if value)
            metadata = {
                "source_file": path.name,
                "document_type": "csv",
                "row": str(idx),
            }
            if "dominio" in row:
                metadata["domain"] = row.get("dominio", "")
            if "categoria" in row:
                metadata["category"] = row.get("categoria", "")
            records.append((text, metadata))
    return records


def load_sources(docs_dir: Path, data_dir: Path) -> list[tuple[str, dict[str, str]]]:
    """Load all supported source files from docs/ and data/."""
    items: list[tuple[str, dict[str, str]]] = []

    for pdf_path in sorted(docs_dir.glob("*.pdf")):
        items.extend(read_pdf(pdf_path))

    for csv_path in sorted(data_dir.glob("*.csv")):
        items.extend(read_csv_as_rows(csv_path))

    if not items:
        raise RuntimeError("No PDF or CSV sources were found. Add files to docs/ or data/.")
    return items
