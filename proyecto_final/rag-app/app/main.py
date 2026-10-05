from pathlib import Path
import time
from google.genai.errors import ClientError
from io import BytesIO
from app.generate import Generator

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader

from app.chunk import chunk_text
from app.embed import Embedder
from app.store import Store

app = FastAPI(title="RAG App", description="Ingesta y consulta de documentos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CHUNK_SIZE = 300
BATCH_SIZE= 20
CHUNK_OVERLAP = 50
MIN_SCORE = 0.0
PAUSA = 4
MIN_SCORE = 0.60
_generator = None

_embedder = None
_store = None


def get_embedder() -> Embedder:
    global _embedder
    if _embedder is None:
        try:
            _embedder = Embedder()
        except ValueError as e:
            raise HTTPException(status_code=503, detail=str(e))
    return _embedder


def get_store() -> Store:
    global _store
    if _store is None:
        _store = Store()
    return _store


def extract_text(name: str, data: bytes) -> str:
    if name.lower().endswith(".pdf"):
        reader = PdfReader(BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return data.decode("utf-8", errors="ignore")


def embed_con_reintento(textos: list[str], intentos: int = 5):
    espera = 20
    for intento in range(intentos):
        try:
            return get_embedder().get_embeddings_batch(textos)
        except ClientError as e:
            if e.code == 429 and intento < intentos - 1:
                time.sleep(espera)
                espera *= 2
            else:
                raise

def get_generator() -> Generator:
    global _generator
    if _generator is None:
        try:
            _generator = Generator()
        except ValueError as e:
            raise HTTPException(status_code=503, detail=str(e))
    return _generator

def index_document(name: str, text: str) -> int:
    chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
    if not chunks:
        return 0
    embeddings = []
    for i in range(0, len(chunks), BATCH_SIZE):
        embeddings += embed_con_reintento(chunks[i : i + BATCH_SIZE])
        time.sleep(PAUSA)
    get_store().add_chunks(name, chunks, embeddings)
    print(f"{name}: lote {i}")
    return len(chunks)

@app.get("/health")
def health():
    try:
        n = get_store().count()
        return {"api": "ok", "chroma": "ok", "chunks_indexados": n}
    except Exception as e:
        return {"api": "ok", "chroma": f"error: {e}"}


@app.post("/ingest")
async def ingest(
    files: list[UploadFile] = File(default=[]),
    folder: str | None = Form(default=None),
):
    docs = []
    for f in files:
        docs.append((f.filename, extract_text(f.filename, await f.read())))
    if folder:
        ruta = Path(folder)
        if not ruta.is_dir():
            raise HTTPException(status_code=400, detail=f"Carpeta no encontrada: {folder}")
        for p in sorted(ruta.iterdir()):
            if p.suffix.lower() in {".txt", ".md", ".pdf"}:
                docs.append((p.name, extract_text(p.name, p.read_bytes())))

    if not docs:
        raise HTTPException(status_code=400, detail="No se recibieron documentos.")

    total_chunks = sum(index_document(name, text) for name, text in docs)
    return {"documentos": len(docs), "chunks": total_chunks}


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


@app.post("/query")
def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta está en blanco.")

    store = get_store()
    if store.count() == 0:
        return {
            "answer": "El índice está vacío. Ingesta documentos primero.",
            "citations": [],
            "abstained": True,
        }

    emb = get_embedder().get_embedding(req.question, is_query=True)
    resultados = store.query(emb, top_k=req.top_k)

    citations = [
        {"n": i + 1, "id": r["id"], "source": r["source"], "text": r["text"], "score": r["score"]}
        for i, r in enumerate(resultados)
    ]

    if not citations or citations[0]["score"] < MIN_SCORE:
        return {
            "answer": "No tengo evidencia suficiente en los documentos para responder.",
            "citations": citations,
            "abstained": True,
        }

    try:
        answer, abstained = get_generator().answer(req.question, citations)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error al generar la respuesta: {e}")
    return {"answer": answer, "citations": citations, "abstained": abstained}