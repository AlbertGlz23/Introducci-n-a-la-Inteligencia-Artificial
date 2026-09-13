import http.server
import os
import socketserver
import sys
import threading
import webbrowser

PORT = 8000
HTML_FILE = "mexico_map.html"


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(folder)

    if not os.path.exists(HTML_FILE):
        print(f"Error: no se encontró {HTML_FILE} en {folder}")
        sys.exit(1)

    handler = http.server.SimpleHTTPRequestHandler
    url = f"http://localhost:{PORT}/{HTML_FILE}"

    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            threading.Timer(0.5, lambda: webbrowser.open(url)).start()

            print(f"Sirviendo en {url}")
            print("Presiona Ctrl+C para detener el servidor.")

            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    except OSError as e:
        print(f"Error: no se pudo iniciar el servidor en el puerto {PORT}. {e}")
        print("¿Ya hay otro servidor corriendo en ese puerto?")
        sys.exit(1)


if __name__ == "__main__":
    main()
