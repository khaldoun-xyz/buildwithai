"""Game board management for Tetris."""

from typing import List, Tuple, Optional
from .tetromino import Tetromino


class Board:
    """Manages the 10x20 Tetris playfield."""
    
    WIDTH = 10
    HEIGHT = 20
    
    def __init__(self):
        """Initialize an empty board."""
        self.grid = [[None for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.lines_cleared = 0
    
    def is_valid_position(self, tetromino: Tetromino) -> bool:
        """Check if a tetromino can be placed at its current position.
        
        Args:
            tetromino: The tetromino to check.
            
        Returns:
            True if the position is valid, False otherwise.
        """
        blocks = tetromino.get_blocks()
        
        for x, y in blocks:
            if x < 0 or x >= self.WIDTH or y >= self.HEIGHT:
                return False
            
            if y >= 0 and self.grid[y][x] is not None:
                return False
        
        return True
    
    def place_tetromino(self, tetromino: Tetromino) -> None:
        """Place a tetromino on the board.
        
        Args:
            tetromino: The tetromino to place.
        """
        blocks = tetromino.get_blocks()
        
        for x, y in blocks:
            if y >= 0:
                self.grid[y][x] = tetromino.color
    
    def clear_lines(self) -> int:
        """Clear completed horizontal lines.
        
        Returns:
            Number of lines cleared.
        """
        lines_to_clear = []
        
        for y in range(self.HEIGHT):
            if all(self.grid[y][x] is not None for x in range(self.WIDTH)):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [None for _ in range(self.WIDTH)])
        
        cleared_count = len(lines_to_clear)
        self.lines_cleared += cleared_count
        
        return cleared_count
    
    def is_game_over(self, tetromino: Tetromino) -> bool:
        """Check if the game is over.
        
        Args:
            tetromino: The current falling tetromino.
            
        Returns:
            True if game is over, False otherwise.
        """
        return not self.is_valid_position(tetromino)
    
    def get_cell(self, x: int, y: int) -> Optional[Tuple[int, int, int]]:
        """Get the color of a cell at the given position.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
            
        Returns:
            RGB color tuple or None if empty.
        """
        if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
            return self.grid[y][x]
        return None
    
    def get_drop_position(self, tetromino: Tetromino) -> int:
        """Get the lowest valid Y position for a tetromino.
        
        Args:
            tetromino: The tetromino to drop.
            
        Returns:
            The Y coordinate where the tetromino should land.
        """
        original_y = tetromino.y
        drop_y = original_y
        
        while self.is_valid_position(tetromino):
            drop_y = tetromino.y
            tetromino.move_down()
        
        tetromino.y = original_y
        return drop_y
    
    def hard_drop(self, tetromino: Tetromino) -> int:
        """Perform a hard drop for a tetromino.
        
        Args:
            tetromino: The tetromino to drop.
            
        Returns:
            Number of blocks dropped (for scoring).
        """
        original_y = tetromino.y
        drop_y = self.get_drop_position(tetromino)
        tetromino.y = drop_y
        return original_y - drop_y
    
    def get_ghost_position(self, tetromino: Tetromino) -> List[Tuple[int, int]]:
        """Get the ghost (preview) position of a tetromino.
        
        Args:
            tetromino: The tetromino to preview.
            
        Returns:
            List of (x, y) coordinates for the ghost position.
        """
        ghost = tetromino.copy()
        drop_y = self.get_drop_position(ghost)
        ghost.y = drop_y
        return ghost.get_blocks()
    
    def reset(self) -> None:
        """Reset the board to empty state."""
        self.grid = [[None for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.lines_cleared = 0
