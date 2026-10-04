def chunk_text(text: str, size: int = 300, overlap: int = 50) -> list[str]:
    if overlap >= size:
        raise ValueError("overlap debe ser menor que size")

    palabras = text.split()
    paso = size - overlap
    chunks = []

    for inicio in range(0, len(palabras), paso):
        trozo = palabras[inicio : inicio + size]
        chunks.append(" ".join(trozo))
        if inicio + size >= len(palabras):
            break

    return chunks