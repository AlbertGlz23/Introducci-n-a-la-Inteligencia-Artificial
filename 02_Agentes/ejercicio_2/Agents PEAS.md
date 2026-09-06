# Agentes - Ejercicio 2

Para cada una de las 8 aplicaciones listadas abajo, redacta una descripción PEAS completa y coherente. Debes pensar como diseñador del agente: qué optimiza, dónde actúa, con qué puede mover o modificar el mundo, y qué puede observar.

---

### 1. Asistente virtual de voz

| Componente | Significado | Descripción |
| :---: | :--- | :--- |
| **P** | *Performance* (medida de desempeño) | El rendimiento de una aplicación de asistente de voz virtual se determina con base en qué tan bien comprende el lenguaje de la persona con la que interactúa, qué tan bien comprende la persona la respuesta generada por la aplicación (que tenga sentido en la conversación), qué tan confiables son las respuestas generadas, en caso de que cometa un error cuántas interacciones necesita para corregirse, medidas estándar como la eficiencia en cuanto al tiempo que le toma dar una respuesta y, por último, si la respuesta logró cumplir el objetivo por el cual se inició la interacción. |
| **E** | *Environment* (entorno) | Las aplicaciones de asistentes de voz virtuales generalmente se desenvuelven en tres diferentes entornos: 1. Este tipo de aplicaciones utiliza servicios de la nube para poder optimizar los tiempos y recursos a utilizar del dispositivo, por lo tanto, tienen que interactuar con el entorno de la nube. 2. Las aplicaciones de asistentes de voz tienen que ir instaladas en un dispositivo electrónico, por lo tanto, interactúan directamente con el hardware del dispositivo en el que están instaladas y dependen de él para delimitar sus capacidades. 3. Las aplicaciones de asistentes virtuales tienen que interactuar con el mundo real, ya que son desarrolladas en su mayoría para poder servir a un propósito de asistencia a un usuario real (persona) que se desenvuelve en el mundo real. |
| **A** | *Actuators* (actuadores) | La mayoría de las aplicaciones de asistentes virtuales utilizan Grandes Modelos de Lenguaje como sus motores principales. Estos, combinados con modelos de reconocimiento de lenguaje natural, de reconocimiento de voz y en algunos casos modelos generativos, permiten transformar la información recibida en la respuesta esperada. Esta respuesta, una vez generada, es comunicada al usuario en el mundo real mediante el uso de bocinas u otro hardware que permita comunicar las respuestas con voz o texto. |
| **S** | *Sensors* (sensores) | Los principales sensores de las aplicaciones de asistentes virtuales son los micrófonos, ya que estos son los que permiten a la aplicación recibir la información para que sus actuadores puedan utilizarla. |

---

### 2. Robot aspirador doméstico

| Componente | Significado | Descripción |
| :---: | :--- | :--- |
| **P** | *Performance* (medida de desempeño) | Algunas de las métricas que nos permiten evaluar a un robot aspirador son: qué tan bien realiza la limpieza (aspirado) del piso de la casa, el tiempo que le toma realizar la limpieza total del piso, la cantidad de carga que consume para realizar la limpieza total o parcial del piso, cuánto tiempo le toma recargarse para poder volver a limpiar el piso y qué tanto tiempo durará en su funcionamiento óptimo hasta que sea necesario reemplazarlo. |
| **E** | *Environment* (entorno) | Este aparato se desenvuelve interactuando con el mundo exterior, ya que si bien cuenta con un hardware que le permite realizar una limpieza inteligente, este lo que hace es transformar el entorno a limpiar en un mapa que traza el robot aspirador para saber dónde ya limpió y dónde le falta limpiar. Por lo tanto, requiere de interacción con el mundo real para que sus sensores puedan realizar este mapeo a una forma que entienda el aparato. |
| **A** | *Actuators* (actuadores) | Los principales actuadores de un robot aspirador son todos aquellos componentes de hardware que le permiten llevar a cabo su tarea de limpieza. Algunos de ellos son: las ruedas y los motores, el sistema de limpieza (aspiradora y barredora), sus mecanismos de vaciado automático si es que los tiene, indicadores digitales como pantallas o LEDs, bocinas u otro sistema que le permita comunicación con el mundo real y los módulos Wi-Fi o Bluetooth que le permiten comunicarse con el usuario. |
| **S** | *Sensors* (sensores) | Los sensores más relevantes de la mayoría de los robots aspiradores son aquellos que le permiten mapear y definir el entorno donde se estarán moviendo, tales como: LiDARs, cámaras frontales y/o laterales, sensores de colisión, sensores anticaída, sensores de seguimiento de pared y odómetros que le permiten determinar qué tanta distancia lleva y calcular un aproximado de dónde está. También cuentan con otros componentes como sensores ultrasónicos que le permiten determinar si el suelo está sucio, sensores de textura para determinar si sigue en el piso o en otro lado como alfombras y un sensor que le avisa al robot aspirador cuando el contenedor está lleno. |

