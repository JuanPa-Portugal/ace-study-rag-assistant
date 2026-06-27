# ACE Study Assistant

Agente RAG para estudiar la certificación **Google Cloud Associate Cloud Engineer (ACE)** usando documentación propia en PDF y CSV.

El proyecto fue diseñado para un Challenge de agente inteligente. La solución procesa documentos, genera embeddings, consulta una base vectorial y produce respuestas con fuentes mediante una interfaz simple en Streamlit.

---

## Problema que resuelve

Cuando una persona estudia para la certificación **Google Cloud Associate Cloud Engineer**, la información suele quedar repartida entre guías oficiales, apuntes, comandos, documentación de servicios y preguntas de práctica.

**ACE Study Assistant** centraliza esa documentación y permite hacer preguntas en lenguaje natural, obteniendo respuestas basadas en los documentos cargados en la base de conocimiento.

Ejemplos:

* ¿Qué dominios cubre la certificación ACE?
* ¿Qué diferencia hay entre Cloud Run y Compute Engine?
* ¿Cuándo conviene usar Cloud NAT?
* ¿Qué comando uso para listar instancias de Compute Engine?
* Dame una pregunta tipo examen sobre IAM.

---

## Objetivo del proyecto

Construir un agente inteligente funcional que permita:

* Leer documentación propia en formato PDF y CSV.
* Procesar los documentos y dividirlos en fragmentos de texto.
* Generar embeddings usando Gemini API.
* Almacenar los vectores en ChromaDB.
* Recuperar fragmentos relevantes según la pregunta del usuario.
* Generar respuestas con Gemini API.
* Mostrar las fuentes utilizadas en cada respuesta.
* Ejecutar la solución desde una interfaz web simple en Streamlit.
* Preparar el proyecto para deploy en Oracle Cloud Infrastructure (OCI).

---

## Arquitectura

```text
PDF/CSV
  ↓
Extracción de texto
  ↓
Limpieza y chunking
  ↓
Embeddings con Gemini API
  ↓
ChromaDB persistente
  ↓
Consulta semántica
  ↓
Prompt con contexto recuperado
  ↓
Gemini API
  ↓
Respuesta con fuentes en Streamlit
```

---

## Tecnologías utilizadas

* Python
* Streamlit
* ChromaDB
* Gemini Embeddings API
* Google GenAI SDK (`google-genai`)
* pypdf
* pandas
* python-dotenv
* Docker
* GitHub
* OCI Compute para deploy

---

## Estructura del proyecto

```text
ace-study-rag-assistant/
 ├── .streamlit/                   # Configuración visual de Streamlit
 ├── assets/                       # Recursos visuales del proyecto
 ├── chroma_db/                    # Base vectorial local generada
 ├── data/                         # CSVs de comandos y preguntas
 ├── docs/                         # PDFs de estudio
 ├── docs_src/                     # Fuentes markdown de los PDFs
 ├── scripts/
 │   └── build_index.py            # Construcción del índice vectorial
 ├── src/
 │   └── ace_assistant/
 │       ├── chunking.py           # División de documentos en chunks
 │       ├── config.py             # Configuración central del proyecto
 │       ├── embeddings.py         # Embeddings con Gemini API
 │       ├── llm_client.py         # Cliente Gemini para generación de respuestas
 │       ├── loaders.py            # Carga de PDFs y CSVs
 │       ├── models.py             # Modelos internos de datos
 │       ├── rag_pipeline.py       # Pipeline RAG principal
 │       └── vector_store.py       # Integración con ChromaDB
 ├── app.py                        # Aplicación Streamlit
 ├── Dockerfile                    # Imagen Docker para deploy
 ├── requirements.txt              # Dependencias del proyecto
 ├── .env.example                  # Plantilla de variables de entorno
 ├── .gitignore
 └── README.md
```

---

## Documentos utilizados como base de conocimiento

El agente utiliza documentación propia creada para el proyecto:

```text
docs/
 ├── 01_guia_general_ace.pdf
 ├── 02_entorno_billing_iam.pdf
 ├── 03_compute_serverless_gke.pdf
 └── 04_storage_networking_operations.pdf
```

También utiliza datasets CSV de apoyo:

```text
data/
 ├── 05_comandos_gcloud.csv
 └── 06_preguntas_tipo_examen.csv
```

