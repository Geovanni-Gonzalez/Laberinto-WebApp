"""Tests de generadores y solvers del laberinto (pytest).

Ejecutar desde la raíz del repo: python -m pytest tests/ -q
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from logic.maze import Maze
from logic.generator import MazeGenerator
from logic.solver import MazeSolver


ALGORITHMS = ["recursive_backtracking", "prims", "cellular"]


def _assert_valid_path(maze, path):
    """El camino debe iniciar en start, terminar en end, ser contiguo y transitable."""
    assert path, "no se encontró camino"
    assert tuple(path[0]) == tuple(maze.start)
    assert tuple(path[-1]) == tuple(maze.end)
    for (x, y) in path:
        assert maze.get_cell(x, y) == 0, f"celda ({x},{y}) no es camino"
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        assert abs(x1 - x2) + abs(y1 - y2) == 1, "paso no ortogonal-contiguo"


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_generated_maze_has_open_endpoints(algorithm):
    maze = MazeGenerator().generate(21, 21, algorithm=algorithm)
    assert maze.get_cell(*maze.start) == 0
    assert maze.get_cell(*maze.end) == 0


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_generated_maze_is_solvable_by_dfs(algorithm):
    maze = MazeGenerator().generate(21, 21, algorithm=algorithm)
    path, visited = MazeSolver(maze).solve_brute_force()
    _assert_valid_path(maze, path)
    assert len(visited) >= len(path) - 1


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_generated_maze_is_solvable_by_astar(algorithm):
    maze = MazeGenerator().generate(21, 21, algorithm=algorithm)
    path, _ = MazeSolver(maze).solve_optimized()
    _assert_valid_path(maze, path)


def test_astar_path_never_longer_than_dfs():
    for algorithm in ALGORITHMS:
        maze = MazeGenerator().generate(21, 21, algorithm=algorithm)
        solver = MazeSolver(maze)
        dfs_path, _ = solver.solve_brute_force()
        astar_path, _ = solver.solve_optimized()
        assert len(astar_path) <= len(dfs_path)


def test_solver_on_known_corridor():
    """Laberinto 5x5 hecho a mano: corredor en L de (1,1) a (3,3)."""
    maze = Maze(5, 5)
    for x, y in [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3)]:
        maze.set_cell(x, y, 0)
    maze.start = (1, 1)
    maze.end = (3, 3)
    path, _ = MazeSolver(maze).solve_optimized()
    assert path == [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3)]


def test_solver_with_alternative_start():
    maze = Maze(5, 5)
    for x, y in [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3)]:
        maze.set_cell(x, y, 0)
    maze.end = (3, 3)
    path, _ = MazeSolver(maze).solve_optimized(start=(3, 1))
    assert path == [(3, 1), (3, 2), (3, 3)]


def test_unsolvable_maze_returns_empty():
    maze = Maze(5, 5)
    maze.set_cell(1, 1, 0)
    maze.set_cell(3, 3, 0)  # aislado: sin conexión
    maze.start = (1, 1)
    maze.end = (3, 3)
    path, _ = MazeSolver(maze).solve_brute_force()
    assert not path
    path2, _ = MazeSolver(maze).solve_optimized()
    assert not path2