---

### 3. Sistema de recomendación de streaming

| Componente | Significado | Descripción |
| :---: | :--- | :--- |
| **P** | *Performance* (medida de desempeño) | Las métricas principales para un sistema de recomendación de streaming podrían ser: la cantidad de usuarios que le dieron una reseña favorable o un "me gusta" a una recomendación hecha, la cantidad de tiempo que un usuario vio una recomendación, la similitud entre las recomendaciones realizadas comparadas con el contenido visto anteriormente por el usuario y una retroalimentación respecto al nivel de serendipia que utiliza el sistema. |
| **E** | *Environment* (entorno) | Los sistemas de recomendación de streaming generalmente se desenvuelven en entornos de la nube donde interactúan con el catálogo de contenido de la plataforma, los registros de los perfiles de los usuarios y contenidos, y los servicios web que utilizan para hacer funcionar la interfaz de usuario de la plataforma. Este sistema, mediante el ambiente de la interfaz de usuario, puede interactuar con este para presentarle los contenidos y determinar las acciones a realizar; también tiende a interactuar con el hardware del dispositivo donde se ejecuta para determinar las delimitaciones de reproducción que pueden tener los contenidos. |
| **A** | *Actuators* (actuadores) | Los sistemas de recomendación tienen un conjunto de actuadores que se centran en modificaciones de pantallas y comandos de software para atraer la atención del usuario. Utilizan herramientas como notificaciones push y correos al usuario, interfaces de listas y/o carruseles personalizados y llamativos, sistemas de reproducción automática para captar la atención mediante fragmentos del contenido, y sistemas de filtrado y búsqueda enfocados en el perfil del usuario con el que interactúan. |
| **S** | *Sensors* (sensores) | La mayoría de los sensores que tienen estos sistemas se encuentran implícitos dentro de las métricas e interfaces de las plataformas, ya que este sistema aprende y recibe información mediante los clics en la interfaz, las métricas de omisión, las acciones explícitas del usuario en la plataforma, sus retroalimentaciones y los metadatos que obtiene de las sesiones y perfiles de los usuarios y contenidos vistos. |

---

### 4. Vehículo autónomo en ciudad

| Componente | Significado | Descripción |
| :---: | :--- | :--- |
| **P** | *Performance* (medida de desempeño) | Las empresas que desarrollan este tipo de vehículos tienen algunas métricas bien delimitadas para determinar el rendimiento. Algunas son: el número de colisiones o accidentes que tenga el vehículo en el mundo real o en un entorno de pruebas, la cantidad de intervenciones humanas que requiere para poder realizar una conducción segura, la cantidad de normas de tránsito que cumple de manera correcta, los tiempos de viaje y la eficiencia en el trazo de las rutas a seguir, la comodidad y seguridad que sienten los pasajeros durante la conducción, el tiempo de acción y reacción que le toma ante posibles accidentes y el consumo de energía o combustible que requiere el vehículo en cuanto a una unidad de tiempo (generalmente un día) antes de necesitar recargarse. |
| **E** | *Environment* (entorno) | El entorno en que se desenvuelve este tipo de vehículo es el mundo real, ya que necesita de todos sus sensores y actuadores para poder determinar rutas a seguir, acciones a tomar y posibles peligros que puedan experimentar la unidad y el usuario durante la conducción. Todo esto es traducido y efectuado la mayoría de las veces por el hardware del vehículo, aunque algunas funciones como el trazado y recalculado de rutas requieren de interacciones con servicios en la nube. |
| **A** | *Actuators* (actuadores) | Este tipo de vehículo tiene un conjunto de actuadores que le permiten desempeñar sus funciones. Los principales son los sistemas que lo definen como vehículo: al ser generalmente automóviles, sistemas como los motores, las baterías, las luces, el sistema hidráulico, de frenos y de tracción son de lo más común. Además, la mayoría cuenta con sistemas de audio para dar retroalimentación al usuario y sistemas incorporados o enlazados con servicios web que permiten la conducción autónoma. |
| **S** | *Sensors* (sensores) | Este tipo de vehículo tiene muchos sensores, algunos de ellos muy sofisticados, pero la mayoría cuenta con sensores LiDAR para determinar distancias, cámaras en los cuatro puntos del auto, sistemas especializados en proximidad, sensores de colisión e incluso, en algunos casos, sensores que permiten monitorear al ocupante. |

