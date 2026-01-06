# Documentación del Proyecto: Laberinto WebApp

## 1. Introducción

Esta aplicación web implementa la generación y resolución de laberintos utilizando algoritmos de backtracking, desarrollada en Python con Flask. El objetivo es visualizar gráficamente cómo diferentes algoritmos abordan la resolución de problemas de búsqueda de caminos.

## 2. Instrucciones de Ejecución

### Requisitos

- Python 3.x instalado.
- Librería `flask`.

### Pasos

1. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar la aplicación:

   ```bash
   python app.py
   ```

3. Abrir en el navegador: `http://localhost:5000`

### Uso de la Herramienta

- **Generar**: Configure el ancho y alto deseado y haga clic en "Generar Laberinto".
- **Resolver**: Seleccione el algoritmo ("Fuerza Bruta" u "Optimizado") y la velocidad de animación, luego haga clic en "Resolver".
- **Interacción**: Haga clic en cualquier camino blanco del laberinto para cambiar el punto de inicio (verde).
- **Persistencia**: Use los botones "Guardar" y "Cargar" para descargar/subir archivos `.json` con la estructura del laberinto.

## 3. Comparación de Algoritmos

### Fuerza Bruta (DFS - Depth First Search)

- **Descripción**: Explora cada ramificación hasta el final antes de retroceder. No tiene conocimiento de dónde está la meta.
- **Ventajas**: Fácil de implementar (recursividad o pila). Garantiza encontrar una solución si existe (en grafos finitos).
- **Desventajas**: Puede recorrer todo el laberinto antes de encontrar la salida si esta se encuentra en la última rama explorada. La solución encontrada casi nunca es la más corta (tiende a ser zigzagueante).
- **Visualización**: Se observa cómo el "buscador" se adentra profundamente en caminos sin salida antes de regresar.

### Optimizado (A* Search)

- **Descripción**: Algoritmo de búsqueda informada. Utiliza una función heurística (en este caso, Distancia Manhattan `|x1-x2| + |y1-y2|`) para estimar qué nodos son prometedores.
- **Ventajas**: Encuentra el camino más corto (si la heurística es admisible). Explora significativamente menos nodos que la fuerza bruta en espacios abiertos o dirigidos.
- **Desventajas**: Mayor complejidad de implementación (requiere cola de prioridad). Consume más memoria al almacenar los costos G y F de cada nodo.
- **Visualización**: Se observa una expansión más "circular" o "dirigida" hacia la meta, evitando explorar rincones opuestos a la salida a menos que sea necesario.

## 4. Estructura del Código

- `app.py`: Controlador principal Flask. Maneja las rutas API.
- `logic/maze.py`: Modelo de datos. Matriz grid, Start/End.
- `logic/generator.py`: Lógica de generación (Backtracking Recursivo).
- `logic/solver.py`: Lógica de resolución (Clase `MazeSolver` con métodos DFS y A*).
- `static/`: Contiene `style.css` y `js/main.js` para el frontend.
- `templates/`: Contiene `index.html`.

## 5. Diseño Modular

Se separó la lógica de negocio (`logic/`) de la capa de presentación (`app.py` + `templates/`). Esto permite cambiar los algoritmos sin afectar la interfaz web, o cambiar la interfaz (a una CLI, por ejemplo) reutilizando la misma lógica.

## 6. Funcionalidades Avanzadas (Fase 2)

### Generación Avanzada

- **Prim's Algorithm**: Seleccionable desde el menú. Genera laberintos orgánicos con muchas bifurcaciones cortas.
- **Autómata Celular**: Genera estructuras tipo cueva naturales en lugar de laberintos de pasillos perfectos.

### Visualización 3D

- **Tecnología**: Three.js.
- **Uso**: Haga clic en el botón "Vista 3D (BETA)" para cambiar a una vista en primera persona.
- **Controles**: Use las teclas `W`, `A`, `S`, `D` para moverse por el laberinto como si fuera un videojuego.

### Inteligencia Artificial (Reinforcement Learning)

- **Agente**: Q-Learning Tabular.
- **Entrenamiento**: El agente no conoce el mapa. Aprende explorando y recibiendo recompensas (+100 meta, -10 pared, -1 paso).
- **Uso**: Configure el número de episodios (ej. 100) y haga clic en "Entrenar". Verá la visualización de la última ruta aprendida (color púrpura).
