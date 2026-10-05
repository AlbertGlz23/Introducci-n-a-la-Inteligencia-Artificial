from pathlib import Path
import time
import httpx

ARTICULOS = {
    "xbox.md": "Xbox",
    "playstation.md": "PlayStation",
    "nintendo.md": "Nintendo",
    "sega.md": "Sega",
    "atari.md": "Atari",
}

URL = "https://es.wikipedia.org/w/api.php"
HEADERS = {
    "User-Agent": "ProyectoRAGUniversidad/1.0 (Tucorreo@ejemplo.com) httpx"
}

carpeta = Path(__file__).resolve().parent / "data"
carpeta.mkdir(exist_ok=True)

for archivo, titulo in ARTICULOS.items():
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": 1,
        "redirects": 1,
        "titles": titulo,
        "format": "json",
    }
    r = httpx.get(URL, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    pagina = next(iter(r.json()["query"]["pages"].values()))
    texto = pagina.get("extract", "")
    (carpeta / archivo).write_text(f"# {titulo}\n\n{texto}", encoding="utf-8")
    print(f"{archivo}: {len(texto.split())} palabras")
    time.sleep(1)