"""Multiplayer game management for Tetris."""

import time
import pygame
from typing import List, Dict, Optional, Tuple
from .tetris import TetrisGame
from .tetromino import Tetromino


class MultiplayerGame:
    """Manages multiple Tetris games for local multiplayer."""
    
    def __init__(self, num_players: int = 2, difficulty: str = 'NORMAL'):
        """Initialize a multiplayer Tetris game.
        
        Args:
            num_players: Number of players (2-4).
            difficulty: Difficulty mode for all players.
        """
        if not 2 <= num_players <= 4:
            raise ValueError("Number of players must be between 2 and 4")
        
        self.num_players = num_players
        self.difficulty = difficulty
        self.players = []
        self.game_over = False
        self.winner = None
        self.shared_piece_queue = []
        self.piece_index = 0
        
        # Initialize players
        for i in range(num_players):
            player = {
                'id': i + 1,
                'name': f"Player {i + 1}",
                'game': TetrisGame(difficulty),
                'score': 0,
                'lines_cleared': 0,
                'level': 1,
                'game_over': False,
                'controls': self._get_player_controls(i + 1)
            }
            self.players.append(player)
        
        # Generate shared piece queue
        self._generate_piece_queue()
    
    def _get_player_controls(self, player_id: int) -> Dict[str, int]:
        """Get control mapping for a specific player.
        
        Args:
            player_id: Player number (1-4).
            
        Returns:
            Dictionary mapping action names to pygame key constants.
        """
        if player_id == 1:
            return {
                'left': pygame.K_LEFT,
                'right': pygame.K_RIGHT,
                'down': pygame.K_DOWN,
                'up': pygame.K_UP,
                'rotate_ccw': pygame.K_z,
                'hard_drop': pygame.K_SPACE,
                'pause': pygame.K_p
            }
        elif player_id == 2:
            return {
                'left': pygame.K_a,
                'right': pygame.K_d,
                'down': pygame.K_s,
                'up': pygame.K_w,
                'rotate_ccw': pygame.K_q,
                'hard_drop': pygame.K_e,
                'pause': pygame.K_t
            }
        elif player_id == 3:
            return {
                'left': pygame.K_j,
                'right': pygame.K_l,
                'down': pygame.K_k,
                'up': pygame.K_i,
                'rotate_ccw': pygame.K_u,
                'hard_drop': pygame.K_o,
                'pause': pygame.K_p
            }
        else:  # Player 4
            return {
                'left': pygame.K_LEFT,
                'right': pygame.K_RIGHT,
                'down': pygame.K_DOWN,
                'up': pygame.K_UP,
                'rotate_ccw': pygame.K_z,
                'hard_drop': pygame.K_SPACE,
                'pause': pygame.K_p
            }
    
    def _generate_piece_queue(self) -> None:
        """Generate a shared piece queue for all players."""
        # Generate 50 pieces to ensure fair play
        for _ in range(50):
            piece = Tetromino(difficulty=self.difficulty)
            self.shared_piece_queue.append(piece)
    
    def _get_next_piece(self) -> Tetromino:
        """Get the next piece from the shared queue.
        
        Returns:
            Next tetromino piece.
        """
        if self.piece_index >= len(self.shared_piece_queue):
            # Regenerate queue if we run out
            self._generate_piece_queue()
            self.piece_index = 0
        
        piece = self.shared_piece_queue[self.piece_index]
        self.piece_index += 1
        return piece
    
    def handle_input(self, player_id: int, key: int) -> bool:
        """Handle input for a specific player.
        
        Args:
            player_id: Player number (1-4).
            key: Pygame key constant.
            
        Returns:
            True if input was handled, False otherwise.
        """
        if player_id < 1 or player_id > self.num_players:
            return False
        
        player = self.players[player_id - 1]
        if player['game_over']:
            return False
        
        controls = player['controls']
        game = player['game']
        
        if key == controls['left']:
            return game.move_left()
        elif key == controls['right']:
            return game.move_right()
        elif key == controls['up']:
            return game.rotate_clockwise()
        elif key == controls['rotate_ccw']:
            return game.rotate_counter_clockwise()
        elif key == controls['down']:
            return game.soft_drop()
        elif key == controls['hard_drop']:
            return game.hard_drop()
        elif key == controls['pause']:
            game.pause()
            return True
        
        return False
    
    def update(self) -> None:
        """Update all player games."""
        if self.game_over:
            return
        
        # Update each player's game
        for player in self.players:
            if not player['game_over']:
                player['game'].update()
                
                # Update player stats
                player['score'] = player['game'].score
                player['lines_cleared'] = player['game'].lines_cleared
                player['level'] = player['game'].level
                player['game_over'] = player['game'].game_over
                
                # Check if player is game over
                if player['game_over']:
                    self._check_game_over()
    
    def _check_game_over(self) -> None:
        """Check if the multiplayer game is over."""
        active_players = [p for p in self.players if not p['game_over']]
        
        if len(active_players) <= 1:
            self.game_over = True
            if active_players:
                self.winner = active_players[0]
            else:
                # All players game over - winner is highest score
                self.winner = max(self.players, key=lambda p: p['score'])
    
    def get_player_states(self) -> List[Dict]:
        """Get current state of all players.
        
        Returns:
            List of player state dictionaries.
        """
        return [
            {
                'id': player['id'],
                'name': player['name'],
                'score': player['score'],
                'lines_cleared': player['lines_cleared'],
                'level': player['level'],
                'game_over': player['game_over'],
                'board': player['game'].board,
                'current_piece': player['game'].current_piece,
                'next_piece': player['game'].next_piece,
                'preview_pieces': player['game'].preview_pieces,
                'paused': player['game'].paused
            }
            for player in self.players
        ]
    
    def reset(self) -> None:
        """Reset all player games."""
        for player in self.players:
            player['game'].reset()
            player['score'] = 0
            player['lines_cleared'] = 0
            player['level'] = 1
            player['game_over'] = False
        
        self.game_over = False
        self.winner = None
        self.piece_index = 0
        self._generate_piece_queue()
    
    def set_player_name(self, player_id: int, name: str) -> None:
        """Set the name for a specific player.
        
        Args:
            player_id: Player number (1-4).
            name: Player name.
        """
        if 1 <= player_id <= self.num_players:
            self.players[player_id - 1]['name'] = name
    
    def change_difficulty(self, difficulty: str) -> None:
        """Change the difficulty mode for all players.
        
        Args:
            difficulty: New difficulty mode.
        """
        if difficulty in TetrisGame.DIFFICULTY_MODES:
            self.difficulty = difficulty
            for player in self.players:
                player['game'].change_difficulty(difficulty)
    
    def get_leaderboard(self) -> List[Dict]:
        """Get current leaderboard sorted by score.
        
        Returns:
            List of players sorted by score (highest first).
        """
        return sorted(self.players, key=lambda p: p['score'], reverse=True)
