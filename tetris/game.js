// Tetris Game Implementation
class TetrisGame {
    constructor(canvas, isMultiGame = false) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.isMultiGame = isMultiGame;
        
        // Game dimensions
        this.gridWidth = 10;
        this.gridHeight = 20;
        this.cellSize = isMultiGame ? 10 : 15;
        
        // Game state
        this.grid = this.createGrid();
        this.currentPiece = null;
        this.nextPieces = [];
        this.score = 0;
        this.level = 1;
        this.lines = 0;
        this.gameRunning = false;
        this.gameOver = false;
        this.paused = false;
        
        // Game timing
        this.lastTime = 0;
        this.dropTime = 0;
        this.baseSpeed = 1000; // milliseconds
        
        // Input handling
        this.keys = {};
        this.keyRepeatDelay = 150;
        this.lastKeyTime = 0;
        
        this.init();
    }
    
    init() {
        this.setupCanvas();
        this.generateNextPieces();
        this.spawnPiece();
        this.setupEventListeners();
    }
    
    setupCanvas() {
        this.canvas.width = this.gridWidth * this.cellSize;
        this.canvas.height = this.gridHeight * this.cellSize;
    }
    
    createGrid() {
        return Array(this.gridHeight).fill().map(() => Array(this.gridWidth).fill(0));
    }
    
    // Tetromino definitions
    getTetrominoes() {
        return {
            I: {
                shape: [
                    [1, 1, 1, 1]
                ],
                color: '#00f0f0'
            },
            O: {
                shape: [
                    [1, 1],
                    [1, 1]
                ],
                color: '#f0f000'
            },
            T: {
                shape: [
                    [0, 1, 0],
                    [1, 1, 1]
                ],
                color: '#a000f0'
            },
            S: {
                shape: [
                    [0, 1, 1],
                    [1, 1, 0]
                ],
                color: '#00f000'
            },
            Z: {
                shape: [
                    [1, 1, 0],
                    [0, 1, 1]
                ],
                color: '#f00000'
            },
            J: {
                shape: [
                    [1, 0, 0],
                    [1, 1, 1]
                ],
                color: '#0000f0'
            },
            L: {
                shape: [
                    [0, 0, 1],
                    [1, 1, 1]
                ],
                color: '#f0a000'
            }
        };
    }
    
    generateNextPieces() {
        const tetrominoes = Object.keys(this.getTetrominoes());
        this.nextPieces = [];
        for (let i = 0; i < 3; i++) {
            const randomType = tetrominoes[Math.floor(Math.random() * tetrominoes.length)];
            this.nextPieces.push({
                type: randomType,
                ...this.getTetrominoes()[randomType]
            });
        }
    }
    
    spawnPiece() {
        if (this.nextPieces.length === 0) {
            this.generateNextPieces();
        }
        
        const pieceData = this.nextPieces.shift();
        this.currentPiece = {
            type: pieceData.type,
            shape: pieceData.shape,
            color: pieceData.color,
            x: Math.floor(this.gridWidth / 2) - Math.floor(pieceData.shape[0].length / 2),
            y: 0,
            rotation: 0
        };
        
        // Check for game over
        if (this.checkCollision(this.currentPiece)) {
            this.gameOver = true;
            this.gameRunning = false;
        }
    }
    
    checkCollision(piece, dx = 0, dy = 0, rotation = null) {
        const shape = rotation !== null ? this.rotateShape(piece.shape, rotation) : piece.shape;
        const newX = piece.x + dx;
        const newY = piece.y + dy;
        
        for (let y = 0; y < shape.length; y++) {
            for (let x = 0; x < shape[y].length; x++) {
                if (shape[y][x]) {
                    const gridX = newX + x;
                    const gridY = newY + y;
                    
                    if (gridX < 0 || gridX >= this.gridWidth || 
                        gridY >= this.gridHeight || 
                        (gridY >= 0 && this.grid[gridY][gridX])) {
                        return true;
                    }
                }
            }
        }
        return false;
    }
    
    rotateShape(shape, rotation) {
        if (rotation === 0) return shape;
        
        let rotated = shape;
        for (let i = 0; i < rotation; i++) {
            rotated = rotated[0].map((_, index) => 
                rotated.map(row => row[index]).reverse()
            );
        }
        return rotated;
    }
    
    movePiece(dx, dy) {
        if (!this.checkCollision(this.currentPiece, dx, dy)) {
            this.currentPiece.x += dx;
            this.currentPiece.y += dy;
            return true;
        }
        return false;
    }
    
    rotatePiece() {
        const newRotation = (this.currentPiece.rotation + 1) % 4;
        if (!this.checkCollision(this.currentPiece, 0, 0, newRotation)) {
            this.currentPiece.rotation = newRotation;
            this.currentPiece.shape = this.rotateShape(this.getTetrominoes()[this.currentPiece.type].shape, newRotation);
            return true;
        }
        return false;
    }
    
    rotatePieceCounterClockwise() {
        const newRotation = (this.currentPiece.rotation + 3) % 4;
        if (!this.checkCollision(this.currentPiece, 0, 0, newRotation)) {
            this.currentPiece.rotation = newRotation;
            this.currentPiece.shape = this.rotateShape(this.getTetrominoes()[this.currentPiece.type].shape, newRotation);
            return true;
        }
        return false;
    }
    
    dropPiece() {
        if (this.movePiece(0, 1)) {
            this.score += 5; // Soft drop bonus
            return true;
        }
        return false;
    }
    
    hardDrop() {
        let dropDistance = 0;
        while (this.movePiece(0, 1)) {
            dropDistance++;
        }
        this.score += dropDistance * 5; // Hard drop bonus
        this.placePiece();
    }
    
    placePiece() {
        const shape = this.currentPiece.shape;
        for (let y = 0; y < shape.length; y++) {
            for (let x = 0; x < shape[y].length; x++) {
                if (shape[y][x]) {
                    const gridX = this.currentPiece.x + x;
                    const gridY = this.currentPiece.y + y;
                    if (gridY >= 0) {
                        this.grid[gridY][gridX] = this.currentPiece.color;
                    }
                }
            }
        }
        this.clearLines();
        this.spawnPiece();
    }
    
    clearLines() {
        let linesCleared = 0;
        for (let y = this.gridHeight - 1; y >= 0; y--) {
            if (this.grid[y].every(cell => cell !== 0)) {
                this.grid.splice(y, 1);
                this.grid.unshift(Array(this.gridWidth).fill(0));
                linesCleared++;
                y++; // Check the same row again
            }
        }
        
        if (linesCleared > 0) {
            this.lines += linesCleared;
            this.updateScore(linesCleared);
            this.updateLevel();
        }
    }
    
    updateScore(linesCleared) {
        const baseScores = { 1: 100, 2: 300, 3: 500, 4: 800 };
        this.score += baseScores[linesCleared] * this.level;
    }
    
    updateLevel() {
        const newLevel = Math.floor(this.lines / 10) + 1;
        if (newLevel > this.level) {
            this.level = newLevel;
        }
    }
    
    getDropSpeed() {
        return Math.max(50, this.baseSpeed * Math.pow(0.8, this.level - 1));
    }
    
    update(deltaTime) {
        if (!this.gameRunning || this.gameOver || this.paused) return;
        
        this.dropTime += deltaTime;
        const dropSpeed = this.getDropSpeed();
        
        if (this.dropTime >= dropSpeed) {
            if (!this.dropPiece()) {
                this.placePiece();
            }
            this.dropTime = 0;
        }
        
        this.handleInput();
    }
    
    handleInput() {
        const currentTime = Date.now();
        if (currentTime - this.lastKeyTime < this.keyRepeatDelay) return;
        
        if (this.keys['ArrowLeft'] || this.keys['a'] || this.keys['A']) {
            this.movePiece(-1, 0);
            this.lastKeyTime = currentTime;
        }
        if (this.keys['ArrowRight'] || this.keys['d'] || this.keys['D']) {
            this.movePiece(1, 0);
            this.lastKeyTime = currentTime;
        }
        if (this.keys['ArrowDown'] || this.keys['s'] || this.keys['S']) {
            this.dropPiece();
            this.lastKeyTime = currentTime;
        }
        if (this.keys['ArrowUp'] || this.keys['w'] || this.keys['W']) {
            this.rotatePiece();
            this.lastKeyTime = currentTime;
        }
        if (this.keys['z'] || this.keys['Z']) {
            this.rotatePieceCounterClockwise();
            this.lastKeyTime = currentTime;
        }
        if (this.keys[' ']) {
            this.hardDrop();
            this.lastKeyTime = currentTime;
        }
    }
    
    render() {
        // Clear canvas
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw grid
        this.drawGrid();
        
        // Draw current piece
        if (this.currentPiece && !this.gameOver) {
            this.drawPiece(this.currentPiece);
        }
        
        // Draw ghost piece
        if (this.currentPiece && !this.gameOver) {
            this.drawGhostPiece();
        }
    }
    
    renderNextPieces() {
        const nextCanvas = document.getElementById('nextCanvas');
        if (!nextCanvas) return;
        
        const nextCtx = nextCanvas.getContext('2d');
        
        // Clear canvas
        nextCtx.fillStyle = '#000';
        nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
        
        // Draw next pieces
        const cellSize = 15;
        const startY = 20;
        
        this.nextPieces.forEach((piece, index) => {
            const y = startY + index * 40;
            this.drawNextPiece(nextCtx, piece, 20, y, cellSize);
        });
    }
    
    drawNextPiece(ctx, piece, x, y, cellSize) {
        ctx.fillStyle = piece.color;
        const shape = piece.shape;
        
        for (let py = 0; py < shape.length; py++) {
            for (let px = 0; px < shape[py].length; px++) {
                if (shape[py][px]) {
                    ctx.fillRect(
                        x + px * cellSize,
                        y + py * cellSize,
                        cellSize,
                        cellSize
                    );
                    
                    // Draw border
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 1;
                    ctx.strokeRect(
                        x + px * cellSize,
                        y + py * cellSize,
                        cellSize,
                        cellSize
                    );
                }
            }
        }
    }
    
    drawGrid() {
        for (let y = 0; y < this.gridHeight; y++) {
            for (let x = 0; x < this.gridWidth; x++) {
                if (this.grid[y][x]) {
                    this.ctx.fillStyle = this.grid[y][x];
                    this.ctx.fillRect(
                        x * this.cellSize,
                        y * this.cellSize,
                        this.cellSize,
                        this.cellSize
                    );
                    
                    // Draw border
                    this.ctx.strokeStyle = '#333';
                    this.ctx.lineWidth = 1;
                    this.ctx.strokeRect(
                        x * this.cellSize,
                        y * this.cellSize,
                        this.cellSize,
                        this.cellSize
                    );
                }
            }
        }
    }
    
    drawPiece(piece) {
        this.ctx.fillStyle = piece.color;
        const shape = piece.shape;
        
        for (let y = 0; y < shape.length; y++) {
            for (let x = 0; x < shape[y].length; x++) {
                if (shape[y][x]) {
                    this.ctx.fillRect(
                        (piece.x + x) * this.cellSize,
                        (piece.y + y) * this.cellSize,
                        this.cellSize,
                        this.cellSize
                    );
                    
                    // Draw border
                    this.ctx.strokeStyle = '#fff';
                    this.ctx.lineWidth = 1;
                    this.ctx.strokeRect(
                        (piece.x + x) * this.cellSize,
                        (piece.y + y) * this.cellSize,
                        this.cellSize,
                        this.cellSize
                    );
                }
            }
        }
    }
    
    drawGhostPiece() {
        if (!this.currentPiece) return;
        
        // Find lowest position
        let ghostY = this.currentPiece.y;
        while (!this.checkCollision(this.currentPiece, 0, ghostY - this.currentPiece.y + 1)) {
            ghostY++;
        }
        
        this.ctx.fillStyle = this.currentPiece.color;
        this.ctx.globalAlpha = 0.3;
        const shape = this.currentPiece.shape;
        
        for (let y = 0; y < shape.length; y++) {
            for (let x = 0; x < shape[y].length; x++) {
                if (shape[y][x]) {
                    this.ctx.fillRect(
                        (this.currentPiece.x + x) * this.cellSize,
                        (ghostY + y) * this.cellSize,
                        this.cellSize,
                        this.cellSize
                    );
                }
            }
        }
        this.ctx.globalAlpha = 1;
    }
    
    setupEventListeners() {
        document.addEventListener('keydown', (e) => {
            this.keys[e.key] = true;
            e.preventDefault();
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.key] = false;
        });
    }
    
    start() {
        this.gameRunning = true;
        this.gameOver = false;
        this.paused = false;
        this.lastTime = performance.now();
        
        // Render next pieces initially
        if (!this.isMultiGame) {
            this.renderNextPieces();
        }
        
        this.gameLoop();
    }
    
    pause() {
        this.paused = !this.paused;
    }
    
    reset() {
        this.grid = this.createGrid();
        this.currentPiece = null;
        this.nextPieces = [];
        this.score = 0;
        this.level = 1;
        this.lines = 0;
        this.gameRunning = false;
        this.gameOver = false;
        this.paused = false;
        this.dropTime = 0;
        this.generateNextPieces();
        this.spawnPiece();
        
        // Render next pieces after reset
        if (!this.isMultiGame) {
            this.renderNextPieces();
        }
    }
    
    gameLoop() {
        if (!this.gameRunning) return;
        
        const currentTime = performance.now();
        const deltaTime = currentTime - this.lastTime;
        this.lastTime = currentTime;
        
        this.update(deltaTime);
        this.render();
        
        // Render next pieces for single game mode
        if (!this.isMultiGame) {
            this.renderNextPieces();
        }
        
        requestAnimationFrame(() => this.gameLoop());
    }
}

