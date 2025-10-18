#!/usr/bin/env python3
"""Test script to verify arrow keys work in multiplayer mode."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.multiplayer import MultiplayerGame
import pygame

def test_arrow_key_mappings():
    """Test that arrow keys are correctly mapped for players 1 and 4."""
    print("Testing arrow key mappings...")
    
    # Initialize pygame
    pygame.init()
    
    try:
        # Create a 2-player game
        game = MultiplayerGame(2, 'NORMAL')
        
        # Test Player 1 controls (arrow keys)
        player1_controls = game.players[0]['controls']
        print(f"Player 1 controls: {player1_controls}")
        
        # Verify arrow key constants
        assert player1_controls['left'] == pygame.K_LEFT, f"Expected pygame.K_LEFT ({pygame.K_LEFT}), got {player1_controls['left']}"
        assert player1_controls['right'] == pygame.K_RIGHT, f"Expected pygame.K_RIGHT ({pygame.K_RIGHT}), got {player1_controls['right']}"
        assert player1_controls['down'] == pygame.K_DOWN, f"Expected pygame.K_DOWN ({pygame.K_DOWN}), got {player1_controls['down']}"
        assert player1_controls['up'] == pygame.K_UP, f"Expected pygame.K_UP ({pygame.K_UP}), got {player1_controls['up']}"
        
        print("✓ Player 1 arrow key mappings correct")
        
        # Test Player 2 controls (WASD)
        player2_controls = game.players[1]['controls']
        print(f"Player 2 controls: {player2_controls}")
        
        assert player2_controls['left'] == pygame.K_a, f"Expected pygame.K_a ({pygame.K_a}), got {player2_controls['left']}"
        assert player2_controls['right'] == pygame.K_d, f"Expected pygame.K_d ({pygame.K_d}), got {player2_controls['right']}"
        assert player2_controls['down'] == pygame.K_s, f"Expected pygame.K_s ({pygame.K_s}), got {player2_controls['down']}"
        assert player2_controls['up'] == pygame.K_w, f"Expected pygame.K_w ({pygame.K_w}), got {player2_controls['up']}"
        
        print("✓ Player 2 WASD mappings correct")
        
        # Test input handling with actual key codes
        print("\nTesting input handling with arrow keys...")
        
        # Test Player 1 arrow key input
        result = game.handle_input(1, pygame.K_LEFT)
        print(f"Player 1 LEFT arrow input result: {result}")
        
        result = game.handle_input(1, pygame.K_RIGHT)
        print(f"Player 1 RIGHT arrow input result: {result}")
        
        result = game.handle_input(1, pygame.K_DOWN)
        print(f"Player 1 DOWN arrow input result: {result}")
        
        result = game.handle_input(1, pygame.K_UP)
        print(f"Player 1 UP arrow input result: {result}")
        
        # Test Player 2 WASD input
        result = game.handle_input(2, pygame.K_a)
        print(f"Player 2 A key input result: {result}")
        
        result = game.handle_input(2, pygame.K_d)
        print(f"Player 2 D key input result: {result}")
        
        result = game.handle_input(2, pygame.K_s)
        print(f"Player 2 S key input result: {result}")
        
        result = game.handle_input(2, pygame.K_w)
        print(f"Player 2 W key input result: {result}")
        
        print("✓ All input handling tests passed")
        
        return True
        
    except Exception as e:
        print(f"✗ Arrow key test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_4_player_arrow_keys():
    """Test arrow keys for 4-player game (Player 1 and Player 4)."""
    print("\nTesting 4-player arrow key mappings...")
    
    pygame.init()
    
    try:
        # Create a 4-player game
        game = MultiplayerGame(4, 'NORMAL')
        
        # Test Player 1 (arrow keys)
        player1_controls = game.players[0]['controls']
        assert player1_controls['left'] == pygame.K_LEFT
        assert player1_controls['right'] == pygame.K_RIGHT
        assert player1_controls['down'] == pygame.K_DOWN
        assert player1_controls['up'] == pygame.K_UP
        print("✓ Player 1 arrow keys correct")
        
        # Test Player 4 (also arrow keys)
        player4_controls = game.players[3]['controls']
        assert player4_controls['left'] == pygame.K_LEFT
        assert player4_controls['right'] == pygame.K_RIGHT
        assert player4_controls['down'] == pygame.K_DOWN
        assert player4_controls['up'] == pygame.K_UP
        print("✓ Player 4 arrow keys correct")
        
        # Test that both players can use arrow keys
        result1 = game.handle_input(1, pygame.K_LEFT)
        result4 = game.handle_input(4, pygame.K_LEFT)
        
        print(f"Player 1 LEFT arrow: {result1}")
        print(f"Player 4 LEFT arrow: {result4}")
        
        return True
        
    except Exception as e:
        print(f"✗ 4-player arrow key test failed: {e}")
        return False
    finally:
        pygame.quit()

def main():
    """Run arrow key tests."""
    print("Starting arrow key tests...\n")
    
    tests = [
        test_arrow_key_mappings,
        test_4_player_arrow_keys
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Arrow key tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All arrow key tests passed!")
        return True
    else:
        print("❌ Some arrow key tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
