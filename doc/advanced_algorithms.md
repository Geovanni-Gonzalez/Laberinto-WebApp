# Documentación Adicional - Fase 2

## Algoritmos de Generación Avanzados

### 1. Algoritmo de Prim Aleatorio (Orgánico)

- **Concepto**: Comienza con una cuadrícula llena de paredes. Selecciona una celda inicial y añade sus paredes vecinas a una lista. En cada paso, elige una pared aleatoria de la lista. Si la pared separa una celda visitada de una no visitada, derriba la pared y añade las paredes de la nueva celda a la lista.
- **Resultado**: Laberintos con muchas ramas cortas y sin caminos largos y rectos. Aspecto muy "orgánico" o fractal.
- **Diferencia con Backtracking**: Backtracking (DFS) tiende a crear pasillos largos y serpenteantes ("River Factor" bajo). Prim crea una textura más uniforme y ramificada.

### 2. Autómata Celular (Cuevas)

- **Concepto**: Inicializa la cuadrícula con ruido aleatorio (45% paredes). Aplica reglas de simulación de vida (similar a Conway's Game of Life) por varias iteraciones.
  - Regla típica (4-5): Una celda se vuelve pared si tiene >4 vecinos paredes, o espacio si tiene <4.
- **Resultado**: Estructuras tipo cueva, con espacios abiertos grandes y pilares irregulares.
- **Ajustes**: Se implementó una lógica post-procesamiento para encontrar puntos de inicio y fin válidos en los espacios abiertos resultantes.