---

### 5. Agente de trading algorítmico en bolsa

| Componente | Significado | Descripción |
| :---: | :--- | :--- |
| **P** | *Performance* (medida de desempeño) | Las empresas y las personas que usan este agente miden su éxito con metas financieras muy claras. Algunas de las principales son: la cantidad de dinero ganado con las inversiones, el porcentaje de compras o ventas hechas con éxito, la capacidad para evitar pérdidas grandes cuando cae el mercado, la velocidad para comprar o vender al precio exacto que buscaba, el respeto a los límites de presupuesto establecidos y el control de las comisiones que cobra la plataforma por cada movimiento. |
| **E** | *Environment* (entorno) | El entorno donde opera este agente es el mercado financiero en internet, por ejemplo las bolsas de valores o sitios de criptomonedas. Es un espacio digital que cambia a cada segundo y donde las cosas no siempre se pueden predecir. Está formado por las listas de precios de compra y venta, noticias del mundo económico, otros programas que también compiten ahí, personas comprando o vendiendo y los servidores de internet donde se procesa toda la información. |
| **A** | *Actuators* (actuadores) | El agente realiza acciones enviando órdenes digitales a la plataforma del mercado. Sus principales herramientas para interactuar son: enviar órdenes automáticas de compra o venta de acciones, cambiar o cancelar peticiones que todavía no se ejecutan, ajustar la cantidad de dinero en cada movimiento, activar límites para cerrar operaciones si el precio cae feo, mandar alertas al usuario y apagar el sistema por completo si nota un comportamiento muy peligroso en el mercado. |
| **S** | *Sensors* (sensores) | Para poder tomar decisiones en pocos segundos, este agente utiliza programas que le envían información constante. Sus sensores incluyen: el seguimiento de los precios en tiempo real, la cantidad de acciones disponibles para comprar o vender, el volumen de movimientos que está haciendo la gente, indicadores que calculan si el precio va subiendo o bajando, noticias de finanzas y los datos de la propia cuenta como el saldo disponible y las compras que están abiertas. |

---

### 6. Sistema de diagnóstico médico asistido por IA

| Componente | Significado | Descripción |
| :---: | :--- | :--- |
| **P** | *Performance* (medida de desempeño) | Los hospitales y los médicos evalúan qué tan bien funciona este sistema usando varias formas de medición. Por ejemplo: el porcentaje de diagnósticos acertados, evitar al máximo pasar por alto enfermedades graves, la velocidad para revisar estudios o imágenes, qué tan claras son sus explicaciones para el médico, qué tanto acepta el doctor sus sugerencias y la mejora en el tiempo que tardan en atender a los pacientes. |
| **E** | *Environment* (entorno) | El entorno donde trabaja este sistema es el área médica de un hospital o clínica. Es un ambiente digital pero con mucha información compleja. Se compone de los expedientes electrónicos de los pacientes, los programas donde se ven las radiografías o tomografías, bases de datos con libros e investigaciones médicas, el historial de salud del paciente, los doctores con los que interactúa y las reglas de privacidad sobre datos de salud. |
| **A** | *Actuators* (actuadores) | Como es un sistema pensado para apoyar, no aplica medicinas ni tratamientos al paciente por sí solo, sino que muestra respuestas digitales en la pantalla del médico. Sus acciones son: señalar o encerrar zonas sospechosas en las radiografías, generar listas con las enfermedades más probables, enviar avisos si hay medicamentos que no se deben combinar, recomendar estudios extra si hacen falta y mandar alertas de prioridad para pacientes graves. |
| **S** | *Sensors* (sensores) | Este sistema recibe datos por medio de conexiones directas con las computadoras del hospital. Sus sensores recopilan información como: las imágenes médicas digitalizadas, los signos vitales medidos al momento o registrados antes (como presión o temperatura), los resultados de análisis de laboratorio, la lista de síntomas que anotó el médico, los antecedentes familiares y las guías de salud actualizadas. |

