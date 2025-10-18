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
    }
    
    gameLoop() {
        if (!this.gameRunning) return;
        
        const currentTime = performance.now();
        const deltaTime = currentTime - this.lastTime;
        this.lastTime = currentTime;
        
        this.update(deltaTime);
        this.render();
        
        requestAnimationFrame(() => this.gameLoop());
    }
}

// Multi-Game Manager for 4-part parallel mode
class MultiGameManager {
    constructor() {
        this.games = [];
        this.gameMode = 'single'; // 'single' or 'multi'
        this.totalScore = 0;
        this.activeGames = 4;
        this.setupGames();
    }
    
    setupGames() {
        // Single game setup
        const singleCanvas = document.getElementById('gameCanvas');
        if (singleCanvas) {
            this.singleGame = new TetrisGame(singleCanvas, false);
        }
        
        // Multi-game setup
        for (let i = 1; i <= 4; i++) {
            const canvas = document.getElementById(`gameCanvas${i}`);
            if (canvas) {
                const game = new TetrisGame(canvas, true);
                this.games.push(game);
            }
        }
    }
    
    startGame() {
        if (this.gameMode === 'single') {
            this.singleGame.start();
        } else {
            this.games.forEach(game => {
                game.reset();
                game.start();
            });
            this.activeGames = 4;
        }
    }
    
    pauseGame() {
        if (this.gameMode === 'single') {
            this.singleGame.pause();
        } else {
            this.games.forEach(game => game.pause());
        }
    }
    
    resetGame() {
        if (this.gameMode === 'single') {
            this.singleGame.reset();
        } else {
            this.games.forEach(game => game.reset());
            this.activeGames = 4;
        }
    }
    
    switchMode() {
        this.gameMode = this.gameMode === 'single' ? 'multi' : 'single';
        
        const singleGame = document.getElementById('singleGame');
        const multiGame = document.getElementById('multiGame');
        const modeBtn = document.getElementById('modeBtn');
        
        if (this.gameMode === 'multi') {
            singleGame.style.display = 'none';
            multiGame.style.display = 'block';
            modeBtn.textContent = 'Switch to Single Mode';
        } else {
            singleGame.style.display = 'flex';
            multiGame.style.display = 'none';
            modeBtn.textContent = 'Switch to 4-Part Mode';
        }
        
        this.resetGame();
    }
    
    updateUI() {
        if (this.gameMode === 'single') {
            document.getElementById('score').textContent = this.singleGame.score;
            document.getElementById('level').textContent = this.singleGame.level;
            document.getElementById('lines').textContent = this.singleGame.lines;
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
        } else {
            if (this.activeGames === 0) {
                this.showGameOver(this.totalScore);
            }
        }
    }
    
    showGameOver(finalScore) {
        document.getElementById('finalScore').textContent = finalScore;
        document.getElementById('gameOver').style.display = 'flex';
    }
    
    hideGameOver() {
        document.getElementById('gameOver').style.display = 'none';
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
    
    document.getElementById('restartBtn').addEventListener('click', () => {
        gameManager.resetGame();
        gameManager.hideGameOver();
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
