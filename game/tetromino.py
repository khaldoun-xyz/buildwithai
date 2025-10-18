"""Tetromino shapes and rotation logic."""

from typing import List, Tuple
import random


class Tetromino:
    """Represents a Tetris piece with shape and rotation states."""
    
    # Define the 7 standard tetromino shapes in their initial rotation
    SHAPES = {
        'I': [['....', '####', '....', '....']],
        'O': [['##', '##']],
        'T': [['.#.', '###', '...']],
        'S': [['.##', '##.', '...']],
        'Z': [['##.', '.##', '...']],
        'J': [['#..', '###', '...']],
        'L': [['..#', '###', '...']]
    }
    
    # Special challenging shapes for Expert and Insane modes
    SPECIAL_SHAPES = {
        'U': [['#.#', '###', '...']],  # U-shape
        'X': [['#.#', '.#.', '#.#']],  # X-shape
        'W': [['#..', '##.', '.##']],  # W-shape
        'F': [['.##', '##.', '.#.']],  # F-shape
        'P': [['##.', '##.', '.#.']],  # P-shape
        'N': [['#..', '###', '..#']],  # N-shape
        'Y': [['#..', '###', '.#.']],  # Y-shape
        'V': [['#..', '#..', '###']],  # V-shape
        'C': [['###', '#..', '###']],  # C-shape
        'H': [['#.#', '###', '#.#']]   # H-shape
    }
    
    COLORS = {
        'I': (0, 255, 255),    # Neon Cyan
        'O': (255, 255, 0),    # Neon Yellow
        'T': (255, 0, 255),    # Neon Magenta
        'S': (0, 255, 0),      # Neon Green
        'Z': (255, 0, 0),      # Neon Red
        'J': (0, 0, 255),      # Neon Blue
        'L': (255, 165, 0),    # Neon Orange
        # Special shape colors (more vibrant)
        'U': (255, 100, 255),  # Bright Magenta
        'X': (100, 255, 100),  # Bright Green
        'W': (255, 200, 0),    # Bright Gold
        'F': (255, 150, 150),  # Bright Pink
        'P': (150, 150, 255),  # Bright Purple
        'N': (255, 100, 100),  # Bright Red
        'Y': (100, 255, 255),  # Bright Cyan
        'V': (255, 255, 100),  # Bright Yellow
        'C': (255, 150, 0),    # Bright Orange
        'H': (200, 100, 255)   # Bright Violet
    }
    
    def __init__(self, shape_type: str = None, difficulty: str = 'NORMAL'):
        """Initialize a tetromino.
        
        Args:
            shape_type: Type of tetromino. If None, randomly selects a shape.
            difficulty: Difficulty mode to determine available shapes.
        """
        if shape_type is None:
            # Choose shape based on difficulty
            if difficulty in ['EXPERT', 'INSANE']:
                # 70% standard shapes, 30% special shapes for Expert/Insane
                if random.random() < 0.7:
                    shape_type = random.choice(list(self.SHAPES.keys()))
                else:
                    shape_type = random.choice(list(self.SPECIAL_SHAPES.keys()))
            else:
                # Only standard shapes for Easy/Normal/Hard
                shape_type = random.choice(list(self.SHAPES.keys()))
        
        self.shape_type = shape_type
        self.rotation = 0
        self.x = 4  # Start at center of 10-width board
        self.y = 0
        self.color = self.COLORS[shape_type]
        self._generate_rotations()
    
    def _generate_rotations(self) -> None:
        """Generate all 4 rotation states for this tetromino."""
        self.rotations = []
        
        # Get the initial shape from appropriate dictionary
        if self.shape_type in self.SHAPES:
            current_shape = self.SHAPES[self.shape_type][0]
        else:
            current_shape = self.SPECIAL_SHAPES[self.shape_type][0]
        
        for _ in range(4):
            self.rotations.append([list(row) for row in current_shape])
            current_shape = self._rotate_clockwise(current_shape)
    
    def _rotate_clockwise(self, shape: List[List[str]]) -> List[List[str]]:
        """Rotate a shape 90 degrees clockwise.
        
        Args:
            shape: 2D list representing the shape.
            
        Returns:
            Rotated shape.
        """
        if not shape:
            return []
        
        rows, cols = len(shape), len(shape[0])
        rotated = [['.' for _ in range(rows)] for _ in range(cols)]
        
        for i in range(rows):
            for j in range(cols):
                rotated[j][rows - 1 - i] = shape[i][j]
        
        return rotated
    
    def get_current_shape(self) -> List[List[str]]:
        """Get the current shape in its current rotation.
        
        Returns:
            Current shape as 2D list.
        """
        return self.rotations[self.rotation]
    
    def get_blocks(self) -> List[Tuple[int, int]]:
        """Get the positions of all blocks in the current shape.
        
        Returns:
            List of (x, y) coordinates relative to tetromino position.
        """
        blocks = []
        shape = self.get_current_shape()
        
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    blocks.append((self.x + col_idx, self.y + row_idx))
        
        return blocks
    
    def rotate_clockwise(self) -> None:
        """Rotate the tetromino 90 degrees clockwise."""
        self.rotation = (self.rotation + 1) % 4
    
    def rotate_counter_clockwise(self) -> None:
        """Rotate the tetromino 90 degrees counter-clockwise."""
        self.rotation = (self.rotation - 1) % 4
    
    def move_left(self) -> None:
        """Move the tetromino one position to the left."""
        self.x -= 1
    
    def move_right(self) -> None:
        """Move the tetromino one position to the right."""
        self.x += 1
    
    def move_down(self) -> None:
        """Move the tetromino one position down."""
        self.y += 1
    
    def move_up(self) -> None:
        """Move the tetromino one position up."""
        self.y -= 1
    
    def get_width(self) -> int:
        """Get the width of the current shape.
        
        Returns:
            Width in blocks.
        """
        shape = self.get_current_shape()
        return len(shape[0]) if shape else 0
    
    def get_height(self) -> int:
        """Get the height of the current shape.
        
        Returns:
            Height in blocks.
        """
        return len(self.get_current_shape())
    
    def copy(self) -> 'Tetromino':
        """Create a copy of this tetromino.
        
        Returns:
            New Tetromino instance with same properties.
        """
        new_tetromino = Tetromino(self.shape_type)
        new_tetromino.rotation = self.rotation
        new_tetromino.x = self.x
        new_tetromino.y = self.y
        return new_tetromino
