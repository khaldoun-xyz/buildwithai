# Product sheet: Tetris

Let's play Tetris!

Build the classic puzzle game.
The user needs to form falling blocks,
called Tetrominoes, into complete horizontal lines.
Your game is supposed to feature a progressive
difficulty curve and a rewarding scoring system.
You may also want to add a multiplayer mode.

## Required features

- **Playfield**: The game will take place
  on a standard 10x20 vertical grid.
- **Tetrominoes**: There will be seven distinct shapes,
  each composed of four blocks: I, O, T, S, Z, J, and L.
  Blocks will be randomly selected and fall
  from the top-center of the playfield.
- **Player controls**: The player must have responsive controls to:
  - Move the falling block left and right.
  - Rotate the block 90 degrees clockwise and counter-clockwise.
  - Soft drop: Intentionally speed up the block's descent.
  - (optional) Hard drop: Instantly drop the block to the
    bottom of the playfield.
- **Line clearing**: When a horizontal row of 10 blocks is completely
  filled with no gaps, that line is cleared.
  All blocks above the cleared line then shift down one row.
- **Scoring system**: Points are awarded primarily for clearing lines.
  To encourage risk-taking and skillful play,
  clearing multiple lines at once provides
  a significantly higher score.
  - Single (1 line): 100 points
  - Double (2 lines): 300 points
  - Triple (3 lines): 500 points
  - Tetris (4 lines): 800 points
  - Additional Points: Award 5 points for each block dropped
    using the "soft drop" or "hard drop" feature to reward faster play.
- **Leveling up**: The player's level increases
  for every 10 lines she clears.
  - With each new level, the passive downward speed of the falling
    blocks increases, giving the player less time to think and act.
    The speed should increase on a well-defined curve,
    starting slow and becoming progressively faster.
- **User interface**: The screen should clearly display
  all essential information.
  - Main playfield: The 10x20 grid where the action happens.
  - Score counter: The player's current total score.
  - Level indicator: The player's current level.
  - Lines cleared: A counter for the total number of lines cleared.
  - Next piece queue: A display showing the next 1-3 upcoming
    Tetrominoes so the player can plan ahead.
  - Game Over screen: The game ends when a newly spawned block has no
    room to appear at the top of the playfield (this is known as
    "blocking out"). A "Game Over" message should be clearly displayed,
    along with the final score.

## Optional features

- **Multiplayer**:
  - Offer a head-to-head multiplayer mode
    where two players compete
    to be the last one standing.
  - **Garbage Lines**: Clearing multiple lines simultaneously on your
    screen will add one or more incomplete "garbage" lines to
    the bottom of your opponent's playfield. These lines have a single
    empty column and push their existing blocks upward, making their
    game more difficult.
    - Clearing a Double sends 1 garbage line.
    - Clearing a Triple sends 2 garbage lines.
    - Clearing a Tetris sends 4 garbage lines.
  - **Gameplay**: Both players play simultaneously in their own
    playfield, visible on a split screen or side-by-side.
    The first player to "block out" loses the round.
