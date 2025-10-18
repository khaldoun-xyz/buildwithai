"""Main Tetris game logic."""

import random
import time
from typing import Optional
from .tetromino import Tetromino
from .board import Board


class TetrisGame:
    """Main game controller for Tetris."""
    
    # Difficulty modes
    DIFFICULTY_MODES = {
        'EASY': {
            'name': 'Easy',
            'base_fall_time': 1.5,
            'speed_multiplier': 0.95,
            'lines_per_level': 15,
            'score_multiplier': 0.5,
            'ghost_piece': True,
            'preview_pieces': 3
        },
        'NORMAL': {
            'name': 'Normal',
            'base_fall_time': 1.0,
            'speed_multiplier': 0.9,
            'lines_per_level': 10,
            'score_multiplier': 1.0,
            'ghost_piece': True,
            'preview_pieces': 1
        },
        'HARD': {
            'name': 'Hard',
            'base_fall_time': 0.7,
            'speed_multiplier': 0.85,
            'lines_per_level': 8,
            'score_multiplier': 1.5,
            'ghost_piece': True,
            'preview_pieces': 1
        },
        'EXPERT': {
            'name': 'Expert',
            'base_fall_time': 0.5,
            'speed_multiplier': 0.8,
            'lines_per_level': 6,
            'score_multiplier': 2.0,
            'ghost_piece': False,
            'preview_pieces': 0
        },
        'INSANE': {
            'name': 'Insane',
            'base_fall_time': 0.3,
            'speed_multiplier': 0.75,
            'lines_per_level': 5,
            'score_multiplier': 3.0,
            'ghost_piece': False,
            'preview_pieces': 0
        }
    }
    
    # Base scoring system
    SCORE_SINGLE = 100
    SCORE_DOUBLE = 300
    SCORE_TRIPLE = 500
    SCORE_TETRIS = 800
    SCORE_SOFT_DROP = 5
    
    def __init__(self, difficulty: str = 'NORMAL'):
        """Initialize a new Tetris game.
        
        Args:
            difficulty: Difficulty mode ('EASY', 'NORMAL', 'HARD', 'EXPERT', 'INSANE').
        """
        if difficulty not in self.DIFFICULTY_MODES:
            difficulty = 'NORMAL'
        
        self.difficulty = difficulty
        self.difficulty_config = self.DIFFICULTY_MODES[difficulty]
        
        self.board = Board()
        self.current_piece: Optional[Tetromino] = None
        self.next_piece: Optional[Tetromino] = None
        self.preview_pieces: list = []
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = self.difficulty_config['base_fall_time']
        self.last_fall_time = time.time()
        self.game_over = False
        self.paused = False
        self._spawn_piece()
    
    def _spawn_piece(self) -> None:
        """Spawn a new piece at the top of the board."""
        if self.next_piece is None:
            self.next_piece = Tetromino(difficulty=self.difficulty)
        
        self.current_piece = self.next_piece
        self.next_piece = Tetromino(difficulty=self.difficulty)
        
        # Generate preview pieces based on difficulty
        self.preview_pieces = []
        for _ in range(self.difficulty_config['preview_pieces']):
            self.preview_pieces.append(Tetromino(difficulty=self.difficulty))
        
        if self.board.is_game_over(self.current_piece):
            self.game_over = True
    
    def _get_fall_time(self) -> float:
        """Calculate the fall time based on current level and difficulty.
        
        Returns:
            Time in seconds between automatic drops.
        """
        return self.difficulty_config['base_fall_time'] * (self.difficulty_config['speed_multiplier'] ** (self.level - 1))
    
    def _update_level(self) -> None:
        """Update level based on lines cleared and difficulty."""
        new_level = (self.lines_cleared // self.difficulty_config['lines_per_level']) + 1
        if new_level > self.level:
            self.level = new_level
            self.fall_time = self._get_fall_time()
    
    def _score_lines(self, lines_cleared: int) -> None:
        """Add points for cleared lines with difficulty multiplier.
        
        Args:
            lines_cleared: Number of lines cleared.
        """
        base_score = 0
        if lines_cleared == 1:
            base_score = self.SCORE_SINGLE
        elif lines_cleared == 2:
            base_score = self.SCORE_DOUBLE
        elif lines_cleared == 3:
            base_score = self.SCORE_TRIPLE
        elif lines_cleared == 4:
            base_score = self.SCORE_TETRIS
        
        # Apply difficulty multiplier
        multiplier = self.difficulty_config['score_multiplier']
        self.score += int(base_score * multiplier)
    
    def _score_soft_drop(self, blocks_dropped: int) -> None:
        """Add points for soft drop with difficulty multiplier.
        
        Args:
            blocks_dropped: Number of blocks dropped.
        """
        multiplier = self.difficulty_config['score_multiplier']
        self.score += int(blocks_dropped * self.SCORE_SOFT_DROP * multiplier)
    
    def move_left(self) -> bool:
        """Move current piece left.
        
        Returns:
            True if move was successful, False otherwise.
        """
        if self.game_over or self.paused or self.current_piece is None:
            return False
        
        self.current_piece.move_left()
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.move_right()
            return False
        return True
    
    def move_right(self) -> bool:
        """Move current piece right.
        
        Returns:
            True if move was successful, False otherwise.
        """
        if self.game_over or self.paused or self.current_piece is None:
            return False
        
        self.current_piece.move_right()
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.move_left()
            return False
        return True
    
    def rotate_clockwise(self) -> bool:
        """Rotate current piece clockwise.
        
        Returns:
            True if rotation was successful, False otherwise.
        """
        if self.game_over or self.paused or self.current_piece is None:
            return False
        
        self.current_piece.rotate_clockwise()
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.rotate_counter_clockwise()
            return False
        return True
    
    def rotate_counter_clockwise(self) -> bool:
        """Rotate current piece counter-clockwise.
        
        Returns:
            True if rotation was successful, False otherwise.
        """
        if self.game_over or self.paused or self.current_piece is None:
            return False
        
        self.current_piece.rotate_counter_clockwise()
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.rotate_clockwise()
            return False
        return True
    
    def soft_drop(self) -> bool:
        """Perform soft drop (faster fall).
        
        Returns:
            True if drop was successful, False otherwise.
        """
        if self.game_over or self.paused or self.current_piece is None:
            return False
        
        self.current_piece.move_down()
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.move_up()
            return False
        
        self._score_soft_drop(1)
        return True
    
    def hard_drop(self) -> bool:
        """Perform hard drop (instant drop to bottom).
        
        Returns:
            True if drop was successful, False otherwise.
        """
        if self.game_over or self.paused or self.current_piece is None:
            return False
        
        blocks_dropped = self.board.hard_drop(self.current_piece)
        self._score_soft_drop(blocks_dropped)
        self._lock_piece()
        return True
    
    def _lock_piece(self) -> None:
        """Lock the current piece to the board."""
        if self.current_piece is None:
            return
        
        self.board.place_tetromino(self.current_piece)
        lines_cleared = self.board.clear_lines()
        
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            self._score_lines(lines_cleared)
            self._update_level()
        
        self.current_piece = None
        self._spawn_piece()
    
    def update(self) -> None:
        """Update game state (called every frame)."""
        if self.game_over or self.paused or self.current_piece is None:
            return
        
        current_time = time.time()
        if current_time - self.last_fall_time >= self.fall_time:
            self.current_piece.move_down()
            
            if not self.board.is_valid_position(self.current_piece):
                self.current_piece.move_up()
                self._lock_piece()
            
            self.last_fall_time = current_time
    
    def pause(self) -> None:
        """Toggle pause state."""
        if not self.game_over:
            self.paused = not self.paused
    
    def reset(self) -> None:
        """Reset the game to initial state."""
        self.board = Board()
        self.current_piece = None
        self.next_piece = None
        self.preview_pieces = []
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = self.difficulty_config['base_fall_time']
        self.last_fall_time = time.time()
        self.game_over = False
        self.paused = False
        self._spawn_piece()
    
    def change_difficulty(self, difficulty: str) -> None:
        """Change the difficulty mode.
        
        Args:
            difficulty: New difficulty mode.
        """
        if difficulty in self.DIFFICULTY_MODES:
            self.difficulty = difficulty
            self.difficulty_config = self.DIFFICULTY_MODES[difficulty]
            self.fall_time = self.difficulty_config['base_fall_time']
            self._spawn_piece()
    
    def get_state(self) -> dict:
        """Get current game state.
        
        Returns:
            Dictionary containing game state information.
        """
        return {
            'board': self.board,
            'current_piece': self.current_piece,
            'next_piece': self.next_piece,
            'score': self.score,
            'level': self.level,
            'lines_cleared': self.lines_cleared,
            'game_over': self.game_over,
            'paused': self.paused
        }
