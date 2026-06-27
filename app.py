from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
load_dotenv(PROJECT_ROOT / ".env")

from ace_assistant.rag_pipeline import RagPipeline


st.set_page_config(page_title="ACE Study Assistant", page_icon="☁️", layout="wide")

st.title("☁️ ACE Study Assistant")
st.caption("Agente RAG para estudiar Google Cloud Associate Cloud Engineer usando documentos propios.")

with st.sidebar:
    st.header("Ejemplos de preguntas")
    st.markdown("""
- ¿Qué dominios cubre la certificación ACE?
- ¿Qué diferencia hay entre Cloud Run y Compute Engine?
- ¿Cuándo conviene usar Cloud NAT?
- Dame una pregunta tipo examen sobre IAM.
- ¿Qué comando uso para listar instancias de Compute Engine?
    """)
    st.divider()
    st.markdown("Primero ejecuta: `python scripts/build_index.py`")

if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource(show_spinner="Cargando pipeline RAG...")
def get_pipeline() -> RagPipeline:
    return RagPipeline()

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
            pipeline = get_pipeline()
            with st.spinner("Buscando en la documentación y generando respuesta..."):
                rag_answer = pipeline.answer(question)
            st.markdown(rag_answer.answer)

            with st.expander("Fuentes recuperadas"):
                for idx, chunk in enumerate(rag_answer.sources, start=1):
                    source = chunk.metadata.get("source_file", "fuente_desconocida")
                    page = chunk.metadata.get("page")
                    row = chunk.metadata.get("row")
                    location = f"página {page}" if page else f"fila {row}" if row else "sin ubicación"
                    st.markdown(f"**{idx}. {source}** - {location}")
                    st.caption(chunk.text[:600] + ("..." if len(chunk.text) > 600 else ""))

            st.session_state.messages.append({"role": "assistant", "content": rag_answer.answer})
        except Exception as exc:
            error_message = f"No pude responder todavía: {exc}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
