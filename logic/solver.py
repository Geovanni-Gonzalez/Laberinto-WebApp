from collections import deque
import heapq

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.width = maze.width
        self.height = maze.height

    def solve_brute_force(self, start=None):
        """
        Resuelve el laberinto utilizando Fuerza Bruta (DFS estándar).
        Explora caminos profundamente hasta encontrar la salida o topar con pared.
        No garantiza el camino más corto, pero es completo.
        
        Args:
            start (tuple): Punto de inicio opcional.
            
        Returns:
            tuple: (camino_solucion, orden_visitados)
        """
        start = start if start else self.maze.start
        end = self.maze.end
        
        stack = [(start, [start])] # (current_pos, path_so_far)
        visited = set()
        visited_order = []

        while stack:
            (cx, cy), path = stack.pop() # LIFO for DFS

            if (cx, cy) == end:
                return path, visited_order

            if (cx, cy) in visited:
                continue
            
            visited.add((cx, cy))
            visited_order.append((cx, cy))

            # Neighbors: Up, Down, Left, Right
            # Check 1 step distance (maze grid path is 0)
            # Actually, standard maze usually has walls.
            # Generator logic: 0 is path, 1 is wall.
            
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            # Brute force: No specific order, or fixed order
            
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.maze.get_cell(nx, ny) == 0 and (nx, ny) not in visited:
                        stack.append(((nx, ny), path + [(nx, ny)]))
        
        return [], visited_order

    def solve_optimized(self, start=None):
        """
        Resuelve el laberinto utilizando A* (Búsqueda Informada).
        Utiliza la distancia Manhattan como heurística para priorizar celdas cercanas a la meta.
        Tiende a encontrar caminos más directos y explora menos celdas innecesarias.
        
        Args:
            start (tuple): Punto de inicio opcional.
            
        Returns:
            tuple: (camino_solucion, orden_visitados)
        """
        start = start if start else self.maze.start
        end = self.maze.end
        
        # Priority Queue: (f_score, current_pos, path)
        # f = g + h
        start_h = abs(start[0] - end[0]) + abs(start[1] - end[1])
        pq = [(start_h, start, [start])]
        
        visited = set()
        visited_order = []
        g_scores = {start: 0}

        while pq:
            _, (cx, cy), path = heapq.heappop(pq)
            
            if (cx, cy) in visited:
                continue
            
            if (cx, cy) == end:
                return path, visited_order

            visited.add((cx, cy))
            visited_order.append((cx, cy))
            
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.maze.get_cell(nx, ny) == 0:
                        new_g = g_scores[(cx, cy)] + 1
                        
                        if (nx, ny) not in g_scores or new_g < g_scores[(nx, ny)]:
                            g_scores[(nx, ny)] = new_g
                            h = abs(nx - end[0]) + abs(ny - end[1])
                            f = new_g + h
                            heapq.heappush(pq, (f, (nx, ny), path + [(nx, ny)]))

        return [], visited_order