Estos archivos contienen explicaciones, comandos y preguntas de práctica relacionadas con los dominios de la certificación **Google Cloud Associate Cloud Engineer**.

---

## Requisitos previos

Antes de ejecutar el proyecto se necesita:

* Python 3.10 o superior.
* Git instalado.
* Una API Key de Gemini creada desde Google AI Studio.
* Entorno virtual de Python.
* Acceso a internet para llamar a Gemini API.

---

## Configuración de Gemini API Key

El proyecto usa Gemini API para:

1. Generar embeddings de los documentos y preguntas.
2. Generar respuestas usando el contexto recuperado.

Para configurar la clave:

1. Crear una API Key desde Google AI Studio.
2. Copiar el archivo `.env.example` como `.env`.
3. Pegar la clave en la variable `GEMINI_API_KEY`.

Ejemplo de archivo `.env`:

```text
GEMINI_API_KEY=tu_api_key
GEMINI_MODEL=gemini-2.5-flash
EMBEDDING_MODEL_NAME=gemini-embedding-2
EMBEDDING_OUTPUT_DIMENSIONALITY=768
TOP_K=5
```

> Importante: el archivo `.env` no debe subirse a GitHub. Está excluido mediante `.gitignore`.

---

## Ejecución local en Windows con PowerShell

### 1. Crear entorno virtual

```powershell
python -m venv .venv
```

### 2. Activar entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación del entorno, ejecutar una sola vez:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego volver a activar:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Actualizar pip

```powershell
python -m pip install --upgrade pip
```

### 4. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 5. Crear archivo `.env`

```powershell
Copy-Item .env.example .env
```

Luego editar `.env` y completar:

```text
GEMINI_API_KEY=tu_api_key
```

### 6. Construir el índice vectorial

```powershell
python scripts/build_index.py
```

Resultado validado localmente:

```text
Index built successfully: 48 chunks stored in chroma_db
```

### 7. Ejecutar la aplicación

```powershell
streamlit run app.py
```

URL local:

```text
http://localhost:8501
```

---

## Ejecución local en Linux/Mac

### 1. Crear entorno virtual

```bash
python -m venv .venv
```

### 2. Activar entorno virtual

```bash
source .venv/bin/activate
```

### 3. Actualizar pip

```bash
python -m pip install --upgrade pip
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Crear archivo `.env`

```bash
cp .env.example .env
```

Luego editar `.env` y completar:

```text
GEMINI_API_KEY=tu_api_key
```

### 6. Construir el índice vectorial

```bash
python scripts/build_index.py
```

### 7. Ejecutar la aplicación

```bash
streamlit run app.py
```

---

## Ejecución validada localmente

La aplicación fue ejecutada localmente con el siguiente flujo:

1. Creación de entorno virtual Python.
2. Instalación de dependencias desde `requirements.txt`.
3. Configuración de `GEMINI_API_KEY` en archivo `.env`.
4. Construcción del índice vectorial con `python scripts/build_index.py`.
5. Ejecución de la interfaz con `streamlit run app.py`.

Resultado validado:

* Índice construido correctamente.
* 48 chunks almacenados en `chroma_db`.
* Aplicación disponible localmente en `http://localhost:8501`.
* Respuestas generadas con fuentes visibles desde los documentos PDF.
* Recuperación semántica funcionando con Gemini Embeddings API.
* Generación de respuestas funcionando con Gemini API.

---

## Ejemplos de preguntas

El agente puede responder preguntas como:

```text
¿Qué dominios cubre la certificación ACE?
```

```text
¿Qué diferencia hay entre Cloud Run y Compute Engine?
```

```text
¿Cuándo conviene usar Cloud NAT?
```

```text
Dame una pregunta tipo examen sobre IAM.
```

```text
¿Qué comando uso para listar instancias de Compute Engine?
```

```text
¿Qué evalúa la certificación Associate Cloud Engineer?
```

---

## Ejemplo de respuesta esperada

```text
La certificación Google Cloud Associate Cloud Engineer evalúa la capacidad de una persona para configurar entornos cloud, implementar soluciones, operar recursos existentes y administrar acceso y seguridad en Google Cloud.

Los dominios principales son:

- Setting up a cloud solution environment.
- Planning and implementing a cloud solution.
- Ensuring successful operation.
- Configuring access and security.

Fuentes utilizadas:
- 01_guia_general_ace.pdf - página 1
- 01_guia_general_ace.pdf - página 2
```

