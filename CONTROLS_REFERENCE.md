# Tetris Multiplayer Controls Reference

## Quick Control Guide

### Player 1 (Arrow Keys)
```
Movement:  ← → ↓
Rotation:  ↑ (CW)  Z (CCW)
Drop:      Space (Hard Drop)
Pause:     P
```

### Player 2 (WASD)
```
Movement:  A D S
Rotation:  W (CW)  Q (CCW)
Drop:      E (Hard Drop)
Pause:     T
```

### Player 3 (IJKL)
```
Movement:  J L K
Rotation:  I (CW)  U (CCW)
Drop:      O (Hard Drop)
Pause:     P
```

### Player 4 (Arrow Keys - Same as Player 1)
```
Movement:  ← → ↓
Rotation:  ↑ (CW)  Z (CCW)
Drop:      Space (Hard Drop)
Pause:     P
```

## Control Legend

| Action | Player 1 | Player 2 | Player 3 | Player 4 |
|--------|----------|----------|----------|----------|
| Move Left | ← | A | J | ← |
| Move Right | → | D | L | → |
| Move Down (Soft Drop) | ↓ | S | K | ↓ |
| Rotate Clockwise | ↑ | W | I | ↑ |
| Rotate Counter-Clockwise | Z | Q | U | Z |
| Hard Drop | Space | E | O | Space |
| Pause | P | T | P | P |

## Global Controls (All Players)

| Key | Action |
|-----|--------|
| 1-5 | Change Difficulty Mode |
| R | Restart Game (when all players done) |
| ESC | Return to Setup Menu |

## Tips

- **Soft Drop**: Hold down the move down key for faster falling
- **Hard Drop**: Press once to instantly drop the piece to the bottom
- **Rotation**: Use both rotation keys to find the best position
- **Pause**: Any player can pause the game for all players
- **Difficulty**: All players play at the same difficulty level
- **Fair Play**: All players receive the same pieces in the same order

## Getting Started

1. **Start Game**: Run `python main.py`
2. **Select Multiplayer**: Choose "2 - MULTIPLAYER"
3. **Setup Players**: Configure 2-4 players with names
4. **Choose Difficulty**: Select difficulty for all players
5. **Start Playing**: Each player uses their assigned controls

## Troubleshooting

- **Controls Not Working**: Make sure you're using the correct keys for your player number
- **Conflicting Keys**: Players 1 and 4 share the same controls - consider using different players
- **Game Not Starting**: Ensure all players are properly configured in setup
- **Performance Issues**: Try reducing the number of players or lowering difficulty
