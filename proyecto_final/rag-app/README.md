# RAG: historia de las empresas de videojuegos

Sistema RAG que responde preguntas sobre Xbox, PlayStation, Nintendo, Sega y Atari,
con citas [n] y abstención cuando no hay evidencia.

## Arquitectura
Streamlit (8501) → FastAPI (8000) → ChromaDB (índice) + Google AI (embeddings y generación).
Streamlit solo habla con la API; no toca Chroma ni Google directamente.

## Requisitos
- Python 3.11
- Una clave de Google AI Studio: https://aistudio.google.com/apikey ("Get API key")

## Instalación
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```
Edita `.env` y escribe tu clave: `GOOGLE_API_KEY=tu_clave` (sin comillas ni espacios).

## Uso
Siempre desde la carpeta `rag-app/`, en dos terminales:

Primera terminal:
```powershell
uvicorn app.main:app --reload --port 8000
```

Segunda teminal
```powershell
streamlit run ui/streamlit_app.py
```
1. Abre http://localhost:8501 → pestaña "Indexar documentos" → escrib el nombre de la carpeta `data` → Indexar.
   (La ingesta tarda varios minutos por los límites de cuota gratuita.)
2. Pestaña "Preguntar": por ejemplo, "¿Cuándo se lanzó la Sega Saturn?".
3. La documentación de la API está en http://localhost:8000/docs.

## Configuración
| Parámetro | Valor | Dónde |
|---|---|---|
| Modelo de embeddings | gemini-embedding-001 (768 dims) | app/embed.py |
| Modelo de generación | gemini-3.8-flash, (Modelo de respaldo: gemini-3.8-flash-lite) | app/generate.py |
| Tamaño de chunk / solape | 300 / 50 palabras | app/main.py |
| top_k por defecto | 5 | app/main.py |
| MIN_SCORE | 0.60 | app/main.py |
Los modelos funcionaban a fecha de 3 de Ocubre de 2026; los nombres cambian con el tiempo.

## Regla de abstención
1. Umbral: si el score del mejor fragmento es menor que 0.60, la API se abstiene sin llamar a Gemini.
2. Gemini: si los fragmentos no contienen el dato pedido, responde NO_HAY_EVIDENCIA y la API se abstiene.
Motivo: el score solo mide qué tan parecido es el tema, no si el fragmento contiene el dato
pedido; por ejemplo, una pregunta sobre Nintendo en 2031 obtuvo 0.711, casi igual que las
preguntas válidas (0.72 a 0.75), así que ningún umbral la separa sin rechazar preguntas legítimas.

## Corpus
Artículos de Wikipedia en español (licencia CC BY-SA), descargados con `down_corpus.py`:
- https://es.wikipedia.org/wiki/Xbox
- https://es.wikipedia.org/wiki/PlayStation
- https://es.wikipedia.org/wiki/Nintendo
- https://es.wikipedia.org/wiki/Sega
- https://es.wikipedia.org/wiki/Atari

## Limitaciones conocidas
- Preguntas vagas pueden traer fragmentos del tema correcto sin el dato; el sistema se abstiene
  en lugar de inventar. Ejemplo: la pregunta sobre qué consola lanzó Sega tras la Genesis se abstuvo, y al reformularla como cuándo se lanzó la Saturn respondió bien.
- El plan gratuito de Google limita la cuota y a veces devuelve 429/503; hay reintentos automáticos.