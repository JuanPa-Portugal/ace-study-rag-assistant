from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
load_dotenv(PROJECT_ROOT / ".env")

from ace_assistant.document_manager import (
    delete_uploaded_document,
    list_documents,
    save_uploaded_files,
)
from ace_assistant.rag_pipeline import RagPipeline


st.set_page_config(
    page_title="ACE Study Assistant",
    page_icon="☁️",
    layout="wide",
)

CUSTOM_CSS = """
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #111827 45%, #1e293b 100%);
    }

    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid #1e293b;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #e5e7eb;
    }

    .hero-card {
        padding: 2rem;
        border-radius: 1.25rem;
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.22), rgba(14, 165, 233, 0.12));
        border: 1px solid rgba(148, 163, 184, 0.25);
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        max-width: 900px;
    }

    .source-badge {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        background: rgba(34, 197, 94, 0.15);
        color: #86efac;
        border: 1px solid rgba(34, 197, 94, 0.35);
        font-size: 0.85rem;
        margin-bottom: 0.75rem;
    }

    div[data-testid="stChatMessage"] {
        border-radius: 1rem;
        border: 1px solid rgba(148, 163, 184, 0.16);
        background: rgba(15, 23, 42, 0.65);
    }

    .stButton > button {
        border-radius: 0.75rem;
        font-weight: 600;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource(show_spinner="Cargando pipeline RAG...")
def get_pipeline() -> RagPipeline:
    return RagPipeline()


def rebuild_index() -> tuple[bool, str]:
    """Run the index build script and refresh the cached RAG pipeline."""
    result = subprocess.run(
        [sys.executable, "scripts/build_index.py"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return False, result.stderr or result.stdout

    get_pipeline.clear()
    return True, result.stdout

def is_simple_greeting(question: str) -> bool:
    """Detect simple greetings that do not need RAG retrieval."""
    normalized = question.lower().strip()

    greetings = {
        "hola",
        "hola!",
        "hola,",
        "buenas",
        "buen dia",
        "buen día",
        "buenas tardes",
        "buenas noches",
        "como estas",
        "cómo estás",
        "hola como estas",
        "hola cómo estás",
        "hey",
        "hi",
        "hello",
    }

    return normalized in greetings


def answer_simple_greeting() -> str:
    """Return a friendly greeting without querying the vector database."""
    return (
        "¡Hola! Estoy listo para ayudarte a estudiar para la certificación "
        "Google Cloud Associate Cloud Engineer. Puedes preguntarme sobre IAM, "
        "Compute Engine, Cloud Run, redes, billing, comandos `gcloud` o pedirme "
        "preguntas tipo examen."
    )


if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.header("Configuración")

    if st.button("Reconstruir índice vectorial", use_container_width=True):
        with st.spinner("Reconstruyendo índice..."):
            ok, output = rebuild_index()

        if ok:
            st.success("Índice reconstruido correctamente.")
            st.caption(output)
        else:
            st.error("No se pudo reconstruir el índice.")
            st.code(output)

    if st.button("Limpiar chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.header("Gestión de documentos")

    uploaded_files = st.file_uploader(
        "Agregar archivos para alimentar a la IA",
        type=["pdf", "csv", "txt", "md"],
        accept_multiple_files=True,
    )

    if st.button("Guardar archivos y reconstruir índice", use_container_width=True):
        if not uploaded_files:
            st.warning("Primero selecciona uno o más archivos.")
        else:
            try:
                saved_paths = save_uploaded_files(uploaded_files)

                with st.spinner("Reconstruyendo índice con los nuevos documentos..."):
                    ok, output = rebuild_index()

                if ok:
                    st.success(f"Se guardaron {len(saved_paths)} archivo(s).")
                    st.caption("El índice fue actualizado correctamente.")
                else:
                    st.error("Los archivos se guardaron, pero falló la reconstrucción del índice.")
                    st.code(output)

            except Exception as exc:
                st.error(f"No se pudieron guardar los archivos: {exc}")

    st.divider()

    st.subheader("Documentos disponibles")

    documents = list_documents()

    if not documents:
        st.caption("Todavía no hay documentos disponibles.")
    else:
        for doc in documents:
            label = f"{doc.name} ({doc.origin}, {doc.size_kb} KB)"

            if doc.deletable:
                col_file, col_delete = st.columns([0.82, 0.18])
                with col_file:
                    st.caption(label)
                with col_delete:
                    if st.button("🗑️", key=f"delete-{doc.path}"):
                        try:
                            delete_uploaded_document(str(doc.path))
                            ok, output = rebuild_index()

                            if ok:
                                st.success("Documento eliminado e índice actualizado.")
                                st.rerun()
                            else:
                                st.error("Documento eliminado, pero falló la reconstrucción del índice.")
                                st.code(output)

                        except Exception as exc:
                            st.error(f"No se pudo eliminar el documento: {exc}")
            else:
                st.caption(label)

    st.divider()

    st.header("Ejemplos de preguntas")
    st.markdown(
        """
- ¿Qué dominios cubre la certificación ACE?
- ¿Qué diferencia hay entre Cloud Run y Compute Engine?
- ¿Cuándo conviene usar Cloud NAT?
- Dame una pregunta tipo examen sobre IAM.
- ¿Qué comando uso para listar instancias de Compute Engine?
        """
    )


st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">☁️ ACE Study Assistant</div>
        <div class="hero-subtitle">
            Agente RAG para estudiar Google Cloud Associate Cloud Engineer usando documentos propios.
            Puedes consultar la base actual, agregar nuevos PDF/CSV/TXT/MD y reconstruir el índice vectorial desde la interfaz.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Escribe tu pregunta sobre Google Cloud ACE")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            if is_simple_greeting(question):
                greeting_answer = answer_simple_greeting()
                st.markdown(greeting_answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": greeting_answer}
                )

            else:
                pipeline = get_pipeline()

                with st.spinner("Buscando en la documentación y generando respuesta..."):
                    rag_answer = pipeline.answer(question)

                st.markdown(
                    '<span class="source-badge">Fuente usada: RAG</span>',
                    unsafe_allow_html=True,
                )
                st.markdown(rag_answer.answer)

                with st.expander("Fuentes recuperadas"):
                    for idx, chunk in enumerate(rag_answer.sources, start=1):
                        source = chunk.metadata.get("source_file", "fuente_desconocida")
                        page = chunk.metadata.get("page")
                        row = chunk.metadata.get("row")

                        if page:
                            location = f"página {page}"
                        elif row:
                            location = f"fila {row}"
                        else:
                            location = "sin ubicación"

                        st.markdown(f"**{idx}. {source}** - {location}")
                        st.caption(
                            chunk.text[:600] + ("..." if len(chunk.text) > 600 else "")
                        )

                st.session_state.messages.append(
                    {"role": "assistant", "content": rag_answer.answer}
                )
        except Exception as exc:
            error_message = f"No pude responder todavía: {exc}"
            st.error(error_message)
            st.session_state.messages.append(
                {"role": "assistant", "content": error_message}
            )