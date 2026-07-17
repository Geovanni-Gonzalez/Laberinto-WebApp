# CV_EVIDENCE — Laberinto-WebApp

Verifiable material. Reinforces Python/Flask (BlackJack) and pathfinding (MiniWaze); unique value is maze-generation algorithmics and 3D visualization.

## Resume bullets (pick & adapt)

- Built a maze web application (Flask + JavaScript) featuring three switchable generation algorithms — recursive backtracking, randomized Prim's, and cellular automata — with save/load support.
- Implemented DFS-based and optimized solvers that expose both the solution path and full visit order for step-by-step exploration visualization in 2D (canvas) and 3D (Three.js).
- Trained a tabular Q-learning agent (numpy) to navigate generated mazes, applying reinforcement learning to a second domain beyond card games.

## Unique evidence

| Item | Evidence |
|---|---|
| Comparative generation algorithms (backtracking / Prim / cellular automata) | `logic/generator.py` |
| Visualization-oriented algorithm design (visit-order tracking) | `logic/solver.py` |
| Three.js 3D rendering | `static/js/maze3d.js` (257 LOC) |
| Q-learning in a grid world | `logic/ai_agent.py` (epsilon-greedy, numpy Q-table) |

## ATS keywords (incremental)

Maze generation, backtracking, Prim's algorithm, cellular automata, DFS, reinforcement learning, Q-learning, numpy, Three.js, WebGL, algorithm visualization, Flask.