// 3D Tetris Game Implementation
class Tetris3D {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        
        // 3D Game dimensions
        this.gridWidth = 10;
        this.gridHeight = 10;
        this.gridDepth = 30;
        this.cellSize = 12;
        
        // 3D Grid (3D array)
        this.grid = this.create3DGrid();
        this.currentPiece = null;
        this.nextPieces = [];
        this.score = 0;
        this.level = 1;
        this.lines = 0;
        this.gameRunning = false;
        this.gameOver = false;
        this.paused = false;
        
        // 3D Camera rotation
        this.cameraRotationX = 0;
        this.cameraRotationY = 0;
        this.cameraRotationZ = 0;
        
        // Game timing
        this.lastTime = 0;
        this.dropTime = 0;
        this.baseSpeed = 1000;
        
        // Input handling
        this.keys = {};
        this.keyRepeatDelay = 150;
        this.lastKeyTime = 0;
        
        this.init();
    }
    
    init() {
        this.setupCanvas();
        this.generateNextPieces();
        this.spawnPiece();
        this.setupEventListeners();
    }
    
    setupCanvas() {
        this.canvas.width = 400;
        this.canvas.height = 600;
    }
    
    create3DGrid() {
        return Array(this.gridDepth).fill().map(() => 
            Array(this.gridHeight).fill().map(() => 
                Array(this.gridWidth).fill(0)
            )
        );
    }
    
    // 3D Tetromino definitions
    get3DTetrominoes() {
        return {
            I: {
                shape: [
                    [[1, 1, 1, 1]],
                    [[0, 0, 0, 0]],
                    [[0, 0, 0, 0]],
                    [[0, 0, 0, 0]]
                ],
                color: '#00f0f0'
            },
            O: {
                shape: [
                    [[1, 1], [1, 1]],
                    [[0, 0], [0, 0]]
                ],
                color: '#f0f000'
            },
            T: {
                shape: [
                    [[0, 1, 0], [1, 1, 1]],
                    [[0, 0, 0], [0, 0, 0]]
                ],
                color: '#a000f0'
            },
            S: {
                shape: [
                    [[0, 1, 1], [1, 1, 0]],
                    [[0, 0, 0], [0, 0, 0]]
                ],
                color: '#00f000'
            },
            Z: {
                shape: [
                    [[1, 1, 0], [0, 1, 1]],
                    [[0, 0, 0], [0, 0, 0]]
                ],
                color: '#f00000'
            },
            J: {
                shape: [
                    [[1, 0, 0], [1, 1, 1]],
                    [[0, 0, 0], [0, 0, 0]]
                ],
                color: '#0000f0'
            },
            L: {
                shape: [
                    [[0, 0, 1], [1, 1, 1]],
                    [[0, 0, 0], [0, 0, 0]]
                ],
                color: '#f0a000'
            }
        };
    }
    
    generateNextPieces() {
        const tetrominoes = Object.keys(this.get3DTetrominoes());
        this.nextPieces = [];
        for (let i = 0; i < 3; i++) {
            const randomType = tetrominoes[Math.floor(Math.random() * tetrominoes.length)];
            this.nextPieces.push({
                type: randomType,
                ...this.get3DTetrominoes()[randomType]
            });
        }
    }
    
    spawnPiece() {
        if (this.nextPieces.length === 0) {
            this.generateNextPieces();
        }
        
        const pieceData = this.nextPieces.shift();
        this.currentPiece = {
            type: pieceData.type,
            shape: pieceData.shape,
            color: pieceData.color,
            x: Math.floor(this.gridWidth / 2) - Math.floor(pieceData.shape[0][0].length / 2),
            y: Math.floor(this.gridHeight / 2) - Math.floor(pieceData.shape[0].length / 2),
            z: 0,
            rotation: 0
        };
        
        // Check for game over
        if (this.check3DCollision(this.currentPiece)) {
            this.gameOver = true;
            this.gameRunning = false;
        }
    }
    
    check3DCollision(piece, dx = 0, dy = 0, dz = 0) {
        const shape = piece.shape;
        const newX = piece.x + dx;
        const newY = piece.y + dy;
        const newZ = piece.z + dz;
        
        for (let z = 0; z < shape.length; z++) {
            for (let y = 0; y < shape[z].length; y++) {
                for (let x = 0; x < shape[z][y].length; x++) {
                    if (shape[z][y][x]) {
                        const gridX = newX + x;
                        const gridY = newY + y;
                        const gridZ = newZ + z;
                        
                        if (gridX < 0 || gridX >= this.gridWidth || 
                            gridY < 0 || gridY >= this.gridHeight ||
                            gridZ < 0 || gridZ >= this.gridDepth ||
                            this.grid[gridZ][gridY][gridX]) {
                            return true;
                        }
                    }
                }
            }
        }
        return false;
    }
    
    movePiece(dx, dy, dz = 0) {
        if (!this.check3DCollision(this.currentPiece, dx, dy, dz)) {
            this.currentPiece.x += dx;
            this.currentPiece.y += dy;
            this.currentPiece.z += dz;
            return true;
        }
        return false;
    }
    
    dropPiece() {
        if (this.movePiece(0, 0, 1)) {
            this.score += 5;
            return true;
        }
        return false;
    }
    
    placePiece() {
        const shape = this.currentPiece.shape;
        for (let z = 0; z < shape.length; z++) {
            for (let y = 0; y < shape[z].length; y++) {
                for (let x = 0; x < shape[z][y].length; x++) {
                    if (shape[z][y][x]) {
                        const gridX = this.currentPiece.x + x;
                        const gridY = this.currentPiece.y + y;
                        const gridZ = this.currentPiece.z + z;
                        if (gridZ >= 0 && gridZ < this.gridDepth) {
                            this.grid[gridZ][gridY][gridX] = this.currentPiece.color;
                        }
                    }
                }
            }
        }
        this.clear3DLayers();
        this.spawnPiece();
    }
    
    clear3DLayers() {
        let layersCleared = 0;
        for (let z = this.gridDepth - 1; z >= 0; z--) {
            let isFullLayer = true;
            for (let y = 0; y < this.gridHeight; y++) {
                for (let x = 0; x < this.gridWidth; x++) {
                    if (!this.grid[z][y][x]) {
                        isFullLayer = false;
                        break;
                    }
                }
                if (!isFullLayer) break;
            }
            
            if (isFullLayer) {
                this.grid.splice(z, 1);
                this.grid.unshift(Array(this.gridHeight).fill().map(() => Array(this.gridWidth).fill(0)));
                layersCleared++;
                z++; // Check the same layer again
            }
        }
        
        if (layersCleared > 0) {
            this.lines += layersCleared;
            this.updateScore(layersCleared);
            this.updateLevel();
        }
    }
    
    updateScore(layersCleared) {
        const baseScores = { 1: 100, 2: 300, 3: 500, 4: 800 };
        this.score += baseScores[layersCleared] * this.level;
    }
    
    updateLevel() {
        const newLevel = Math.floor(this.lines / 10) + 1;
        if (newLevel > this.level) {
            this.level = newLevel;
        }
    }
    
    getDropSpeed() {
        return Math.max(50, this.baseSpeed * Math.pow(0.8, this.level - 1));
    }
    
    update(deltaTime) {
        if (!this.gameRunning || this.gameOver || this.paused) return;
        
        this.dropTime += deltaTime;
        const dropSpeed = this.getDropSpeed();
        
        if (this.dropTime >= dropSpeed) {
            if (!this.dropPiece()) {
                this.placePiece();
            }
            this.dropTime = 0;
        }
        
        this.handleInput();
    }
    
    handleInput() {
        const currentTime = Date.now();
        if (currentTime - this.lastKeyTime < this.keyRepeatDelay) return;
        
        // 3D Camera rotation with WASD
        if (this.keys['w'] || this.keys['W']) {
            this.cameraRotationX += 0.1;
            this.lastKeyTime = currentTime;
        }
        if (this.keys['s'] || this.keys['S']) {
            this.cameraRotationX -= 0.1;
            this.lastKeyTime = currentTime;
        }
        if (this.keys['a'] || this.keys['A']) {
            this.cameraRotationY += 0.1;
            this.lastKeyTime = currentTime;
        }
        if (this.keys['d'] || this.keys['D']) {
            this.cameraRotationY -= 0.1;
            this.lastKeyTime = currentTime;
        }
        
        // Piece movement with arrow keys
        if (this.keys['ArrowLeft'] || this.keys['ArrowRight']) {
            this.movePiece(this.keys['ArrowLeft'] ? -1 : 1, 0);
            this.lastKeyTime = currentTime;
        }
        if (this.keys['ArrowUp'] || this.keys['ArrowDown']) {
            this.movePiece(0, this.keys['ArrowUp'] ? -1 : 1);
            this.lastKeyTime = currentTime;
        }
        if (this.keys[' ']) {
            this.hardDrop();
            this.lastKeyTime = currentTime;
        }
    }
    
    hardDrop() {
        let dropDistance = 0;
        while (this.movePiece(0, 0, 1)) {
            dropDistance++;
        }
        this.score += dropDistance * 5;
        this.placePiece();
    }
    
    // 3D Projection and Rendering
    project3D(x, y, z) {
        // Simple 3D to 2D projection
        const scale = 200;
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        
        // Apply camera rotation
        const cosX = Math.cos(this.cameraRotationX);
        const sinX = Math.sin(this.cameraRotationX);
        const cosY = Math.cos(this.cameraRotationY);
        const sinY = Math.sin(this.cameraRotationY);
        
        // Rotate around Y axis
        let x1 = x * cosY - z * sinY;
        let y1 = y;
        let z1 = x * sinY + z * cosY;
        
        // Rotate around X axis
        let x2 = x1;
        let y2 = y1 * cosX - z1 * sinX;
        let z2 = y1 * sinX + z1 * cosX;
        
        // Project to 2D
        const projectedX = centerX + (x2 * scale) / (z2 + 20);
        const projectedY = centerY + (y2 * scale) / (z2 + 20);
        
        return { x: projectedX, y: projectedY, z: z2 };
    }
    
    render() {
        // Clear canvas
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw 3D grid
        this.draw3DGrid();
        
        // Draw current piece
        if (this.currentPiece && !this.gameOver) {
            this.draw3DPiece(this.currentPiece);
        }
    }
    
    draw3DGrid() {
        const cells = [];
        
        // Collect all filled cells
        for (let z = 0; z < this.gridDepth; z++) {
            for (let y = 0; y < this.gridHeight; y++) {
                for (let x = 0; x < this.gridWidth; x++) {
                    if (this.grid[z][y][x]) {
                        const projected = this.project3D(x, y, z);
                        cells.push({
                            x: projected.x,
                            y: projected.y,
                            z: projected.z,
                            color: this.grid[z][y][x]
                        });
                    }
                }
            }
        }
        
        // Sort by depth (back to front)
        cells.sort((a, b) => b.z - a.z);
        
        // Draw cells
        cells.forEach(cell => {
            this.ctx.fillStyle = cell.color;
            this.ctx.fillRect(
                cell.x - this.cellSize / 2,
                cell.y - this.cellSize / 2,
                this.cellSize,
                this.cellSize
            );
            
            // Draw border
            this.ctx.strokeStyle = '#fff';
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(
                cell.x - this.cellSize / 2,
                cell.y - this.cellSize / 2,
                this.cellSize,
                this.cellSize
            );
        });
    }
    
    draw3DPiece(piece) {
        const cells = [];
        
        for (let z = 0; z < piece.shape.length; z++) {
            for (let y = 0; y < piece.shape[z].length; y++) {
                for (let x = 0; x < piece.shape[z][y].length; x++) {
                    if (piece.shape[z][y][x]) {
                        const projected = this.project3D(
                            piece.x + x,
                            piece.y + y,
                            piece.z + z
                        );
                        cells.push({
                            x: projected.x,
                            y: projected.y,
                            z: projected.z,
                            color: piece.color
                        });
                    }
                }
            }
        }
        
        // Sort by depth
        cells.sort((a, b) => b.z - a.z);
        
        // Draw cells
        cells.forEach(cell => {
            this.ctx.fillStyle = cell.color;
            this.ctx.fillRect(
                cell.x - this.cellSize / 2,
                cell.y - this.cellSize / 2,
                this.cellSize,
                this.cellSize
            );
            
            this.ctx.strokeStyle = '#fff';
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(
                cell.x - this.cellSize / 2,
                cell.y - this.cellSize / 2,
                this.cellSize,
                this.cellSize
            );
        });
    }
    
    renderNextPieces() {
        const nextCanvas = document.getElementById('nextCanvas3d');
        if (!nextCanvas) return;
        
        const nextCtx = nextCanvas.getContext('2d');
        nextCtx.fillStyle = '#000';
        nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
        
        const cellSize = 15;
        const startY = 20;
        
        this.nextPieces.forEach((piece, index) => {
            const y = startY + index * 40;
            this.drawNextPiece(nextCtx, piece, 20, y, cellSize);
        });
    }
    
    drawNextPiece(ctx, piece, x, y, cellSize) {
        ctx.fillStyle = piece.color;
        const shape = piece.shape[0]; // Use first layer for 2D preview
        
        for (let py = 0; py < shape.length; py++) {
            for (let px = 0; px < shape[py].length; px++) {
                if (shape[py][px]) {
                    ctx.fillRect(
                        x + px * cellSize,
                        y + py * cellSize,
                        cellSize,
                        cellSize
                    );
                    
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 1;
                    ctx.strokeRect(
                        x + px * cellSize,
                        y + py * cellSize,
                        cellSize,
                        cellSize
                    );
                }
            }
        }
    }
    
    setupEventListeners() {
        document.addEventListener('keydown', (e) => {
            this.keys[e.key] = true;
            e.preventDefault();
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.key] = false;
        });
    }
    
    start() {
        this.gameRunning = true;
        this.gameOver = false;
        this.paused = false;
        this.lastTime = performance.now();
        
        this.renderNextPieces();
        this.gameLoop();
    }
    
    pause() {
        this.paused = !this.paused;
    }
    
    reset() {
        this.grid = this.create3DGrid();
        this.currentPiece = null;
        this.nextPieces = [];
        this.score = 0;
        this.level = 1;
        this.lines = 0;
        this.gameRunning = false;
        this.gameOver = false;
        this.paused = false;
        this.dropTime = 0;
        this.cameraRotationX = 0;
        this.cameraRotationY = 0;
        this.cameraRotationZ = 0;
        this.generateNextPieces();
        this.spawnPiece();
        
        this.renderNextPieces();
    }
    
    gameLoop() {
        if (!this.gameRunning) return;
        
        const currentTime = performance.now();
        const deltaTime = currentTime - this.lastTime;
        this.lastTime = currentTime;
        
        this.update(deltaTime);
        this.render();
        
        this.renderNextPieces();
        
        requestAnimationFrame(() => this.gameLoop());
    }
}

