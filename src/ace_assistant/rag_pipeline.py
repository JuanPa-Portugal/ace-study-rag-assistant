from __future__ import annotations

from ace_assistant.config import settings
from ace_assistant.embeddings import GeminiEmbeddingModel
from ace_assistant.llm_client import GeminiClient
from ace_assistant.models import RagAnswer, RetrievedChunk
from ace_assistant.vector_store import ChromaVectorStore


def format_sources(chunks: list[RetrievedChunk]) -> str:
    lines: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        source = chunk.metadata.get("source_file", "fuente_desconocida")
        page = chunk.metadata.get("page")
        row = chunk.metadata.get("row")
        location = f"pagina {page}" if page else f"fila {row}" if row else "ubicacion no especificada"
        lines.append(f"[{index}] {source} - {location}: {chunk.text}")
    return "\n\n".join(lines)


def build_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
    context = format_sources(chunks)
    return f"""Eres ACE Study Assistant, un asistente de estudio para la certificacion Google Cloud Associate Cloud Engineer.

Reglas:
- Responde solo con base en el contexto recuperado.
- Si la informacion no esta en el contexto, dilo claramente.
- Responde en espanol claro y didactico.
- Incluye una seccion final llamada Fuentes utilizadas con los archivos consultados.
- No inventes comandos, porcentajes ni datos que no esten respaldados por el contexto.

Pregunta del usuario:
{question}

Contexto recuperado:
{context}

Respuesta:"""


class RagPipeline:
    """Coordinates embedding, retrieval and answer generation."""

    def __init__(self) -> None:
        self._embeddings = GeminiEmbeddingModel(
    model_name=settings.embedding_model_name,
    output_dimensionality=settings.embedding_output_dimensionality,
)
        self._store = ChromaVectorStore(settings.chroma_dir, settings.collection_name)
        self._llm = GeminiClient(settings.gemini_model)

    def answer(self, question: str) -> RagAnswer:
        normalized_question = question.strip()
        if not normalized_question:
            raise ValueError("Question cannot be empty")

        if self._store.count() == 0:
            raise RuntimeError("The vector index is empty. Run: python scripts/build_index.py")

        query_embedding = self._embeddings.embed_query(normalized_question)
        chunks = self._store.query(query_embedding=query_embedding, top_k=settings.top_k)
        prompt = build_prompt(normalized_question, chunks)
        answer = self._llm.generate(prompt)
        return RagAnswer(answer=answer, sources=chunks)
