# Tetris Multiplayer Mode

This document describes the multiplayer functionality added to the Tetris game.

## Features

### Local Multiplayer Support
- **2-4 Players**: Support for 2, 3, or 4 players playing simultaneously
- **Shared Screen**: All players play on the same screen with side-by-side boards
- **Independent Controls**: Each player has their own control scheme
- **Synchronized Gameplay**: All players use the same piece sequence for fair play

### Game Modes

#### Single Player Mode
- Classic Tetris experience
- All original features preserved
- High score tracking

#### Multiplayer Mode
- **Player Setup**: Configure number of players (2-4) and player names
- **Difficulty Selection**: Choose difficulty for all players
- **Simultaneous Play**: All players play at the same time
- **Leaderboard**: Real-time scoring and final rankings

## Controls

### Player 1 (Arrow Keys)
- **Move Left**: ← (Left Arrow)
- **Move Right**: → (Right Arrow)
- **Move Down**: ↓ (Down Arrow) - Soft Drop
- **Rotate Clockwise**: ↑ (Up Arrow)
- **Rotate Counter-Clockwise**: Z
- **Hard Drop**: Space (instantly drops to bottom)
- **Pause**: P

### Player 2 (WASD)
- **Move Left**: A
- **Move Right**: D
- **Move Down**: S - Soft Drop
- **Rotate Clockwise**: W
- **Rotate Counter-Clockwise**: Q
- **Hard Drop**: E (instantly drops to bottom)
- **Pause**: T

### Player 3 (IJKL)
- **Move Left**: J
- **Move Right**: L
- **Move Down**: K - Soft Drop
- **Rotate Clockwise**: I
- **Rotate Counter-Clockwise**: U
- **Hard Drop**: O (instantly drops to bottom)
- **Pause**: P

### Player 4 (Arrow Keys - Same as Player 1)
- **Move Left**: ← (Left Arrow)
- **Move Right**: → (Right Arrow)
- **Move Down**: ↓ (Down Arrow) - Soft Drop
- **Rotate Clockwise**: ↑ (Up Arrow)
- **Rotate Counter-Clockwise**: Z
- **Hard Drop**: Space (instantly drops to bottom)
- **Pause**: P

### Control Tips
- **Soft Drop**: Hold down the move down key for faster falling
- **Hard Drop**: Press once to instantly drop the piece to the bottom
- **Rotation**: Use both rotation keys to find the best position
- **Pause**: Any player can pause the game for all players

**📋 Quick Reference**: See [CONTROLS_REFERENCE.md](CONTROLS_REFERENCE.md) for a printable control guide.

## How to Play Multiplayer

1. **Start the Game**: Run `python main.py`
2. **Select Mode**: Choose "2 - MULTIPLAYER" from the main menu
3. **Setup Players**:
   - Press 1-3 to select number of players (2-4)
   - Use ↑↓ to navigate between player names
   - Type to edit player names
   - Press TAB to switch to difficulty selection
   - Press 1-5 to select difficulty
4. **Start Game**: Press ENTER to begin
5. **Play**: Each player uses their assigned controls
6. **Game Over**: When all players are done, see the final leaderboard

## Technical Implementation

### Architecture
- **MultiplayerGame Class**: Manages multiple TetrisGame instances
- **Shared Piece Queue**: Ensures all players get the same piece sequence
- **Independent Game States**: Each player has their own board, score, and level
- **Synchronized Updates**: All games update simultaneously

### Key Components

#### MultiplayerGame
- Manages 2-4 player games
- Handles input routing to correct players
- Maintains shared piece queue
- Tracks game state and winner

#### Enhanced Renderer
- **Multiplayer Layouts**: Different board arrangements for 2-4 players
- **Player Information**: Shows names, scores, and game status
- **Game Over Screen**: Displays final leaderboard

#### Control System
- **Player-Specific Controls**: Each player has unique key mappings
- **Input Routing**: Routes keyboard input to correct player
- **Simultaneous Input**: Handles multiple players pressing keys at once

## Board Layouts

### 2 Players
- Side-by-side boards
- Full-size boards for optimal gameplay

### 3 Players
- 2x2 grid with one empty space
- Player 3 positioned below the first row

### 4 Players
- 2x2 grid
- All players in equal-sized boards

## Game Rules

### Shared Elements
- **Piece Sequence**: All players receive pieces in the same order
- **Difficulty**: All players play at the same difficulty level
- **Scoring**: Standard Tetris scoring applies to all players

### Individual Elements
- **Boards**: Each player has their own 10x20 board
- **Scores**: Independent scoring for each player
- **Game Over**: Players can be eliminated individually
- **Controls**: Each player has their own control scheme

## Winning Conditions

- **Last Player Standing**: Game continues until only one player remains
- **Highest Score**: If all players are eliminated, winner is highest score
- **Real-time Leaderboard**: Shows current rankings during gameplay

## Troubleshooting

### Common Issues
1. **Controls Not Working**: Make sure you're using the correct keys for your player number
2. **Game Not Starting**: Ensure all players are properly configured in setup
3. **Performance Issues**: Try reducing the number of players or lowering difficulty

### Performance Notes
- Multiplayer mode requires more CPU resources
- 4-player mode may be slower on older systems
- Consider using lower difficulty settings for better performance

## Future Enhancements

Potential improvements for future versions:
- Online multiplayer support
- Tournament mode with brackets
- Spectator mode
- Custom control schemes
- Team-based gameplay
- Power-ups and special effects

## Testing

Run the multiplayer test suite:
```bash
python test_multiplayer.py
```

This will verify:
- Game initialization
- Control mappings
- Piece queue functionality
- Input handling
- State management
