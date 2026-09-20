# Ejercicio 1 - 7 Clustering de K-medias

**Autor:** Alberto Gonzalez

---

## Sección I: Link del notebook del ejercicio
* **Notebook en Google Colab:** [Ver Notebook](https://colab.research.google.com/drive/1GSc1iwB3qoCVb6h8NDyzaFfL089YzsOQ?usp=sharing)

---

## Sección II: Comparativa de Diagramas y Gráficos

| Categoría / Gráfico | Centroides originales | Centroides separados (nuevos) |
| :--- | :---: | :---: |
| **Plano con los centros** | `![Plano Original](assets/Centroides_og.png)` | `![Plano Nuevos](assets/Centroides_new.png)` |
| **Diagrama de dispersión** | `![Dispersión Original](assets/scatter_og.png)` | `![Dispersión Nuevos](assets/scatter_new.png)` |
| **Diagrama de Voronoi (K=5)** | `![Voronoi Original](assets/voronoi_og.png)` | `![Voronoi Nuevos](assets/voronoi_new.png)` |
| **Diagrama de inercia (Codo)** | `![Inercia Original](assets/inertia_og.png)` | `![Inercia Nuevos](assets/inertia_new.png)` |
| **Diagrama de silueta** | `![Silueta Original](assets/silhouette_og.png)` | `![Silueta Nuevos](assets/silhouette_new.png)` |

---

## Sección III: Centros y Dispersión Usados

### Configuración de los Centroides y Desviación Estándar

```python

# Coordenadas (X, Y) de los centroides

    [ 0.4,  2.1],   # Centro 1
    [ 1.2,  2.5],   # Centro 2
    [-3.1,  1.6],   # Centro 3
    [-2.6,  2.9],   # Centro 4
    [-2.9,  0.5]    # Centro 5


# Desviación estándar (dispersión) asociada a cada centroide

    0.35,  # Dispersión del Centro 1
    0.25,  # Dispersión del Centro 2
    0.15,  # Dispersión del Centro 3
    0.08,  # Dispersión del Centro 4
    0.12   # Dispersión del Centro 5

```

## Sección IV: Reporte de resultados

En los datos originales, el método del codo indica un $k = 4$ a pesar de que el conjunto sintético se generó utilizando 5 centros distintos. Esto ocurre porque dos de los agrupamientos originales (nuestros blobs) estaban ubicados tan cerca uno del otro y contaban con una dispersión lo suficientemente amplia como para solaparse de manera considerable. Al estar tan encimados, la inercia experimenta una reducción drástica y sostenida hasta llegar a 4 grupos, punto a partir del cual la ganancia por dividir esos dos bloques encimados resulta matemáticamente minima para dicha métrica. En este escenario original, tanto la gráfica del codo como el coeficiente de silueta favorecían la estructura de 4 clusters por la falta de separación espacial evidente entre ambos grupos.   

Tras realizar la modificación e introducir los nuevos centroides más distanciados en el espacio, la evaluación del modelo cambia. Al observar las gráficas generadas con los nuevos datos, el método del codo y el análisis de silueta ya no sugieren el mismo valor óptimo: mientras que la curva del codo mantiene la inflexión marcada en $k = 4$, la silueta alcanza su punto máximo claramente en $k = 5$. Esto confirma que, con la nueva configuración, la silueta sí reconoce de manera precisa la existencia de los 5 clusters reales, mientras que el codo aún no termina de registrar el quinto grupo como un cambio drástico en la reducción de inercia.

Como la gráfica del codo continúa señalando $k = 4$, el factor decisivo a cambiar es la relación entre la distancia física de los centroides y/o la desviación estándar de cada grupo. Aunque se desplazaron las coordenadas para separar los centros, la dispersión elegida en alguno de los bloques (por ejemplo, el centroide 1 que tiene una desviación de 0.35) sigue haciendo que sus puntos se extiendan hacia el cluster vecino. Para lograr que la curva del codo cambie de opinión y coincida de forma precisa para$k = 5$, se requiere reducir el valor de blob_std en los grupos más extendidos para hacerlos más compactos, o bien aumentar aún más la distancia entre las coordenadas de los centros involucrados, eliminando por completo cualquier solapamiento entre las fronteras de Voronoi.

## Sección V: Evidencias de ejecución

`![Evidencias de ejecución de la notebook](assets/exec_evidences.png)` 