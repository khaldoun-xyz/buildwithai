# Tetris Game

A classic Tetris implementation built with Python and Pygame, featuring all the essential gameplay mechanics, progressive difficulty, and audio support.

## Features

- **Classic Gameplay**: 7 standard tetromino shapes (I, O, T, S, Z, J, L) with proper rotation
- **Special Shapes**: 10 additional challenging shapes for Expert and Insane modes
- **Progressive Difficulty**: 5 difficulty levels with varying speeds and features
- **Multiplayer Mode**: Local multiplayer support for 2-4 players with independent controls
- **High Score System**: Top 10 leaderboard for each difficulty mode
- **Scoring System**: Points for line clears and soft/hard drops with difficulty multipliers
- **Audio Support**: Optional sound effects (gracefully handles audio failures)
- **Modern UI**: Clean, responsive interface with ghost piece preview
- **Docker Support**: Easy deployment with Docker and Docker Compose

## Game Controls

### Single Player Mode
- **← →** Move piece left/right
- **↑** Rotate clockwise
- **Z** Rotate counter-clockwise
- **↓** Soft drop (faster fall)
- **Space** Hard drop (instant drop)
- **P** Pause/Resume
- **R** Restart (when game over)
- **1-5** Change difficulty mode
- **H** View high scores leaderboard
- **ESC** Quit or return to difficulty selection

### Multiplayer Mode

#### Player 1 (Arrow Keys)
- **Move Left**: ← (Left Arrow)
- **Move Right**: → (Right Arrow)  
- **Move Down**: ↓ (Down Arrow) - Soft Drop
- **Rotate Clockwise**: ↑ (Up Arrow)
- **Rotate Counter-Clockwise**: Z
- **Hard Drop**: Space
- **Pause**: P

#### Player 2 (WASD)
- **Move Left**: A
- **Move Right**: D
- **Move Down**: S - Soft Drop
- **Rotate Clockwise**: W
- **Rotate Counter-Clockwise**: Q
- **Hard Drop**: E
- **Pause**: T

#### Player 3 (IJKL)
- **Move Left**: J
- **Move Right**: L
- **Move Down**: K - Soft Drop
- **Rotate Clockwise**: I
- **Rotate Counter-Clockwise**: U
- **Hard Drop**: O
- **Pause**: P

#### Player 4 (Arrow Keys - Same as Player 1)
- **Move Left**: ← (Left Arrow)
- **Move Right**: → (Right Arrow)
- **Move Down**: ↓ (Down Arrow) - Soft Drop
- **Rotate Clockwise**: ↑ (Up Arrow)
- **Rotate Counter-Clockwise**: Z
- **Hard Drop**: Space
- **Pause**: P

#### Global Controls
- **1-5** Change difficulty mode (affects all players)
- **R** Restart game (when all players are done)
- **ESC** Return to setup menu

## Scoring System

- **Single line**: 100 points
- **Double lines**: 300 points
- **Triple lines**: 500 points
- **Tetris (4 lines)**: 800 points
- **Soft/Hard drop**: 5 points per block dropped

## Difficulty Modes

### Standard Modes (Easy, Normal, Hard)
- **7 classic tetromino shapes**: I, O, T, S, Z, J, L
- **Standard gameplay** with varying speeds and features

### Expert & Insane Modes
- **17 total shapes**: 7 classic + 10 special challenging shapes
- **Special shapes**: U, X, W, F, P, N, Y, V, C, H
- **30% chance** of special shapes appearing
- **Unique colors** for each special shape
- **More complex patterns** requiring advanced strategies

## Level Progression

- Level increases based on difficulty mode
- Falling speed increases with each level
- Speed formula varies by difficulty mode

## High Score System

### **Leaderboard Features**
- **Top 10 scores** for each difficulty mode
- **Persistent storage** - scores saved between sessions
- **Player names** up to 15 characters
- **Detailed stats** - score, level, lines cleared, date
- **Automatic detection** - game checks if score qualifies for leaderboard

### **How It Works**
1. **Achieve a high score** - Score must be in top 10 for that difficulty
2. **Enter your name** - Type your name when prompted
3. **View leaderboard** - Press H from main menu to see all scores
4. **Switch difficulties** - Use 1-5 keys to view different difficulty leaderboards

### **Score Tracking**
- **Separate leaderboards** for each difficulty mode
- **Score multipliers** applied based on difficulty
- **Date and time** recorded for each score
- **Level and lines** tracked for additional stats

## Installation

### Local Development

1. **Prerequisites**:
   - Python 3.11 or higher
   - pip package manager

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

### Docker Deployment

1. **Using Docker Compose** (recommended):
   ```bash
   docker-compose up --build
   ```

2. **Using Docker directly**:
   ```bash
   docker build -t tetris .
   docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw tetris
   ```

**Note**: For Docker deployment, you need X11 forwarding enabled for the GUI to work.

## Project Structure

```
tetris/
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── main.py                # Main game entry point
├── game/                  # Game logic package
│   ├── __init__.py
│   ├── tetris.py         # Main game controller
│   ├── multiplayer.py    # Multiplayer game management
│   ├── board.py          # Board management
│   ├── tetromino.py      # Tetromino shapes and rotation
│   ├── renderer.py       # UI rendering
│   ├── audio.py          # Audio system
│   └── highscore.py      # High score management
└── assets/               # Game assets
    ├── sounds/           # Sound effects
    └── music/            # Background music
```

## Multiplayer Mode

### Getting Started
1. **Select Mode**: Choose "2 - MULTIPLAYER" from the main menu
2. **Setup Players**: Configure 2-4 players with custom names
3. **Choose Difficulty**: Select difficulty level for all players
4. **Start Playing**: Each player uses their assigned controls

### Features
- **Local Multiplayer**: 2-4 players on the same screen
- **Independent Controls**: Each player has unique key mappings
- **Shared Piece Queue**: All players receive pieces in the same order
- **Real-time Leaderboard**: Live scoring and rankings
- **Flexible Layouts**: Different board arrangements for 2-4 players

### Player Controls
- **Player 1**: Arrow keys + Z + Space + P
- **Player 2**: WASD + Q + E + T  
- **Player 3**: IJKL + U + O + P
- **Player 4**: Arrow keys + Z + Space + P

For detailed multiplayer documentation, see [MULTIPLAYER_README.md](MULTIPLAYER_README.md).

**Quick Controls Reference**: See [CONTROLS_REFERENCE.md](CONTROLS_REFERENCE.md) for a printable control guide.

## Game Rules

1. **Objective**: Clear horizontal lines by filling them completely with tetromino pieces
2. **Game Over**: When a new piece cannot be placed at the top of the board
3. **Line Clearing**: Complete horizontal lines disappear and blocks above fall down
4. **Ghost Piece**: Semi-transparent preview shows where the piece will land
5. **Leveling**: Every 10 lines cleared increases the level and falling speed

## Technical Details

- **Language**: Python 3.11+
- **Graphics**: Pygame 2.5.2
- **Architecture**: Object-oriented design with separate modules for different concerns
- **Audio**: Optional sound effects (gracefully handles audio failures)
- **Performance**: 60 FPS target with efficient rendering

## Development

The codebase follows clean architecture principles with clear separation of concerns:

- `Tetromino`: Handles piece shapes, rotation, and movement
- `Board`: Manages the 10x20 grid, line clearing, and collision detection
- `TetrisGame`: Main game logic, scoring, and state management
- `Renderer`: All visual rendering and UI components
- `AudioManager`: Sound effects and music management

## License

This project is open source and available under the MIT License.
