import json

class Maze:
    """
    Representa la estructura de datos del laberinto.
    Almacena la cuadrícula (grid), dimensiones y puntos de inicio/fin.
    """
    def __init__(self, width=20, height=20):
        """
        Inicializa un laberinto lleno de paredes.
        Args:
            width (int): Ancho del laberinto.
            height (int): Alto del laberinto.
        """
        self.width = width
        self.height = height
        # 1 = Wall, 0 = Path
        # Initialize with walls
        self.grid = [[1 for _ in range(width)] for _ in range(height)]
        self.start = (1, 1)  # Default start
        self.end = (width - 2, height - 2) # Default end, usually adjusted by generator

    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "grid": self.grid,
            "start": self.start,
            "end": self.end
        }

    def from_dict(self, data):
        self.width = data.get("width", 20)
        self.height = data.get("height", 20)
        self.grid = data.get("grid", [])
        self.start = tuple(data.get("start", (1, 1)))
        self.end = tuple(data.get("end", (self.width - 2, self.height - 2)))
    
    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
