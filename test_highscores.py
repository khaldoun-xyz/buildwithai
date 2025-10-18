#!/usr/bin/env python3
"""Test script for high score difficulty switching."""

import pygame
from game.highscore import HighScoreManager
from game.renderer import Renderer

def test_high_score_switching():
    """Test the high score difficulty switching functionality."""
    pygame.init()
    
    # Initialize components
    renderer = Renderer()
    high_score_manager = HighScoreManager()
    
    # Add some test scores
    high_score_manager.add_score('EASY', 'EasyPlayer1', 1000, 5, 20)
    high_score_manager.add_score('EASY', 'EasyPlayer2', 1500, 6, 25)
    high_score_manager.add_score('NORMAL', 'NormalPlayer1', 2000, 8, 35)
    high_score_manager.add_score('NORMAL', 'NormalPlayer2', 2500, 9, 40)
    high_score_manager.add_score('HARD', 'HardPlayer1', 3000, 10, 50)
    high_score_manager.add_score('HARD', 'HardPlayer2', 3500, 11, 55)
    
    print("Test scores added successfully!")
    
    # Test different difficulties
    difficulties = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'INSANE']
    
    for difficulty in difficulties:
        print(f"\nTesting difficulty: {difficulty}")
        scores = high_score_manager.get_scores(difficulty)
        print(f"Number of scores: {len(scores)}")
        for i, score in enumerate(scores):
            print(f"  {i+1}. {score['player']} - {score['score']:,} (Level {score['level']}, {score['lines']} lines)")
    
    print("\nHigh score switching test completed!")

if __name__ == "__main__":
    test_high_score_switching()