// Multi-Game Manager for 4-part parallel mode
class MultiGameManager {
    constructor() {
        this.games = [];
        this.gameMode = 'single'; // 'single', 'multi', or '3d'
        this.totalScore = 0;
        this.activeGames = 4;
        this.isRotating = false;
        this.setupGames();
    }
    
    setupGames() {
        // Single game setup
        const singleCanvas = document.getElementById('gameCanvas');
        if (singleCanvas) {
            this.singleGame = new TetrisGame(singleCanvas, false);
        }
        
        // 3D game setup
        const game3DCanvas = document.getElementById('gameCanvas3d');
        if (game3DCanvas) {
            this.game3D = new Tetris3D(game3DCanvas);
        }
        
        // Multi-game setup
        for (let i = 1; i <= 4; i++) {
            const canvas = document.getElementById(`gameCanvas${i}`);
            if (canvas) {
                const game = new TetrisGame(canvas, true);
                
                // All games have the same dimensions: 10x20 grid
                game.gridWidth = 10;
                game.gridHeight = 20;
                game.cellSize = 15; // 150px canvas width / 10 cells = 15px per cell
                
                game.grid = game.createGrid(); // Recreate grid with new dimensions
                game.setupCanvas();
                this.games.push(game);
            }
        }
    }
    
