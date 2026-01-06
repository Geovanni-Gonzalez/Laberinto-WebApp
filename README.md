# Laberinto WebApp v2.0 🚀

Una aplicación web profesional para la generación, resolución y visualización de laberintos, potenciada con **Inteligencia Artificial** y **Gráficos 3D**.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-yellow.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Características Principales

### 🧠 Generación Avanzada

- **Backtracking Recursivo**: Pasillos largos y perfectos.
- **Algoritmo de Prim**: Laberintos orgánicos y fractales.
- **Autómata Celular**: Estructuras tipo cueva/mapa RPG.

### 🎮 Visualización Inmersiva

- **Vista 2D (Canvas)**: Renderizado rápido y limpio.
- **Vista 3D (Three.js)**: Explora tu laberinto en primera persona con controles FPS (WASD + Mouse).
- **Interfaz Moderna**: Diseño "Cyberpunk" con barra lateral y tema oscuro.

### 🤖 Inteligencia Artificial

- **Agente Q-Learning**: Entrena una IA en tiempo real para que aprenda a resolver cualquier mapa por sí misma.
- **Visualización de Aprendizaje**: Observa la ruta lógica (púrpura) que el agente deduce tras su entrenamiento.

### ⚡ Resolución Clásica

- **DFS (Fuerza Bruta)**: Búsqueda en profundidad.
- **A* (Optimizado)**: Búsqueda heurística inteligente (Manhattan).

## 🛠️ Instalación y Uso

1. **Clonar repositorio**:

    ```bash
    git clone https://github.com/tu-usuario/Laberinto-WebApp.git
    cd Laberinto-WebApp
    ```

2. **Instalar dependencias**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Ejecutar**:

    ```bash
    python app.py
    ```

4. **Abrir**: Navega a `http://localhost:5000`

## 📂 Estructura del Proyecto

- `app.py`: Backend Flask (API).
- `logic/`: Núcleo algorítmico (Generadores, Solvers, IA).
- `static/`: Frontend (JS modular, Three.js, CSS).
- `templates/`: HTML5.

## 🤝 Créditos

Desarrollado como proyecto educativo de algoritmia y sistemas inteligentes.
