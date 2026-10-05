# RAG: historia de las empresas de videojuegos

Sistema RAG que responde preguntas sobre la historia de **Xbox, PlayStation, Nintendo, Sega y Atari**. Cada respuesta se escribe en español, cita sus fuentes con `[n]` y muestra los fragmentos usados con su score. Si los documentos no contienen la respuesta, el sistema **se abstiene** en lugar de inventar.

**Tecnologías:** Streamlit (interfaz) · FastAPI (API) · ChromaDB (índice vectorial persistente) · Google AI (embeddings y generación con Gemini).

## Contenido

1. [Cómo funciona](#cómo-funciona)
2. [Arquitectura](#arquitectura)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Requisitos](#requisitos)
5. [Instalación](#instalación)
6. [Uso](#uso)
7. [Usar la API directamente](#usar-la-api-directamente)
8. [Configuración](#configuración)
9. [Regla de abstención](#regla-de-abstención)
10. [Usar tu propio corpus](#usar-tu-propio-corpus)
11. [Solución de problemas](#solución-de-problemas)
12. [Corpus y licencia](#corpus-y-licencia)
13. [Limitaciones conocidas](#limitaciones-conocidas)

---

## Cómo funciona

**Ingesta (se hace una vez):**
1. Los documentos de `data/` se parten en chunks de 300 palabras con solape de 50.
2. Google AI convierte cada chunk en un vector (embedding).
3. ChromaDB guarda los vectores, los textos y su origen en la carpeta `chroma/`.

**Consulta (cada pregunta):**
1. La pregunta se convierte en un vector con el mismo modelo de embeddings.
2. ChromaDB devuelve los `top_k` fragmentos más parecidos, cada uno con su score.
3. Si el mejor score es menor que el umbral (0.60), el sistema se abstiene sin llamar a Gemini.
4. Si no, Gemini recibe los fragmentos numerados y redacta la respuesta con citas `[n]`, o se abstiene si ningún fragmento contiene el dato.

## Arquitectura

```
Usuario
  └── Streamlit (puerto 8501)
        └── HTTP JSON
              └── FastAPI (puerto 8000)
                    ├── Google AI → embeddings
                    ├── ChromaDB  → persistencia y búsqueda de vecinos
                    └── Google AI → generación de la respuesta (Gemini)
```

Streamlit solo habla con la API por HTTP; nunca accede a Chroma ni a Google AI directamente. La clave de Google AI solo la usa FastAPI.

## Estructura del proyecto

```
rag-app/
├── README.md
├── requirements.txt
├── .env.example          ← plantilla de configuración (se sube)
├── .env                  ← tu clave real (NO se sube)
├── .gitignore
├── down_corpus.py        ← descarga el corpus desde Wikipedia
├── app/
│   ├── main.py           ← API: /health, /ingest, /query
│   ├── chunk.py          ← partición en chunks con solape
│   ├── embed.py          ← embeddings con Google AI
│   ├── store.py          ← ChromaDB: guardar y buscar
│   └── generate.py       ← Gemini: respuesta anclada y abstención
├── ui/
│   └── streamlit_app.py  ← interfaz web
├── data/                 ← corpus (5 archivos .md)
└── chroma/               ← índice local (se genera solo, NO se sube)
```

## Requisitos

- **Python 3.11.** Otras versiones recientes probablemente funcionen, pero esta es la probada.
- **Una clave de Google AI Studio** (gratuita, ver el paso 5 de la instalación).
- **Conexión a internet**, porque los embeddings y las respuestas se generan en los servidores de Google.
- Las instrucciones están probadas en **Windows con PowerShell**. Las equivalentes para Linux y macOS aparecen indicadas.

## Instalación

Todos los comandos se ejecutan **desde la carpeta `rag-app/`**, la que contiene `app/`, `data/` y `ui/`.

### 1. Entrar a la carpeta del proyecto

```powershell
cd ruta\a\proyecto_final\rag-app
dir
```

Con `dir` debes ver `app`, `data`, `ui` y `requirements.txt`. Si no los ves, estás en la carpeta equivocada.

### 2. Crear el entorno virtual

```powershell
python -m venv .venv
```

### 3. Activarlo

```powershell
.venv\Scripts\Activate.ps1
```

Cuando está activo, el prompt empieza con `(.venv)`.

Si PowerShell dice que la ejecución de scripts está deshabilitada, ejecuta esto y vuelve a activar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

> **Linux / macOS:** `python3 -m venv .venv` y luego `source .venv/bin/activate`.

### 4. Instalar las dependencias

```powershell
pip install -r requirements.txt
```

### 5. Obtener una clave de Google AI Studio

1. Entra a https://aistudio.google.com/apikey e inicia sesión con tu cuenta de Google.
2. Pulsa **Create API key** (o **Get API key**) y elige o crea un proyecto.
3. Copia la clave que aparece. Empieza con `AIza` o `AQ.`, según el tipo.

### 6. Configurar el archivo `.env`

Crea tu `.env` a partir de la plantilla:

```powershell
copy .env.example .env
```

> **Linux / macOS:** `cp .env.example .env`

Abre `.env` con VS Code o el Bloc de notas y deja **una sola línea**, sin comillas ni espacios alrededor del `=`:

```
GOOGLE_API_KEY=tu_clave_aqui
```

Guarda el archivo en UTF-8. El `.env` debe estar en la raíz de `rag-app/`, junto a `requirements.txt`, y **nunca dentro de `.venv/`**. Está en el `.gitignore`, así que no se sube al repositorio.

### 7. Verificar la instalación

```powershell
python -c "from app.embed import Embedder; Embedder(); print('Clave detectada: OK')"
```

Si imprime `Clave detectada: OK`, todo está listo. Si falla, mira la [solución de problemas](#solución-de-problemas).

## Uso

Se necesitan **dos terminales**, ambas en `rag-app/` y con el entorno virtual activado (`(.venv)` en el prompt).

### 1. Levantar la API (terminal 1)

```powershell
uvicorn app.main:app --reload --port 8000
```

Debe aparecer `Application startup complete`. La primera línea indica el directorio vigilado y **debe terminar en `rag-app'`**; si termina en otra carpeta, estás en el lugar equivocado.

Comprueba que funciona abriendo http://localhost:8000/docs, donde se listan `/health`, `/ingest` y `/query`.

### 2. Levantar la interfaz (terminal 2)

Abre una terminal nueva, entra a `rag-app/`, activa el entorno virtual y ejecuta:

```powershell
streamlit run ui/streamlit_app.py
```

Se abre en http://localhost:8501. La barra lateral debe mostrar **"API conectada"** y el número de chunks indexados.

### 3. Indexar el corpus (solo la primera vez)

1. En la interfaz, abre la pestaña **Indexar documentos**.
2. Deja en el campo de carpeta el valor `data` y pulsa **Indexar**.
3. Espera. Tarda **varios minutos** porque el plan gratuito de Google limita cuántos textos se pueden enviar por minuto. No cierres la terminal de uvicorn mientras corre.
4. Al terminar aparece un mensaje con el número de documentos y chunks (con el corpus incluido: 5 documentos y 131 chunks).

Alternativa desde la terminal, útil si la interfaz se corta por el tiempo:

```powershell
curl.exe -X POST http://localhost:8000/ingest -F "folder=data"
```

Indexar de nuevo el mismo archivo **no duplica** los datos: los chunks se actualizan (`upsert`).

También puedes subir archivos `.txt`, `.md` o `.pdf` desde la misma pestaña.

### 4. Hacer preguntas

En la pestaña **Preguntar**, escribe una pregunta y pulsa **Preguntar**. El control `top_k` define cuántos fragmentos se recuperan (5 por defecto). La pantalla muestra:

- **Respuesta:** texto en español con citas `[n]`.
- **Fragmentos usados:** desplegables numerados `[n]` con el archivo de origen, el score y el texto.
- **Aviso amarillo:** aparece cuando el sistema se abstiene, y los fragmentos siguen visibles.

### Preguntas de prueba

| Pregunta | Resultado esperado | Score aprox. |
|---|---|---|
| ¿Cuándo se lanzó la Sega Saturn? | Responde con fechas y citas | 0.78 |
| ¿Cuándo salió la primera PlayStation? | Responde con la fecha de 1994 | 0.75 |
| ¿Qué pasó con Atari en la crisis de 1983? | Responde con citas | 0.74 |
| ¿Cuántas consolas vendió Nintendo en 2031? | Se abstiene (lo decide Gemini) | 0.71 |
| ¿Cuál es la receta del mole poblano? | Se abstiene (lo decide el umbral) | 0.50 |

Los scores pueden variar ligeramente.

### Reiniciar la aplicación

Detén uvicorn con **Ctrl+C** y vuélvelo a levantar. El índice **se conserva** en la carpeta `chroma/`, así que no hace falta volver a indexar.

## Usar la API directamente

La documentación interactiva está en http://localhost:8000/docs.

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/health` | Confirma que la API y Chroma responden, e informa cuántos chunks hay indexados |
| POST | `/ingest` | Recibe archivos (`files`) o una carpeta (`folder`), los parte en chunks, calcula los embeddings y los guarda |
| POST | `/query` | Recibe una pregunta y devuelve la respuesta, las citas y si se abstuvo |

**`GET /health`**

```json
{ "api": "ok", "chroma": "ok", "chunks_indexados": 131 }
```

**`POST /ingest`** (formulario `multipart/form-data`)

```powershell
curl.exe -X POST http://localhost:8000/ingest -F "folder=data"
```

```json
{ "documentos": 5, "chunks": 131 }
```

> En `/docs`, el botón "Try it out" de `/ingest` a veces envía el campo `files` vacío y da un error 422. Usa `curl.exe` o la interfaz de Streamlit.

**`POST /query`** (JSON)

```powershell
curl.exe -X POST http://localhost:8000/query -H "Content-Type: application/json" -d "{\"question\": \"¿Cuándo se lanzó la Sega Saturn?\", \"top_k\": 5}"
```

Respuesta (resumida):

```json
{
  "answer": "La Sega Saturn se lanzó el 22 de noviembre de 1994 en Japón [1] ...",
  "citations": [
    { "n": 1, "id": "sega.md::14", "source": "sega.md", "text": "...", "score": 0.7777 }
  ],
  "abstained": false
}
```

Una pregunta sin evidencia **no devuelve un error**: responde con `"abstained": true` y un mensaje claro.

## Configuración

| Parámetro | Valor | Dónde cambiarlo |
|---|---|---|
| Modelo de embeddings | `gemini-embedding-001` (768 dimensiones) | `app/embed.py` |
| Modelo de generación | `gemini-3.8-flash` | `MODELOS` en `app/generate.py` |
| Modelo de respaldo | `gemini-3.8-flash-lite` | `MODELOS` en `app/generate.py` |
| Tamaño de chunk / solape | 300 / 50 palabras | `CHUNK_SIZE`, `CHUNK_OVERLAP` en `app/main.py` |
| `top_k` por defecto | 5 | `QueryRequest` en `app/main.py` |
| Umbral de abstención `MIN_SCORE` | 0.60 | `app/main.py` |
| Tamaño de lote al indexar | 20 chunks, con pausa de 4 s | `BATCH_SIZE`, `PAUSA` en `app/main.py` |

Los modelos funcionaban a fecha del **4 de octubre de 2026**. Google retira y renombra modelos con frecuencia; si aparece un error 404 con el nombre de un modelo, consulta la [solución de problemas](#solución-de-problemas).

> **Importante:** si cambias el modelo de embeddings o el tamaño de chunk, borra la carpeta `chroma/` y vuelve a indexar. Los vectores de modelos distintos no son comparables.

## Regla de abstención

El sistema decide en dos capas si responde o se abstiene:

1. **Umbral.** Si el score del mejor fragmento es menor que **0.60**, la API se abstiene sin llamar a Gemini y muestra los fragmentos recuperados.
2. **Gemini.** Si el score es de 0.60 o más, Gemini recibe los fragmentos numerados con la instrucción de responder solo con esa evidencia. Si ningún fragmento contiene el dato pedido, responde `NO_HAY_EVIDENCIA` y la API se abstiene.

**Por qué dos capas.** El score solo mide qué tan parecido es el *tema*, no si el fragmento contiene el *dato* pedido. Una pregunta sobre Nintendo en 2031 obtuvo 0.711, casi igual que las preguntas válidas (0.72 a 0.78), así que ningún umbral la separa sin rechazar preguntas legítimas. Por eso Gemini actúa como segunda capa.

## Usar tu propio corpus

1. Coloca archivos `.md`, `.txt` o `.pdf` en `data/`, o súbelos desde la pestaña **Indexar documentos**.
2. Indexa de nuevo.
3. Para empezar desde cero, detén uvicorn, borra la carpeta `chroma/` y vuelve a indexar.

## Solución de problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| `GOOGLE_API_KEY no encontrada en el archivo .env` | El `.env` no está en `rag-app/`, está vacío o mal escrito | Verifica que esté junto a `requirements.txt` (no en `.venv/`), que tenga la línea `GOOGLE_API_KEY=...` sin comillas ni espacios, y que lo hayas guardado |
| `ModuleNotFoundError: No module named 'app'` | Estás ejecutando uvicorn desde otra carpeta | Haz `cd` a `rag-app/` y vuelve a ejecutarlo |
| `Could not import module "app.main"` | Falta `app/main.py` o tiene un error de sintaxis | Revisa que el archivo exista y mira el traceback |
| `429 RESOURCE_EXHAUSTED` | Se superó la cuota gratuita de Google | Espera un minuto: la API reintenta sola. Si persiste, revisa tu uso en https://ai.dev/rate-limit |
| `503 UNAVAILABLE` | El modelo de Google está saturado | Espera unos segundos y repite; hay reintentos automáticos y un modelo de respaldo |
| `404 NOT_FOUND` con el nombre de un modelo | Google retiró o renombró el modelo | Lista los modelos disponibles (comando abajo) y cambia el nombre en `embed.py` o `generate.py` |
| `422 Unprocessable Entity` en `/ingest` desde `/docs` | Swagger envía el campo `files` vacío | Usa `curl.exe` o la interfaz de Streamlit |
| La interfaz dice "No se pudo conectar con la API" | uvicorn no está corriendo o usa otro puerto | Levanta la API en el puerto 8000 |
| Todas las preguntas se abstienen con "índice vacío" | No se ha indexado el corpus | Ejecuta la indexación (paso 3 del uso) |
| Los resultados son raros tras cambiar de modelo | Los vectores viejos son de otro modelo | Borra `chroma/` y vuelve a indexar |

**Listar los modelos disponibles para tu clave:**

```powershell
python -c "import os; from dotenv import load_dotenv; from google import genai; load_dotenv(); c=genai.Client(api_key=os.getenv('GOOGLE_API_KEY')); [print(m.name) for m in c.models.list()]"
```

Para generación, busca nombres que contengan `flash`. Para embeddings, busca los que contengan `embedding`.

## Corpus y licencia

El corpus son cinco artículos de Wikipedia en español, publicados bajo licencia **CC BY-SA**:

- https://es.wikipedia.org/wiki/Xbox
- https://es.wikipedia.org/wiki/PlayStation
- https://es.wikipedia.org/wiki/Nintendo
- https://es.wikipedia.org/wiki/Sega
- https://es.wikipedia.org/wiki/Atari

Ya están incluidos en `data/`. Si quieres volver a descargarlos, ejecuta `python down_corpus.py`. Antes, edita la línea `User-Agent` del script y escribe tu correo de contacto, porque Wikimedia rechaza con un error 403 las peticiones que no se identifican.

## Limitaciones conocidas

- **Preguntas vagas.** Pueden recuperar fragmentos del tema correcto que no contienen el dato; el sistema se abstiene en lugar de inventar. Ejemplo: «¿Qué consola lanzó Sega tras la Genesis?» se abstuvo, y al reformularla como «¿Cuándo se lanzó la Sega Saturn?» respondió bien.
- **Cuota gratuita.** El plan gratuito de Google limita la cantidad de peticiones y a veces devuelve errores 429 o 503; hay reintentos automáticos, pero la indexación inicial es lenta.
- **Cortes por palabras.** Los chunks se parten por número de palabras, no por oraciones, así que pueden empezar a mitad de una frase.
- **Umbral calibrado con pocos ejemplos.** El valor de 0.60 se eligió con un conjunto pequeño de preguntas de prueba.