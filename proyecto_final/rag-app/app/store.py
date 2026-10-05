from pathlib import Path
import chromadb

CHROMA_PATH = Path(__file__).resolve().parent.parent / "chroma"


class Store:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        self.collection = self.client.get_or_create_collection(
            name="documentos",
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, source: str, chunks: list[str], embeddings: list[list[float]]):
        ids = [f"{source}::{i}" for i in range(len(chunks))]
        metadatas = [{"source": source, "chunk_index": i} for i in range(len(chunks))]
        self.collection.upsert(
            ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas
        )

    def query(self, embedding: list[float], top_k: int = 4) -> list[dict]:
        res = self.collection.query(query_embeddings=[embedding], n_results=top_k)
        resultados = []
        for id_, doc, meta, dist in zip(
            res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]
        ):
            resultados.append({
                "id": id_,
                "text": doc,
                "source": meta["source"],
                "chunk_index": meta["chunk_index"],
                "score": 1 - dist,
            })
        return resultados

    def count(self) -> int:
        return self.collection.count()