"""High score management system for Tetris."""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class HighScoreManager:
    """Manages high scores for different difficulty modes."""
    
    def __init__(self, filename: str = "highscores.json"):
        """Initialize the high score manager.
        
        Args:
            filename: Name of the file to store high scores.
        """
        self.filename = filename
        self.scores = self._load_scores()
        self.max_scores = 10
    
    def _load_scores(self) -> Dict[str, List[Dict]]:
        """Load high scores from file.
        
        Returns:
            Dictionary with difficulty modes as keys and score lists as values.
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Return empty scores for all difficulty modes
        return {
            'EASY': [],
            'NORMAL': [],
            'HARD': [],
            'EXPERT': [],
            'INSANE': []
        }
    
    def _save_scores(self) -> None:
        """Save high scores to file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except IOError:
            # If we can't save, continue without error
            pass
    
    def add_score(self, difficulty: str, player_name: str, score: int, level: int, lines: int) -> bool:
        """Add a new score to the leaderboard.
        
        Args:
            difficulty: Difficulty mode.
            player_name: Name of the player.
            score: Score achieved.
            level: Level reached.
            lines: Lines cleared.
            
        Returns:
            True if the score made it to the leaderboard, False otherwise.
        """
        if difficulty not in self.scores:
            return False
        
        new_entry = {
            'player': player_name,
            'score': score,
            'level': level,
            'lines': lines,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'difficulty': difficulty
        }
        
        # Add the new score
        self.scores[difficulty].append(new_entry)
        
        # Sort by score (descending) and keep only top scores
        self.scores[difficulty].sort(key=lambda x: x['score'], reverse=True)
        self.scores[difficulty] = self.scores[difficulty][:self.max_scores]
        
        # Save to file
        self._save_scores()
        
        # Check if this score made it to the leaderboard
        return new_entry in self.scores[difficulty]
    
    def get_scores(self, difficulty: str) -> List[Dict]:
        """Get high scores for a specific difficulty.
        
        Args:
            difficulty: Difficulty mode.
            
        Returns:
            List of high score entries.
        """
        return self.scores.get(difficulty, [])
    
    def get_all_scores(self) -> Dict[str, List[Dict]]:
        """Get all high scores.
        
        Returns:
            Dictionary with all difficulty scores.
        """
        return self.scores
    
    def is_high_score(self, difficulty: str, score: int) -> bool:
        """Check if a score qualifies for the leaderboard.
        
        Args:
            difficulty: Difficulty mode.
            score: Score to check.
            
        Returns:
            True if the score would make the leaderboard.
        """
        if difficulty not in self.scores:
            return False
        
        scores = self.scores[difficulty]
        if len(scores) < self.max_scores:
            return True
        
        return score > scores[-1]['score']
    
    def get_rank(self, difficulty: str, score: int) -> int:
        """Get the rank a score would have.
        
        Args:
            difficulty: Difficulty mode.
            score: Score to rank.
            
        Returns:
            Rank (1-based) or -1 if not in top 10.
        """
        if difficulty not in self.scores:
            return -1
        
        scores = self.scores[difficulty]
        for i, entry in enumerate(scores):
            if score > entry['score']:
                return i + 1
        
        if len(scores) < self.max_scores:
            return len(scores) + 1
        
        return -1
    
    def clear_scores(self, difficulty: Optional[str] = None) -> None:
        """Clear high scores.
        
        Args:
            difficulty: Specific difficulty to clear, or None for all.
        """
        if difficulty is None:
            self.scores = {mode: [] for mode in self.scores.keys()}
        elif difficulty in self.scores:
            self.scores[difficulty] = []
        
        self._save_scores()
