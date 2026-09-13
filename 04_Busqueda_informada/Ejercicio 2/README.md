# Mexico Cities Graph — Mapa interactivo de rutas

Visualización interactiva de 1,000 ciudades de México como un grafo de proximidad, con búsqueda de rutas más cortas (algoritmo A* + distancia Haversine) directamente desde el navegador.

## Contenido del proyecto

| Archivo | Descripción |
|---|---|
| `mexico_map.html` | Mapa interactivo (buscador de ciudades, filtro por estado, cálculo de rutas). |
| `mexico_cities_graph.json` | Datos del grafo (ciudades, coordenadas, conexiones). Requerido por el HTML y por `find_route.py`. |
| `find_route.py` | Script de línea de comandos que calcula la misma ruta que el mapa, útil para verificar resultados. |
| `run_map.py` | Levanta el servidor local y abre el mapa automáticamente. |
| `iniciar_mapa.bat` | Lanzador de doble clic (Windows) que ejecuta `run_map.py`. |

Todos los archivos deben estar en la **misma carpeta** para que todo funcione correctamente.

## Cómo iniciar el mapa (uso normal)

El proyecto está automatizado: no es necesario escribir comandos.

1. Haz doble clic en **`iniciar_mapa.bat`**.
2. Esto abre automáticamente:
   - Una ventana de terminal, que mantiene corriendo el servidor local.
   - El mapa (`mexico_map.html`) en tu navegador predeterminado.
3. Usa el mapa con normalidad: busca ciudades, filtra por estado, y calcula rutas con el buscador "Find a route (A*)".

> **Nota:** la ventana de terminal debe permanecer abierta mientras usas el mapa — es la que sirve los datos al navegador. Minimizarla está bien; cerrarla detiene el servidor.

## Cómo cerrar todo correctamente

Para evitar procesos colgados, cierra las ventanas en este orden:

1. **Cierra primero la pestaña/ventana del navegador** con el mapa.
2. **Luego cierra la ventana de terminal** que se abrió junto con el mapa (o presiona `Ctrl + C` dentro de ella y después ciérrala).

## Verificación manual con `find_route.py` (opcional)

Si quieres confirmar el resultado de una ruta calculada en el mapa desde la línea de comandos:

1. Abre una terminal **en la misma carpeta** donde están `find_route.py` y `mexico_cities_graph.json`.
2. Ejecuta:

   ```bash
   python find_route.py --from-city "NOMBRE_ORIGEN" --to "NOMBRE_DESTINO"
   ```

   Por ejemplo:

   ```bash
   python find_route.py --from-city "Higuera de Zaragoza" --to "Tamazula de Gordiano"
   ```

3. El script imprime la ruta encontrada y el costo total en kilómetros. Este número debería coincidir con el que muestra el mapa para la misma ruta, ya que ambos usan el mismo grafo (`mexico_cities_graph.json`) y el mismo algoritmo (A* con heurística Haversine).

> Si el nombre de una ciudad existe en más de un estado, el script te lo indicará y listará las opciones para que lo especifiques de forma única.

## Requisitos

- Python 3 instalado y disponible en el PATH (`python` o `python3`, según el sistema).
- Un navegador web moderno (Chrome, Firefox, Edge, etc.).
