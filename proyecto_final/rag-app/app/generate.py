import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MODELOS = ["gemini-3.8-flash", "gemini-3.8-flash-lite"]
SIN_EVIDENCIA = "NO_HAY_EVIDENCIA"

INSTRUCCIONES = f"""Eres un asistente que responde preguntas usando SOLO los fragmentos numerados que se te dan.
Reglas:
1. Responde siempre en español.
2. Usa únicamente información que aparezca en los fragmentos. No uses conocimiento propio.
3. Cita cada afirmación con el número del fragmento, por ejemplo [1] o [2][3].
4. Puedes combinar información de varios fragmentos. Si la respuesta se deduce razonablemente de ellos, respóndela citando cada uno.
5. Responde SOLO con la palabra {SIN_EVIDENCIA}, sin nada más, si ningún fragmento aporta información sobre lo que se pregunta, o si el dato concreto que se pide (una fecha, una cifra, un nombre) no aparece en ninguno. Que el tema coincida no basta."""


class Generator:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY no encontrada en el archivo .env")
        self.client = genai.Client(api_key=api_key)

    def answer(self, question: str, citations: list[dict]) -> tuple[str, bool]:
        """Devuelve (respuesta, abstained)."""
        contexto = "\n\n".join(f"[{c['n']}] ({c['source']}) {c['text']}" for c in citations)
        prompt = f"Fragmentos:\n{contexto}\n\nPregunta: {question}"

        resp = None
        ultimo_error = None
        for modelo in MODELOS:
            espera = 3
            for intento in range(4):
                try:
                    resp = self.client.models.generate_content(
                        model=modelo,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=INSTRUCCIONES,
                            temperature=0.0,
                        ),
                    )
                    break
                except (ServerError, ClientError) as e:
                    ultimo_error = e
                    if e.code in (429, 500, 503):
                        time.sleep(espera)
                        espera *= 2
                    else:
                        raise
            if resp is not None:
                break

        if resp is None:
            raise ultimo_error

        texto = (resp.text or "").strip()
        if not texto or SIN_EVIDENCIA in texto:
            return "No tengo evidencia suficiente en los documentos para responder.", True
        return texto, False