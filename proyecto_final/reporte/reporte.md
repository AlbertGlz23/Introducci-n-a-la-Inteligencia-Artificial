# Reporte: sistema RAG sobre empresas de videojuegos

**Nombre:** ___
**Fecha:** 4 de octubre de 2026

---

## 1. Dominio y tamaño del corpus

El corpus trata sobre la historia de Xbox, PlayStation, Nintendo, Sega y Atari. Son empresas que comparten época y competidores, lo que da un tema coherente y preguntas naturales para probar el sistema.

| Dato | Valor |
|---|---|
| Documentos | 5 (uno por empresa), artículos de Wikipedia en español, licencia CC BY-SA |
| Palabras totales | 32 376 |
| Chunks generados | 131 |
| Modelo de embeddings | gemini-embedding-001 (768 dimensiones) |
| Modelo de generación | gemini-3.8-flash |

## 2. Cómo particioné los documentos

Dividí cada documento en chunks de **300 palabras con solape de 50**, por lo que cada chunk empieza 250 palabras después del anterior (paso = tamaño − solape = 300 − 50). Se parten los textos porque un embedding resume el significado de todo lo que recibe: en un artículo completo se mezclan muchos temas y la búsqueda sería imprecisa, y además solo conviene enviar a Gemini lo relevante. El solape evita que un dato quede cortado entre dos chunks. Elegí valores dentro del rango recomendado (200 a 400 palabras de tamaño, 40 a 80 de solape) porque dan contexto suficiente sin perder precisión.

Comprobación: 32 376 ÷ 250 ≈ 130 chunks esperados; el sistema generó 131, porque cada documento termina con un chunk más corto.

## 3. Cómo decido abstenerme

El sistema tiene dos capas:

1. **Umbral de similitud.** Si el score del fragmento más parecido a la pregunta es menor que **0.60**, la API se abstiene sin llamar a Gemini y muestra los fragmentos recuperados con un mensaje de abstención.
2. **Gemini.** Si el score es de 0.60 o más, Gemini recibe los fragmentos numerados con la instrucción de responder solo con esa evidencia. Si ninguno contiene el dato pedido, responde `NO_HAY_EVIDENCIA` y la API se abstiene.

El umbral solo no basta porque el score mide qué tan parecido es el *tema*, no si el fragmento contiene el *dato*. Una pregunta sobre Nintendo en 2031 obtuvo 0.711, casi igual que las preguntas válidas, y solo Gemini detecta que falta la cifra.

| Pregunta | Score top-1 | Resultado | Capa que decidió |
|---|---|---|---|
| ¿Cuándo se lanzó la Sega Saturn? | 0.778 | Responde con citas | Ninguna: pasa ambas |
| ¿Cuántas consolas vendió Nintendo en 2031? | 0.711 | Se abstiene | Gemini |
| ¿Cuál es la receta del mole poblano? | 0.495 | Se abstiene | Umbral |

## 4. Qué hace Google AI y qué hace Chroma

| Componente | Qué hace | Cuándo interviene |
|---|---|---|
| Google AI: embeddings | Convierte un texto en un vector de 768 números que representa su significado | Al indexar cada chunk y al recibir cada pregunta (siempre el mismo modelo) |
| ChromaDB | Guarda en disco los vectores, textos y metadatos, y busca los vectores más cercanos al de la pregunta | Al indexar (guardar) y al consultar (top-k por similitud coseno) |
| Google AI: generación (Gemini) | Lee los fragmentos recuperados y redacta una respuesta en español con citas `[n]`, o se abstiene | Solo si el score supera el umbral |

**Recorrido de una pregunta:** Streamlit envía la pregunta a FastAPI → se convierte en vector con Google AI → Chroma devuelve los 5 fragmentos más cercanos con su score → si el mejor supera 0.60, Gemini redacta la respuesta → Streamlit muestra la respuesta, las citas y los fragmentos.

**Persistencia:** Chroma escribe el índice en la carpeta `chroma/`, por lo que al reiniciar la API los 131 chunks siguen disponibles sin volver a indexar.

## 5. Limitaciones

- Una pregunta vaga puede recuperar fragmentos del tema correcto sin el dato. «¿Qué consola lanzó Sega tras la Genesis?» se abstuvo, y al reformularla como «¿Cuándo se lanzó la Sega Saturn?» respondió bien. El sistema prefiere abstenerse a inventar.
- El umbral de 0.60 se calibró con pocas preguntas de prueba.
- El plan gratuito de Google limita la cuota y a veces responde con errores temporales (429 o 503); la API reintenta automáticamente.
- Los chunks se cortan por número de palabras, no por oraciones, por lo que pueden empezar a mitad de una frase.

---

*Corpus: Wikipedia en español (CC BY-SA), artículos Xbox, PlayStation, Nintendo, Sega y Atari.*
