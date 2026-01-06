import random
from .maze import Maze

class MazeGenerator:
    def __init__(self):
        pass

    def generate(self, width, height, algorithm='recursive_backtracking'):
        """
        Genera un laberinto utilizando el algoritmo especificado.
        
        Args:
            width (int): Ancho deseado.
            height (int): Alto deseado.
            algorithm (str): 'recursive_backtracking', 'prims', o 'cellular'.
            
        Returns:
            Maze: Objeto Maze generado.
        """
        # Ensure odd dimensions for wall/path logic (except cellular which is flexible)
        if width % 2 == 0: width += 1
        if height % 2 == 0: height += 1
        
        maze = Maze(width, height)
        
        if algorithm == 'prims':
            self._prims_algorithm(maze)
        elif algorithm == 'cellular':
            self._cellular_automata(maze)
        else:
            # Default: Recursive Backtracking
            start_x, start_y = 1, 1
            maze.set_cell(start_x, start_y, 0)
            self._recursive_backtracking(maze, start_x, start_y)
        
        # Set start and end logic (shared for wall-based mazes)
        if algorithm != 'cellular':
            maze.start = (1, 1)
            maze.end = (width - 2, height - 2)
            if maze.get_cell(*maze.end) == 1:
                maze.set_cell(*maze.end, 0)
        else:
            # Cellular automata needs specific start/end finding
            self._find_start_end_cellular(maze)

        return maze

    def _prims_algorithm(self, maze):
        """
        Implementación del Algoritmo de Prim Aleatorio.
        Genera laberintos con ramas cortas y muchas bifurcaciones.
        """
        start_x, start_y = 1, 1
        maze.set_cell(start_x, start_y, 0)
        
        # Walls list: (x, y, parent_x, parent_y)
        walls = []
        self._add_walls(maze, start_x, start_y, walls)
        
        while walls:
            # Randomly select a wall
            idx = random.randint(0, len(walls) - 1)
            wx, wy, px, py = walls[idx]
            walls.pop(idx)
            
            # Check if it connects to an unvisited cell
            # Direction from parent to wall
            dx, dy = wx - px, wy - py
            # Target cell
            tx, ty = wx + dx, wy + dy
            
            if 0 < tx < maze.width - 1 and 0 < ty < maze.height - 1:
                if maze.get_cell(tx, ty) == 1:
                    # Carve through wall and target
                    maze.set_cell(wx, wy, 0)
                    maze.set_cell(tx, ty, 0)
                    # Add walls of the new cell
                    self._add_walls(maze, tx, ty, walls)

    def _add_walls(self, maze, cx, cy, walls):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            wx, wy = cx + dx, cy + dy
            if 0 < wx < maze.width - 1 and 0 < wy < maze.height - 1:
                if maze.get_cell(wx, wy) == 1:
                    # Check if it's not a border (simplification)
                    # Actually we just add it, check validity later
                    walls.append((wx, wy, cx, cy))

    def _cellular_automata(self, maze, iterations=5):
        """
        Simulación de Autómata Celular para generar cuevas.
        Regla común: 4-5.
        """
        # Random initialization (45% walls)
        for y in range(1, maze.height - 1):
            for x in range(1, maze.width - 1):
                if random.random() < 0.45:
                    maze.set_cell(x, y, 1)
                else:
                    maze.set_cell(x, y, 0)
        
        # Simulation steps
        for _ in range(iterations):
            new_grid = [row[:] for row in maze.grid]
            for y in range(1, maze.height - 1):
                for x in range(1, maze.width - 1):
                    neighbors = self._count_wall_neighbors(maze, x, y)
                    if neighbors > 4:
                        new_grid[y][x] = 1 # Become wall
                    elif neighbors < 4:
                        new_grid[y][x] = 0 # Become space
            maze.grid = new_grid
            
    def _count_wall_neighbors(self, maze, x, y):
        walls = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0: continue
                nx, ny = x + dx, y + dy
                # Out of bounds counts as wall
                if nx < 0 or nx >= maze.width or ny < 0 or ny >= maze.height:
                    walls += 1
                elif maze.get_cell(nx, ny) == 1:
                    walls += 1
        return walls

    def _find_start_end_cellular(self, maze):
        # Find first open cell for start
        found_start = False
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.get_cell(x, y) == 0:
                    maze.start = (x, y)
                    found_start = True
                    break
            if found_start: break
            
        # Find last open cell for end
        found_end = False
        for y in range(maze.height - 1, -1, -1):
            for x in range(maze.width - 1, -1, -1):
                if maze.get_cell(x, y) == 0:
                    maze.end = (x, y)
                    found_end = True
                    break
            if found_end: break

    def _recursive_backtracking(self, maze, cx, cy):
        """
        Algoritmo recursivo que cava caminos en direcciones aleatorias.
        Args:
            maze (Maze): Instancia del laberinto.
            cx, cy (int): Coordenadas actuales.
        """
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy

            if 0 < nx < maze.width - 1 and 0 < ny < maze.height - 1:
                if maze.get_cell(nx, ny) == 1:
                    # Carve path to new cell
                    maze.set_cell(nx, ny, 0)
                    # Carve wall between
                    maze.set_cell(cx + dx // 2, cy + dy // 2, 0)
                    
                    self._recursive_backtracking(maze, nx, ny)
