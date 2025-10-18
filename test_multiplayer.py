#!/usr/bin/env python3
"""Test script for multiplayer functionality."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.multiplayer import MultiplayerGame
from game.tetris import TetrisGame
import pygame

def test_multiplayer_initialization():
    """Test multiplayer game initialization."""
    print("Testing multiplayer game initialization...")
    
    try:
        # Test 2-player game
        game = MultiplayerGame(2, 'NORMAL')
        assert game.num_players == 2
        assert len(game.players) == 2
        assert game.difficulty == 'NORMAL'
        print("✓ 2-player game initialization successful")
        
        # Test 4-player game
        game = MultiplayerGame(4, 'HARD')
        assert game.num_players == 4
        assert len(game.players) == 4
        assert game.difficulty == 'HARD'
        print("✓ 4-player game initialization successful")
        
        # Test invalid player count
        try:
            game = MultiplayerGame(1, 'NORMAL')
            assert False, "Should have raised ValueError for 1 player"
        except ValueError:
            print("✓ Correctly rejected 1 player game")
        
        try:
            game = MultiplayerGame(5, 'NORMAL')
            assert False, "Should have raised ValueError for 5 players"
        except ValueError:
            print("✓ Correctly rejected 5 player game")
            
    except Exception as e:
        print(f"✗ Multiplayer initialization test failed: {e}")
        return False
    
    return True

def test_player_controls():
    """Test player control mappings."""
    print("\nTesting player control mappings...")
    
    try:
        game = MultiplayerGame(4, 'NORMAL')
        
        # Test control mappings for each player
        for i, player in enumerate(game.players):
            controls = player['controls']
            assert 'left' in controls
            assert 'right' in controls
            assert 'down' in controls
            assert 'up' in controls
            assert 'rotate_ccw' in controls
            assert 'hard_drop' in controls
            assert 'pause' in controls
            print(f"✓ Player {i+1} controls mapped correctly")
            
    except Exception as e:
        print(f"✗ Player controls test failed: {e}")
        return False
    
    return True

def test_shared_piece_queue():
    """Test shared piece queue functionality."""
    print("\nTesting shared piece queue...")
    
    try:
        game = MultiplayerGame(2, 'NORMAL')
        
        # Test initial queue generation
        assert len(game.shared_piece_queue) == 50
        print("✓ Initial piece queue generated")
        
        # Test piece retrieval
        piece1 = game._get_next_piece()
        piece2 = game._get_next_piece()
        assert piece1 is not None
        assert piece2 is not None
        assert piece1 != piece2  # Should be different pieces
        print("✓ Piece retrieval working")
        
        # Test queue regeneration
        game.piece_index = 50  # Force queue regeneration
        piece3 = game._get_next_piece()
        assert piece3 is not None
        print("✓ Queue regeneration working")
        
    except Exception as e:
        print(f"✗ Shared piece queue test failed: {e}")
        return False
    
    return True

def test_input_handling():
    """Test input handling for different players."""
    print("\nTesting input handling...")
    
    try:
        game = MultiplayerGame(2, 'NORMAL')
        
        # Test player 1 controls (arrow keys)
        result = game.handle_input(1, pygame.K_LEFT)
        assert isinstance(result, bool)
        print("✓ Player 1 input handling working")
        
        # Test player 2 controls (WASD)
        result = game.handle_input(2, pygame.K_a)
        assert isinstance(result, bool)
        print("✓ Player 2 input handling working")
        
        # Test invalid player
        result = game.handle_input(5, pygame.K_LEFT)
        assert result == False
        print("✓ Invalid player handling working")
        
    except Exception as e:
        print(f"✗ Input handling test failed: {e}")
        return False
    
    return True

def test_game_state_management():
    """Test game state management."""
    print("\nTesting game state management...")
    
    try:
        game = MultiplayerGame(2, 'NORMAL')
        
        # Test initial state
        states = game.get_player_states()
        assert len(states) == 2
        assert all('score' in state for state in states)
        assert all('name' in state for state in states)
        assert all('game_over' in state for state in states)
        print("✓ Player state retrieval working")
        
        # Test leaderboard
        leaderboard = game.get_leaderboard()
        assert len(leaderboard) == 2
        print("✓ Leaderboard generation working")
        
        # Test player name setting
        game.set_player_name(1, "TestPlayer")
        assert game.players[0]['name'] == "TestPlayer"
        print("✓ Player name setting working")
        
    except Exception as e:
        print(f"✗ Game state management test failed: {e}")
        return False
    
    return True

def main():
    """Run all multiplayer tests."""
    print("Starting multiplayer functionality tests...\n")
    
    # Initialize pygame for testing
    pygame.init()
    
    tests = [
        test_multiplayer_initialization,
        test_player_controls,
        test_shared_piece_queue,
        test_input_handling,
        test_game_state_management
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    pygame.quit()
    
    print(f"Multiplayer tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All multiplayer tests passed!")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
