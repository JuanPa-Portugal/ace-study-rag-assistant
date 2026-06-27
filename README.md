# ACE Study Assistant

Agente RAG para estudiar la certificación **Google Cloud Associate Cloud Engineer (ACE)** usando documentación propia en PDF y CSV.

El proyecto fue diseñado para un Challenge de agente inteligente: procesa documentos, crea embeddings, consulta una base vectorial y genera respuestas con fuentes mediante una interfaz simple en Streamlit.

## Problema que resuelve

Cuando una persona estudia para la certificación ACE, la información suele quedar repartida entre guías, apuntes, comandos y preguntas de práctica. Este asistente centraliza esa documentación y permite hacer preguntas en lenguaje natural.

## Arquitectura

```text
PDF/CSV
  ↓
Extracción de texto
  ↓
Limpieza y chunking
  ↓
Embeddings locales con sentence-transformers
  ↓
ChromaDB persistente
  ↓
Consulta semántica
  ↓
Prompt con contexto
  ↓
Gemini API
  ↓
Respuesta con fuentes en Streamlit
```

## Tecnologías

- Python
- Streamlit
- ChromaDB
- sentence-transformers
- pypdf
- Google GenAI SDK (`google-genai`)
- Docker
- OCI Compute para deploy

## Estructura

```text
ace-study-rag-assistant/
 ├── docs/                         # PDFs de estudio
 ├── docs_src/                     # Fuentes markdown de los PDFs
 ├── data/                         # CSVs de comandos y preguntas
 ├── src/ace_assistant/            # Código modular del agente
 ├── scripts/build_index.py        # Construcción del índice vectorial
 ├── app.py                        # App Streamlit
 ├── requirements.txt
 ├── Dockerfile
 ├── .env.example
 └── README.md
```

## Cómo ejecutar localmente

### 1. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Gemini API Key

```bash
cp .env.example .env
```

Editar `.env`:

```text
GEMINI_API_KEY=tu_api_key
```

### 4. Construir el índice vectorial

```bash
python scripts/build_index.py
```

### 5. Ejecutar la aplicación

```bash
streamlit run app.py
```

## Ejemplos de preguntas

- ¿Qué dominios cubre la certificación ACE?
- ¿Qué diferencia hay entre Cloud Run y Compute Engine?
- ¿Cuándo conviene usar Cloud NAT?
- Dame una pregunta tipo examen sobre IAM.
- ¿Qué comando uso para listar instancias de Compute Engine?

## Ejemplo de respuesta esperada

```text
Cloud Run conviene cuando necesitas ejecutar una aplicación containerizada sin administrar servidores. Escala automáticamente y permite gestionar revisiones y traffic splitting.

Fuentes utilizadas:
- 03_compute_serverless_gke.pdf
```

## Deploy en OCI - camino recomendado

1. Crear una VM en OCI Compute.
2. Abrir el puerto 8501 en la lista de seguridad o Network Security Group.
3. Instalar Docker o Python.
4. Clonar el repositorio.
5. Configurar `.env`.
6. Ejecutar el índice.
7. Levantar Streamlit.

Con Docker:

```bash
docker build -t ace-study-rag-assistant .
docker run --env-file .env -p 8501:8501 ace-study-rag-assistant
```

## Fuentes oficiales utilizadas para construir la documentación

- https://cloud.google.com/learn/certification/cloud-engineer
- https://services.google.com/fh/files/misc/associate_cloud_engineer_exam_guide_english.pdf
- https://cloud.google.com/sdk
- https://docs.cloud.google.com/sdk/docs/authenticate
- https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects
- https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/list
- https://docs.cloud.google.com/sdk/gcloud/reference/run/services/list
- https://docs.cloud.google.com/docs

## Limitaciones de la versión inicial

- La base documental es pequeña y creada para el Challenge.
- No incluye autenticación de usuarios.
- No incluye reranking todavía.
- El índice vectorial se reconstruye manualmente con `scripts/build_index.py`.
- El deploy final debe completarse en OCI y documentarse con captura o URL pública.

## Mejoras futuras

- Agregar más documentos de estudio.
- Agregar evaluación automática de respuestas.
- Agregar filtros por dominio del examen.
- Agregar historial persistente de consultas.
- Automatizar actualización del índice cuando cambien los documentos.