---

## Funcionamiento del RAG

El flujo RAG implementado funciona de la siguiente manera:

1. Los documentos PDF y CSV son cargados desde las carpetas `docs/` y `data/`.
2. El texto se extrae y se transforma en fragmentos o chunks.
3. Cada chunk recibe metadatos como nombre de documento, tipo de archivo y página.
4. Se generan embeddings con Gemini API.
5. Los embeddings se almacenan en ChromaDB.
6. Cuando el usuario hace una pregunta, se genera un embedding de la consulta.
7. ChromaDB recupera los chunks más relevantes.
8. Gemini recibe la pregunta junto con el contexto recuperado.
9. La respuesta final se muestra en Streamlit junto con las fuentes utilizadas.

---

## Deploy en OCI - camino recomendado

El deploy final está preparado para realizarse en Oracle Cloud Infrastructure usando OCI Compute.

Pasos recomendados:

1. Crear una VM en OCI Compute.
2. Configurar reglas de red para permitir acceso al puerto `8501`.
3. Instalar Git, Python y Docker.
4. Clonar este repositorio.
5. Crear el archivo `.env` con la API Key de Gemini.
6. Instalar dependencias o construir la imagen Docker.
7. Ejecutar `python scripts/build_index.py`.
8. Levantar la aplicación con Streamlit.
9. Tomar una captura de pantalla o registrar la URL pública como evidencia del deploy.

---

## Ejecución con Docker

Construir la imagen:

```bash
docker build -t ace-study-rag-assistant .
```

Ejecutar el contenedor:

```bash
docker run --env-file .env -p 8501:8501 ace-study-rag-assistant
```

La aplicación quedará disponible en:

```text
http://localhost:8501
```

---

## Evidencia de deploy

Estado actual:

```text
Pendiente de deploy final en OCI.
```

Una vez desplegado, esta sección deberá actualizarse con:

* URL pública de la aplicación.
* Captura de pantalla de la aplicación funcionando.
* Breve descripción de la infraestructura utilizada.
* Comando o método usado para levantar la aplicación.
* Fecha de validación del deploy.

---

## Fuentes oficiales utilizadas para construir la documentación

* https://cloud.google.com/learn/certification/cloud-engineer
* https://services.google.com/fh/files/misc/associate_cloud_engineer_exam_guide_english.pdf
* https://cloud.google.com/sdk
* https://docs.cloud.google.com/sdk/docs/authenticate
* https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects
* https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/list
* https://docs.cloud.google.com/sdk/gcloud/reference/run/services/list
* https://docs.cloud.google.com/docs

---

## Limitaciones de la versión inicial

* La base documental es pequeña y fue creada para el Challenge.
* No incluye autenticación de usuarios.
* No incluye reranking.
* No incluye filtros por dominio del examen.
* El índice vectorial se reconstruye manualmente con `scripts/build_index.py`.
* El deploy final en OCI debe completarse y documentarse con evidencia.
* La aplicación depende de una API Key válida de Gemini.

---

## Mejoras futuras

* Agregar más documentos de estudio para la certificación ACE.
* Incorporar más preguntas tipo examen.
* Agregar filtros por dominio del examen.
* Agregar historial persistente de consultas.
* Agregar evaluación automática de respuestas.
* Agregar reranking para mejorar la relevancia de los documentos recuperados.
* Automatizar la actualización del índice cuando cambien los documentos.
* Agregar autenticación de usuarios.
* Registrar métricas de uso, latencia y preguntas sin respuesta.

---

## Estado del proyecto

```text
Versión inicial funcional validada localmente.
```

Funcionalidades ya implementadas:

* Carga de documentos PDF y CSV.
* Procesamiento y chunking.
* Embeddings con Gemini API.
* Persistencia en ChromaDB.
* Recuperación semántica.
* Generación de respuestas con Gemini API.
* Visualización de fuentes utilizadas.
* Interfaz web con Streamlit.
* Repositorio público en GitHub.
* Preparación inicial para deploy en OCI.

---

## Autor

Proyecto desarrollado por **Juan Pablo Portugal** como parte de un Challenge de agente inteligente y como herramienta de apoyo para la preparación de la certificación **Google Cloud Associate Cloud Engineer**.
