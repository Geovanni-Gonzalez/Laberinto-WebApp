import * as THREE from 'https://unpkg.com/three@0.126.0/build/three.module.js';

let scene, camera, renderer;
let mazeGeometry;
let is3DMode = false;
let controls;

// Basic FPS controls vars
let moveForward = false;
let moveBackward = false;
let moveLeft = false;
let moveRight = false;
let prevTime = performance.now();
const velocity = new THREE.Vector3();
const direction = new THREE.Vector3();

// Export function to initialize 3D view
export function init3D(mazeData) {
    if (scene) {
        // Clear previous maze
        while (scene.children.length > 0) {
            scene.remove(scene.children[0]);
        }
    } else {
        // Init scene
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1a1a1a);

        const canvasContainer = document.querySelector('.canvas-wrapper');
        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(canvasContainer.clientWidth, canvasContainer.clientHeight);
        renderer.domElement.id = 'canvas3d';
        renderer.domElement.style.display = 'none'; // Hidden by default
        canvasContainer.appendChild(renderer.domElement);

        camera = new THREE.PerspectiveCamera(75, canvasContainer.clientWidth / canvasContainer.clientHeight, 0.1, 1000);

        // Listeners for Controls
        document.addEventListener('keydown', onKeyDown);
        document.addEventListener('keyup', onKeyUp);

        // Simple pointer lock click
        renderer.domElement.addEventListener('click', () => {
            document.body.requestPointerLock();
        });

        animate();
    }

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(10, 20, 10);
    scene.add(dirLight);

    // Build Maze
    const wallMaterial = new THREE.MeshStandardMaterial({ color: 0x4caf50 }); // Green walls
    const floorMaterial = new THREE.MeshStandardMaterial({ color: 0x333333 });

    // Floor
    const floorGeo = new THREE.PlaneGeometry(mazeData.width, mazeData.height);
    const floor = new THREE.Mesh(floorGeo, floorMaterial);
    floor.rotation.x = -Math.PI / 2;
    floor.position.set(mazeData.width / 2, 0, mazeData.height / 2);
    scene.add(floor);

    // Ceiling (Optional, maybe sky?)

    // Walls
    const wallGeo = new THREE.BoxGeometry(1, 2, 1);
    const geometry = new THREE.InstancedMesh(wallGeo, wallMaterial, countWalls(mazeData));

    let idx = 0;
    const dummy = new THREE.Object3D();

    for (let y = 0; y < mazeData.height; y++) {
        for (let x = 0; x < mazeData.width; x++) {
            if (mazeData.grid[y][x] === 1) {
                dummy.position.set(x + 0.5, 1, y + 0.5);
                dummy.updateMatrix();
                geometry.setMatrixAt(idx++, dummy.matrix);
            }
        }
    }
    scene.add(geometry);

    // Start Position
    camera.position.set(mazeData.start[0] + 0.5, 1, mazeData.start[1] + 0.5);
    camera.rotation.set(0, 0, 0); // Look forward
}

function countWalls(mazeData) {
    let c = 0;
    for (let row of mazeData.grid) {
        for (let cell of row) {
            if (cell === 1) c++;
        }
    }
    return c;
}

export function toggle3D(enable) {
    is3DMode = enable;
    const c2d = document.getElementById('mazeCanvas');
    const c3d = document.getElementById('canvas3d');

    if (enable) {
        c2d.style.display = 'none';
        if (c3d) c3d.style.display = 'block';
    } else {
        c2d.style.display = 'block';
        if (c3d) c3d.style.display = 'none';
        document.exitPointerLock();
    }
}

function onKeyDown(event) {
    switch (event.code) {
        case 'ArrowUp':
        case 'KeyW': moveForward = true; break;
        case 'ArrowLeft':
        case 'KeyA': moveLeft = true; break;
        case 'ArrowDown':
        case 'KeyS': moveBackward = true; break;
        case 'ArrowRight':
        case 'KeyD': moveRight = true; break;
    }
}

function onKeyUp(event) {
    switch (event.code) {
        case 'ArrowUp':
        case 'KeyW': moveForward = false; break;
        case 'ArrowLeft':
        case 'KeyA': moveLeft = false; break;
        case 'ArrowDown':
        case 'KeyS': moveBackward = false; break;
        case 'ArrowRight':
        case 'KeyD': moveRight = false; break;
    }
}

function animate() {
    requestAnimationFrame(animate);

    if (is3DMode) {
        // Controls Logic
        const time = performance.now();
        const delta = (time - prevTime) / 1000;

        velocity.x -= velocity.x * 10.0 * delta;
        velocity.z -= velocity.z * 10.0 * delta;

        direction.z = Number(moveForward) - Number(moveBackward);
        direction.x = Number(moveRight) - Number(moveLeft);
        direction.normalize(); // Ensure consistent speed

        if (moveForward || moveBackward) velocity.z -= direction.z * 40.0 * delta;
        if (moveLeft || moveRight) velocity.x -= direction.x * 40.0 * delta;

        // Simple movement (no collision detection for MVP)
        // To implement collision, we'd need to check position against mazeData map

        camera.translateX(-velocity.x * delta);
        camera.translateZ(-velocity.z * delta);

        prevTime = time;
        renderer.render(scene, camera);

        // Mouse look?
        // Basic Pointer Lock handling for mouse look requires 'controls' object or manual Euler calc.
        // For brevity, using simple PointerLockControls logic replication or simple manual:
        // Actually, without PointerLockControls imported, we need manual handling.
        // Let's rely on basic keyboard movement for now or add a listener for mousemove if locked.
    }
}

// Global mouse listener for rotation
document.addEventListener('mousemove', (event) => {
    if (document.pointerLockElement === document.body) {
        const movementX = event.movementX || 0;
        const movementY = event.movementY || 0;

        camera.rotation.y -= movementX * 0.002;
        camera.rotation.x -= movementY * 0.002;
        // Clamp Up/Down
        camera.rotation.x = Math.max(- Math.PI / 2, Math.min(Math.PI / 2, camera.rotation.x));
    }
});