    startGame() {
        if (this.gameMode === 'single') {
            this.singleGame.start();
        } else if (this.gameMode === '3d') {
            this.game3D.start();
        } else {
            this.games.forEach(game => {
                game.reset();
                game.start();
            });
            this.activeGames = 4;
        }
        // Enable pause button when game starts
        document.getElementById('pauseBtn').disabled = false;
    }
    
    pauseGame() {
        if (this.gameMode === 'single') {
            this.singleGame.pause();
        } else if (this.gameMode === '3d') {
            this.game3D.pause();
        } else {
            this.games.forEach(game => game.pause());
        }
    }
    
    resetGame() {
        if (this.gameMode === 'single') {
            this.singleGame.reset();
        } else if (this.gameMode === '3d') {
            this.game3D.reset();
        } else {
            this.games.forEach(game => game.reset());
            this.activeGames = 4;
        }
        // Disable pause button when game is reset
        document.getElementById('pauseBtn').disabled = true;
        // Stop rotation when game is reset
        if (this.isRotating) {
            this.toggleRotation();
        }
    }
    
    switchMode() {
        this.gameMode = this.gameMode === 'single' ? 'multi' : 'single';
        
        const singleGame = document.getElementById('singleGame');
        const multiGame = document.getElementById('multiGame');
        const game3D = document.getElementById('game3D');
        const modeBtn = document.getElementById('modeBtn');
        
        if (this.gameMode === 'multi') {
            singleGame.style.display = 'none';
            multiGame.style.display = 'block';
            game3D.style.display = 'none';
            modeBtn.textContent = 'Switch to Single Mode';
        } else {
            singleGame.style.display = 'flex';
            multiGame.style.display = 'none';
            game3D.style.display = 'none';
            modeBtn.textContent = 'Switch to 4-Part Mode';
        }
        
        this.resetGame();
    }
    
