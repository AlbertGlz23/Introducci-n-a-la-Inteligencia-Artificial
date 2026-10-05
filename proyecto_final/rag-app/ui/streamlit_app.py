import httpx
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG Videojuegos", page_icon="🎮", layout="wide")
st.title("🎮 RAG: historia de las empresas de videojuegos")


def llamar_api(metodo: str, ruta: str, timeout: int = 60, **kwargs):
    """Llama a la API y muestra un error claro si algo falla. Devuelve el JSON o None."""
    try:
        r = httpx.request(metodo, f"{API_URL}{ruta}", timeout=timeout, **kwargs)
    except httpx.ConnectError:
        st.error("No se pudo conectar con la API. ¿Está corriendo uvicorn en el puerto 8000?")
        return None
    except httpx.TimeoutException:
        st.error("La API tardó demasiado en responder. Intenta de nuevo.")
        return None
    if r.status_code >= 400:
        try:
            detalle = r.json().get("detail", r.text)
        except Exception:
            detalle = r.text
        st.error(f"Error {r.status_code}: {detalle}")
        return None
    return r.json()

with st.sidebar:
    st.header("Estado")
    try:
        h = httpx.get(f"{API_URL}/health", timeout=5).json()
        st.success("API conectada")
        st.metric("Chunks indexados", h.get("chunks_indexados", 0))
        if h.get("chunks_indexados", 0) == 0:
            st.info("El índice está vacío. Ve a la pestaña «Indexar documentos».")
    except Exception:
        st.error("API caída o sin conexión")

tab_preguntar, tab_indexar = st.tabs(["Preguntar", "Indexar documentos"])

with tab_preguntar:
    pregunta = st.text_input("Escribe tu pregunta", placeholder="¿Cuándo se lanzó la Sega Saturn?")
    top_k = st.slider("Fragmentos a recuperar (top_k)", 2, 8, 5)

    if st.button("Preguntar", type="primary"):
        if not pregunta.strip():
            st.warning("Escribe una pregunta antes de enviar.")
        else:
            with st.spinner("Buscando y generando respuesta..."):
                datos = llamar_api("POST", "/query", json={"question": pregunta, "top_k": top_k})
            if datos:
                if datos["abstained"]:
                    st.warning(datos["answer"])
                else:
                    st.subheader("Respuesta")
                    st.markdown(datos["answer"].replace("$", "\\$"))

                if datos["citations"]:
                    st.subheader("Fragmentos usados")
                    for c in datos["citations"]:
                        with st.expander(f"[{c['n']}] {c['source']} — score {c['score']:.3f}"):
                            st.progress(max(0.0, min(1.0, c["score"])))
                            st.write(c["text"])


with tab_indexar:
    st.write("Sube archivos o indexa una carpeta que esté en la máquina de la API.")
    archivos = st.file_uploader("Archivos (.txt, .md, .pdf)", type=["txt", "md", "pdf"], accept_multiple_files=True)
    carpeta = st.text_input("O ruta de una carpeta", value="data")

    if st.button("Indexar"):
        if archivos:
            files = [("files", (a.name, a.getvalue(), "application/octet-stream")) for a in archivos]
            data = {}
        elif carpeta.strip():
            files, data = [], {"folder": carpeta.strip()}
        else:
            st.warning("Sube al menos un archivo o escribe una carpeta.")
            files = data = None

        if files is not None:
            with st.spinner("Indexando... puede tardar varios minutos por los límites de la API."):
                res = llamar_api("POST", "/ingest", timeout=900, files=files or None, data=data)
            if res:
                st.success(f"Listo: {res['documentos']} documentos y {res['chunks']} chunks indexados.")