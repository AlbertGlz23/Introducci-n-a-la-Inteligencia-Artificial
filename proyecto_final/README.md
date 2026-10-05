# Proyecto final: sistema RAG sobre empresas de videojuegos

Este repositorio contiene la entrega completa del proyecto final: un sistema RAG
(Retrieval-Augmented Generation) que responde preguntas sobre la historia de Xbox, PlayStation,
Nintendo, Sega y Atari, con citas `[n]` y abstención cuando no hay evidencia.

Stack: **Streamlit** (UI) + **FastAPI** (API) + **ChromaDB** (índice vectorial) + **Google AI** (embeddings y generación con Gemini).

## Organización

```
proyecto_final/
├── README.md                 ← este archivo
├── rag-app/                  ← el sistema (código, corpus e índice)
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   ├── down_corpus.py
│   ├── app/
│   │   ├── main.py
│   │   ├── chunk.py
│   │   ├── embed.py
│   │   ├── store.py
│   │   └── generate.py
│   ├── ui/
│   │   └── streamlit_app.py
│   ├── data/
│   │   ├── xbox.md
│   │   ├── playstation.md
│   │   ├── nintendo.md
│   │   ├── sega.md
│   │   └── atari.md
│   └── chroma/               ← índice local (no se entrega)
├── evidencias/
│   ├── evidencias.md
│   └── assets/               ← capturas de pantalla
└── reporte/
    └── reporte.md
```

## Qué hay en cada carpeta

### `rag-app/`: el sistema

Todo lo necesario para ejecutar el proyecto. Sus instrucciones de instalación y uso están en
[`rag-app/README.md`](rag-app/README.md).

| Ruta | Contenido |
|---|---|
| `app/main.py` | API con FastAPI: `GET /health`, `POST /ingest` y `POST /query` |
| `app/chunk.py` | Partición del texto en chunks con solape |
| `app/embed.py` | Cliente de embeddings de Google AI (`gemini-embedding-001`) |
| `app/store.py` | Acceso a ChromaDB: guardar chunks y buscar los más similares |
| `app/generate.py` | Generación de la respuesta con Gemini: anclada a la evidencia, con citas y abstención |
| `ui/streamlit_app.py` | Interfaz web: indexar documentos, preguntar y ver citas con scores |
| `data/` | Corpus: 5 artículos de Wikipedia en español (licencia CC BY-SA) |
| `down_corpus.py` | Script que descarga el corpus desde la API de Wikipedia |
| `chroma/` | Índice vectorial persistente, generado al ingestar. Se recrea y no se entrega |
| `requirements.txt` | Dependencias con las versiones que funcionaron |
| `.env.example` | Plantilla de configuración: `GOOGLE_API_KEY=` vacío |

### `evidencias/`

Capturas que demuestran el funcionamiento del sistema, organizadas en
[`evidencias.md`](evidencias/evidencias.md): arranque, endpoints en `/docs`, respuesta con citas y scores,
la misma pregunta en la API, abstención y persistencia del índice. Las imágenes están en `evidencias/assets/`.

### `reporte/`

[`reporte.md`](reporte/reporte.md): reporte de una página con el dominio y tamaño del corpus,
el chunking, la regla de abstención y el reparto de tareas entre Google AI y Chroma.

## Cómo ejecutar el sistema

Las instrucciones completas (crear el entorno virtual, obtener la clave de Google AI Studio,
levantar la API y la interfaz) están en [`rag-app/README.md`](rag-app/README.md).

## Archivos que no se incluyen en la entrega

Se generan o contienen datos privados, así que no se suben al repositorio ni al comprimir:

| Ruta | Motivo |
|---|---|
| `rag-app/.env` | Contiene la clave real de Google AI |
| `rag-app/.venv/` | Entorno virtual: se recrea con `pip install -r requirements.txt` |
| `rag-app/chroma/` | Índice local: se recrea indexando `data/` desde la interfaz |
| `__pycache__/` | Archivos temporales de Python |
