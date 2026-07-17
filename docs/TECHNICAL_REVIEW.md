# TECHNICAL_REVIEW — Laberinto-WebApp

Fecha de revisión: 2026-07-16
Método: análisis estático, enunciado (`docs/Enunciado de Proyecto #1.md`, IC-3002 Análisis de Algoritmos), CI y git. Sin ejecución en esta pasada; CI hace `compileall` (sin tests).

## 1. Comprensión del proyecto

WebApp de laberintos en **Flask + JS** (~1,000 LOC): generación con **3 algoritmos** (recursive backtracking, Prim's, autómata celular), resolución con DFS fuerza-bruta y variante optimizada, un **agente Q-learning** (numpy) que aprende a resolverlos, y visualización 2D (canvas) y **3D (Three.js)**. Guardado/carga de laberintos.

## 2. Cumplimiento del enunciado

| Requisito | Estado | Evidencia |
|---|---|---|
| Backtracking como enfoque central | ✅ estático | `generator.py::_recursive_backtracking`, `solver.py::solve_brute_force` (DFS con pila) |
| Generación aleatoria de laberintos | ✅ estático | 3 algoritmos seleccionables (`generate(algorithm=...)`) |
| Resolver desde punto de partida definido o arbitrario | ✅ estático | `solve_*(start=None)` con override |
| Guardar/cargar soluciones | 🟦 | `app.py` + `saved_mazes/` (no trackeado, correcto) |
| Extras no exigidos | ✅ | Q-learning (`ai_agent.py`), vista 3D (`maze3d.js`), comparación de solvers con orden de visita |

## 3. Fortalezas

1. Tres algoritmos de generación conmutables — muestra comprensión comparativa (backtracking vs Prim vs celular), justo lo que evalúa un curso de análisis de algoritmos.
2. El solver retorna `(camino, orden_visitados)` — diseñado para visualizar la exploración, no solo el resultado.
3. Q-learning de refuerzo aplicado a un segundo dominio (además de BlackJack) — consolida el claim de RL.
4. Doble render 2D/3D con Three.js.

## 4. Debilidades y riesgos

| Hallazgo | Severidad | Nota |
|---|---|---|
| Sin tests; CI solo `compileall` | Media | Los solvers son puros y triviales de testear (laberinto fijo → camino esperado) |
| Comentarios de razonamiento en vivo en `solver.py` ("Actually, standard maze usually has walls.") | Baja-Media | Señal de generación asistida sin limpiar — pulir |
| DOCUMENTACION.md en raíz duplica rol de docs/ | Baja | Mover a `docs/` |

## 5. Evaluación profesional

- Nivel demostrado: **Junior+/Mid en algoritmos aplicados**. La variedad algorítmica y el RL lo suben; la ausencia total de tests en un proyecto de curso de *análisis de algoritmos* es la carencia más visible.
- Rol en el portafolio: refuerza Python/Flask/algoritmos; único por los **algoritmos de generación** y la visualización 3D.

## 6. Recomendaciones

Ver `IMPROVEMENT_ROADMAP.md`. P1: suite pytest de generadores/solvers + CI.