---

### 7. Dron de inspección de infraestructura

| Componente | Significado | Descripción |
| :---: | :--- | :--- |
| **P** | *Performance* (medida de desempeño) | Las empresas de construcción y mantenimiento miden el rendimiento de este tipo de drones según qué tan bien hace sus revisiones. Por ejemplo: qué tan exacto es para encontrar grietas, fuga de líquidos o corrosión, no mandar falsas alarmas de fallas que no existen, revisar toda la estructura sin dejar partes sin ver, el buen uso de la batería, evitar chocar con la construcción o con cosas cercanas y el tiempo total que tarda en revisar la obra comparado con un trabajo hecho a mano. |
| **E** | *Environment* (entorno) | El entorno donde opera este dron es el espacio físico al aire libre o dentro de construcciones cerca de obras grandes, por ejemplo puentes, torres de luz, tuberías o edificios. Es un lugar en tres dimensiones que cambia todo el tiempo, donde hay viento, cambios en la luz del sol, polvo, presencia de aves, árboles alrededor e interferencias en la señal causadas por las mismas estructuras de metal. |
| **A** | *Actuators* (actuadores) | Este dron interactúa con el mundo mediante sus piezas mecánicas y digitales para moverse y tomar datos. Sus actuadores principales son: los motores y las hélices para volar (subir, girar, frenar o quedarse quieto en el aire), el motor del soporte de la cámara para mover el lente a donde se necesite, encender luces o linternas si está oscuro, mandar señales de aviso o regresar a su base, y transmitir la señal de video e informes en tiempo real a la pantalla del operador. |
| **S** | *Sensors* (sensores) | Para poder volar sin peligro y revisar las construcciones, este dron usa sensores físicos y ópticos. Entre ellos están: cámaras de alta resolución (normales y térmicas), sensores de distancia o ultrasonido para medir espacios y no chocar, módulo de localización por satélite para saber su posición exacta, un sensor de presión para medir la altura, giroscopios y acelerómetros para mantenerse estable en el aire y un medidor del nivel de batería. |

---

### 8. Agente jugador de ajedrez

| Componente | Significado | Descripción |
| :---: | :--- | :--- |
| **P** | *Performance* (medida de desempeño) | El éxito de este agente se mide con cosas puntuales dentro del juego, por ejemplo: cuántas partidas les gana a otros jugadores humanos o programas, el aumento en su puntuación de nivel, la precisión al mover las piezas evitando descuidos o jugadas débiles, la cantidad de turnos que le toma ganar la partida y la buena administración del tiempo de su reloj para no perder porque se le acabó el tiempo. |
| **E** | *Environment* (entorno) | El entorno donde opera este agente es el tablero de ajedrez. Puede ser un tablero físico en el mundo real (usando un tablero electrónico o un brazo de robot) o un entorno totalmente digital dentro de una página web o aplicación. Es un lugar donde todo está a la vista, las reglas no cambian, el espacio es de 8 por 8 casillas y las jugadas van turnadas entre dos jugadores. |
| **A** | *Actuators* (actuadores) | El agente actúa enviando la decisión de su jugada. Si está en una aplicación digital, sus actuadores son las órdenes de programa que mueven una pieza de una casilla a otra en la pantalla (por ejemplo, mandar la instrucción de mover el caballo de la casilla g1 a la casilla f3). Si está en un tablero físico, sus actuadores son los motores de un brazo de robot que toma la pieza y la cambia de lugar en el tablero real. |
| **S** | *Sensors* (sensores) | Para saber cómo va la partida, este agente usa sensores para leer el estado del tablero. Si es en programa, el sensor es un lector de texto que recibe la jugada del rival escrita en el sistema. Si es en un tablero real en el mundo físico, utiliza cámaras con visión por computadora o sensores con imanes debajo del tablero para detectar qué pieza está en cada casilla. |