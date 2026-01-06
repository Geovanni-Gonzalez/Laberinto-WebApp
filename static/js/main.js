import { init3D, toggle3D, renderPath, clearPaths } from './maze3d.js';

const canvas = document.getElementById('mazeCanvas');
const ctx = canvas.getContext('2d');
const statusDiv = document.getElementById('status');
const CELL_SIZE = 20;

let currentMaze = null;
let isAnimating = false;
let is3DActive = false;

// Buttons
document.getElementById('btn-generate').addEventListener('click', generateMaze);
document.getElementById('btn-solve').addEventListener('click', solveMaze);
document.getElementById('mazeCanvas').addEventListener('click', handleCanvasClick);
document.getElementById('btn-save').addEventListener('click', saveMaze);
document.getElementById('btn-load').addEventListener('click', () => document.getElementById('file-input').click());
document.getElementById('file-input').addEventListener('change', loadMaze);
document.getElementById('btn-toggle-3d').addEventListener('click', toggleView);

function toggleView() {
    is3DActive = !is3DActive;
    toggle3D(is3DActive);
    document.getElementById('btn-toggle-3d').textContent = is3DActive ? "Vista 2D" : "Vista 3D (BETA)";
    if (is3DActive && currentMaze) {
        init3D(currentMaze);
    }
}

function setStatus(msg) {
    statusDiv.textContent = msg;
}

async function generateMaze() {
    if (isAnimating) return;
    setStatus("Generando...");

    const width = document.getElementById('width').value;
    const height = document.getElementById('height').value;

    try {
        const res = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ width, height })
        });
        const data = await res.json();

        if (data.status === 'ok') {
            currentMaze = data.maze;
            drawMaze(currentMaze);
            if (is3DActive) init3D(currentMaze);
            setStatus("Laberinto generado. Click para cambiar Inicio (Verde).");
        }
    } catch (e) {
        console.error(e);
        setStatus("Error generando laberinto.");
    }
}

async function solveMaze() {
    if (!currentMaze || isAnimating) return;
    setStatus("Resolviendo...");

    const algorithm = document.getElementById('algorithm').value;
    const speed = parseInt(document.getElementById('speed').value);

    try {
        const res = await fetch('/api/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                maze: currentMaze,
                method: algorithm,
                start_x: currentMaze.start[0],
                start_y: currentMaze.start[1]
            })
        });
        const data = await res.json();

        if (data.status === 'ok') {
            await animateSolution(data.visited, data.solution, speed);
            setStatus("¡Finalizado!");
        }
    } catch (e) {
        console.error(e);
        setStatus("Error al resolver.");
    }
}

function drawMaze(maze, visited = [], solution = [], isAI = false) {
    canvas.width = maze.width * CELL_SIZE;
    canvas.height = maze.height * CELL_SIZE;

    // Draw grid
    for (let y = 0; y < maze.height; y++) {
        for (let x = 0; x < maze.width; x++) {
            const cell = maze.grid[y][x];
            ctx.fillStyle = cell === 1 ? '#333' : '#fff'; // Wall vs Path
            ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
        }
    }

    // Draw visited (cyan tint) or AI (purple tint)
    ctx.fillStyle = isAI ? 'rgba(156, 39, 176, 0.6)' : 'rgba(0, 200, 200, 0.5)';
    for (const [vx, vy] of visited) {
        ctx.fillRect(vx * CELL_SIZE, vy * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    }

    // Draw solution (yellow tint)
    ctx.fillStyle = 'rgba(255, 255, 0, 0.7)';
    for (const [sx, sy] of solution) {
        ctx.fillRect(sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    }

    // Draw Start & End
    if (maze.start) {
        ctx.fillStyle = '#0f0';
        ctx.fillRect(maze.start[0] * CELL_SIZE, maze.start[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    }
    if (maze.end) {
        ctx.fillStyle = '#f00';
        ctx.fillRect(maze.end[0] * CELL_SIZE, maze.end[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    }
}


function handleCanvasClick(e) {
    if (!currentMaze || isAnimating) return;

    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) / CELL_SIZE);
    const y = Math.floor((e.clientY - rect.top) / CELL_SIZE);

    if (x >= 0 && x < currentMaze.width && y >= 0 && y < currentMaze.height) {
        // Allow moving start point if cell is path (0)
        if (currentMaze.grid[y][x] === 0) {
            currentMaze.start = [x, y];
            drawMaze(currentMaze);
            setStatus(`Inicio movido a (${x}, ${y}).`);
        } else {
            setStatus("No puedes iniciar en una pared.");
        }
    }
}

function saveMaze() {
    if (!currentMaze) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(currentMaze));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "maze.json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}

function loadMaze(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        try {
            currentMaze = JSON.parse(e.target.result);
            drawMaze(currentMaze);
            setStatus("Laberinto cargado.");
        } catch (err) {
            console.error(err);
            setStatus("Error al cargar archivo.");
        }
    };
    reader.readAsText(file);
}

document.getElementById('btn-train').addEventListener('click', trainAgent);

async function trainAgent() {
    if (!currentMaze || isAnimating) return;
    const episodes = document.getElementById('episodes').value;
    setStatus(`Entrenando IA (${episodes} episodios)...`);

    try {
        const res = await fetch('/api/train', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ episodes: parseInt(episodes) })
        });
        const data = await res.json();

        if (data.status === 'ok') {
            setStatus("Entrenamiento completado. Visualizando última ruta...");
            const speed = parseInt(document.getElementById('speed').value);
            // Visualize with isAI=true flag
            await animateSolution(data.trace, [], speed, true);
            setStatus(`IA Entrenada por ${data.episodes_run} episodios.`);
        }
    } catch (e) {
        console.error(e);
        setStatus("Error entrenando IA.");
    }
}

async function animateSolution(visited, solution, delay, isAI = false) {
    isAnimating = true;

    // Clear previous 3D paths if any
    if (is3DActive) clearPaths();

    // Animate visited
    for (let i = 0; i < visited.length; i++) {
        drawMaze(currentMaze, visited.slice(0, i + 1), [], isAI);

        // Real-time 3D update
        if (is3DActive) {
            renderPath([visited[i]], isAI ? 'agent' : 'visited');
        }

        await new Promise(r => setTimeout(r, delay));
    }

    if (!isAI) {
        // Animate solution path 2D
        drawMaze(currentMaze, visited, solution);

        // Animate solution path 3D
        if (is3DActive) {
            for (let i = 0; i < solution.length; i++) {
                renderPath([solution[i]], 'solution');
                // Small extra delay for dramatic effect in 3D
                await new Promise(r => setTimeout(r, 20));
            }
        }
    }

    isAnimating = false;
}
