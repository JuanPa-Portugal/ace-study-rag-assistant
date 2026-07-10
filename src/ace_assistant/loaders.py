from __future__ import annotations

import csv
from collections.abc import Iterable
from pathlib import Path

SourceInput = Path | Iterable[Path]


def _as_paths(value: SourceInput) -> list[Path]:
    """Normalize one path or many paths into a list of Path objects."""
    if isinstance(value, Path):
        return [value]

    return list(value)


def read_pdf(path: Path) -> list[tuple[str, dict[str, str]]]:
    """Extract text from each PDF page with basic metadata."""
    from pypdf import PdfReader

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    reader = PdfReader(str(path))
    pages: list[tuple[str, dict[str, str]]] = []

    for idx, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append(
                (
                    text,
                    {
                        "source_file": path.name,
                        "document_type": "pdf",
                        "page": str(idx),
                    },
                )
            )

    return pages


def read_text_file(path: Path) -> list[tuple[str, dict[str, str]]]:
    """Read TXT or Markdown files as plain text sources."""
    if not path.exists():
        raise FileNotFoundError(f"Text file not found: {path}")

    text = path.read_text(encoding="utf-8").strip()

    if not text:
        return []

    document_type = path.suffix.lower().replace(".", "")

    return [
        (
            text,
            {
                "source_file": path.name,
                "document_type": document_type,
            },
        )
    ]


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


def load_sources(
    docs_dir: SourceInput,
    data_dir: SourceInput,
) -> list[tuple[str, dict[str, str]]]:
    """
    Load all supported source files.

    Supports:
    - PDF files
    - TXT files
    - Markdown files
    - CSV files

    The function accepts either one directory or a list of directories,
    so it remains compatible with the original build_index.py and also
    supports uploaded document folders.
    """
    items: list[tuple[str, dict[str, str]]] = []

    docs_dirs = _as_paths(docs_dir)
    data_dirs = _as_paths(data_dir)

    for current_docs_dir in docs_dirs:
        if not current_docs_dir.exists():
            continue

        for pdf_path in sorted(current_docs_dir.glob("*.pdf")):
            items.extend(read_pdf(pdf_path))

        for txt_path in sorted(current_docs_dir.glob("*.txt")):
            items.extend(read_text_file(txt_path))

        for md_path in sorted(current_docs_dir.glob("*.md")):
            items.extend(read_text_file(md_path))

    for current_data_dir in data_dirs:
        if not current_data_dir.exists():
            continue

        for csv_path in sorted(current_data_dir.glob("*.csv")):
            items.extend(read_csv_as_rows(csv_path))

    if not items:
        raise RuntimeError(
            "No PDF, TXT, MD or CSV sources were found. "
            "Add files to docs/, data/ or upload folders."
        )

    return items