    switchTo3DMode() {
        this.gameMode = '3d';
        
        const singleGame = document.getElementById('singleGame');
        const multiGame = document.getElementById('multiGame');
        const game3D = document.getElementById('game3D');
        const modeBtn = document.getElementById('modeBtn');
        const mode3DBtn = document.getElementById('mode3DBtn');
        
        singleGame.style.display = 'none';
        multiGame.style.display = 'none';
        game3D.style.display = 'flex';
        modeBtn.textContent = 'Switch to Single Mode';
        mode3DBtn.textContent = 'Switch to 2D Mode';
        
        this.resetGame();
    }
    
    updateUI() {
        if (this.gameMode === 'single') {
            document.getElementById('score').textContent = this.singleGame.score;
            document.getElementById('level').textContent = this.singleGame.level;
            document.getElementById('lines').textContent = this.singleGame.lines;
        } else if (this.gameMode === '3d') {
            document.getElementById('score3d').textContent = this.game3D.score;
            document.getElementById('level3d').textContent = this.game3D.level;
            document.getElementById('lines3d').textContent = this.game3D.lines;
        } else {
            this.totalScore = this.games.reduce((sum, game) => sum + game.score, 0);
            this.activeGames = this.games.filter(game => !game.gameOver).length;
            
            document.getElementById('totalScore').textContent = this.totalScore;
            document.getElementById('activeGames').textContent = this.activeGames;
            
            this.games.forEach((game, index) => {
                document.getElementById(`score${index + 1}`).textContent = game.score;
                document.getElementById(`level${index + 1}`).textContent = game.level;
            });
        }
    }
    
