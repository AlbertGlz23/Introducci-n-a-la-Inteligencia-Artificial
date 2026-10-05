import os
from google import genai
from pathlib import Path  
from google.genai import types
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

class Embedder:
    def __init__(self, dim: int = 768):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY no encontrada en el archivo .env")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-embedding-001"
        self.dim = dim

    def _embed(self, contents, task_type: str):
        return self.client.models.embed_content(
            model=self.model,
            contents=contents,
            config=types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=self.dim,
            ),
        )

    def get_embedding(self, text: str, is_query: bool = False) -> list[float]:
        task = "RETRIEVAL_QUERY" if is_query else "RETRIEVAL_DOCUMENT"
        response = self._embed(text, task)
        return response.embeddings[0].values

    def get_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        response = self._embed(texts, "RETRIEVAL_DOCUMENT")
        return [e.values for e in response.embeddings]