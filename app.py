from flask import Flask, render_template, jsonify, request
import os
import json

app = Flask(__name__)
app.secret_key = 'laberinto_secret_key'

# Ensure saved_mazes directory exists
MAZES_DIR = os.path.join(os.path.dirname(__file__), 'saved_mazes')
if not os.path.exists(MAZES_DIR):
    os.makedirs(MAZES_DIR)

from logic.maze import Maze
from logic.generator import MazeGenerator
from logic.solver import MazeSolver
from logic.ai_agent import QLearningAgent

# Global storage (simple in-memory)
current_maze = None
ai_agent = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_maze():
    global current_maze, ai_agent
    data = request.json
    width = int(data.get('width', 20))
    height = int(data.get('height', 20))
    algo = data.get('algo', 'recursive_backtracking')
    
    gen = MazeGenerator()
    current_maze = gen.generate(width, height, algo)
    
    # Initialize new AI agent for this maze
    ai_agent = QLearningAgent(current_maze)
    
    return jsonify({
        "status": "ok", 
        "maze": current_maze.to_dict()
    })

@app.route('/api/train', methods=['POST'])
def train_agent():
    global ai_agent
    if not ai_agent:
        return jsonify({"status": "error", "message": "No maze/agent initialized"}), 400
    
    episodes = request.json.get('episodes', 1)
    last_trace = []
    
    for _ in range(episodes):
        last_trace = ai_agent.train_episode()
        
    return jsonify({
        "status": "ok",
        "trace": last_trace,
        "episodes_run": episodes
    })

@app.route('/api/solve', methods=['POST'])
def solve_maze():
    global current_maze
    if not current_maze:
        # Try finding a maze in request or fail
        data = request.json
        if 'maze' in data:
            current_maze = Maze()
            current_maze.from_dict(data['maze'])
        else:
            return jsonify({"status": "error", "message": "No maze generated"}), 400

    data = request.json
    method = data.get('method', 'brute_force')
    start_x = data.get('start_x')
    start_y = data.get('start_y')
    
    start = None
    if start_x is not None and start_y is not None:
        start = (start_x, start_y)

    solver = MazeSolver(current_maze)
    
    if method == 'optimized':
        path, visited = solver.solve_optimized(start)
    else:
        path, visited = solver.solve_brute_force(start)

    return jsonify({
        "status": "ok",
        "solution": path,
        "visited": visited
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
