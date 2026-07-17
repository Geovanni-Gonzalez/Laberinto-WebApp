# IMPROVEMENT_ROADMAP — Laberinto-WebApp

Backlog priorizado. Impacto/Esfuerzo: Alto/Medio/Bajo.

## Quick Wins

| # | Mejora | Impacto | Esfuerzo | Prioridad |
|---|---|---|---|---|
| 1 | Limpiar comentarios de razonamiento en vivo en `solver.py` ("Actually, ...") | Alto (credibilidad) | Bajo | P0 |
| 2 | Suite pytest: generadores producen laberintos válidos (conexos, con inicio/fin), solvers hallan camino en laberinto conocido — y ejecutarla en CI (hoy solo `compileall`) | Alto | Bajo | P1 |
| 3 | GitHub Topics: `flask`, `maze-generator`, `backtracking`, `q-learning`, `threejs`, `algorithms` + descripción | Medio | Bajo | P1 |
| 4 | Mover `DOCUMENTACION.md` a `docs/` | Bajo | Bajo | P2 |
| 5 | GIF del render 3D en el README (es el gancho visual del repo) | Medio | Bajo | P1 |

## Mejoras técnicas

| # | Mejora | Impacto | Esfuerzo | Prioridad |
|---|---|---|---|---|
| 6 | Solver BFS/A* explícito etiquetado como "camino más corto garantizado" para contrastar con el DFS | Medio | Bajo | P2 |
| 7 | Métricas comparativas de generadores (longitud media de camino, ramificación) expuestas en la UI | Medio | Medio | P3 |

## Mejoras de GitHub

Ya presentes: badge CI, LICENSE, enunciado en docs, requirements.txt. Faltan: Topics (item 3), demo visual (item 5).