    checkGameOver() {
        if (this.gameMode === 'single') {
            if (this.singleGame.gameOver) {
                this.showGameOver(this.singleGame.score);
            }
        } else if (this.gameMode === '3d') {
            if (this.game3D.gameOver) {
                this.showGameOver(this.game3D.score);
            }
        } else {
            if (this.activeGames === 0) {
                this.showGameOver(this.totalScore);
            }
        }
    }
    
    showGameOver(finalScore) {
        document.getElementById('finalScore').textContent = finalScore;
        document.getElementById('gameOver').style.display = 'flex';
        // Disable pause button when game is over
        document.getElementById('pauseBtn').disabled = true;
    }
    
    hideGameOver() {
        document.getElementById('gameOver').style.display = 'none';
    }
    
    toggleRotation() {
        if (this.gameMode !== 'multi') return;
        
        this.isRotating = !this.isRotating;
        const gameGrid = document.querySelector('.game-grid');
        const rotationBtn = document.getElementById('rotationBtn');
        
        if (this.isRotating) {
            gameGrid.classList.add('rotating');
            rotationBtn.textContent = 'Stop Rotation';
            rotationBtn.style.background = '#4CAF50';
        } else {
            gameGrid.classList.remove('rotating');
            rotationBtn.textContent = 'Start Rotation';
            rotationBtn.style.background = '#ff6b6b';
        }
    }
}

// Initialize the game
document.addEventListener('DOMContentLoaded', () => {
    const gameManager = new MultiGameManager();
    
    // Event listeners
    document.getElementById('startBtn').addEventListener('click', () => {
        gameManager.startGame();
        gameManager.hideGameOver();
    });
    
    document.getElementById('pauseBtn').addEventListener('click', () => {
        gameManager.pauseGame();
    });
    
    document.getElementById('modeBtn').addEventListener('click', () => {
        gameManager.switchMode();
    });
    
    document.getElementById('mode3DBtn').addEventListener('click', () => {
        gameManager.switchTo3DMode();
    });
    
    document.getElementById('restartBtn').addEventListener('click', () => {
        gameManager.resetGame();
        gameManager.hideGameOver();
    });
    
    document.getElementById('rotationBtn').addEventListener('click', () => {
        gameManager.toggleRotation();
    });
    
    // Game loop for UI updates
    setInterval(() => {
        gameManager.updateUI();
        gameManager.checkGameOver();
    }, 100);
    
    // Pause with P key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'p' || e.key === 'P') {
            gameManager.pauseGame();
        }
    });
});
