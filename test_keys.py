#!/usr/bin/env python3
"""Test script for key handling in high score view."""

import pygame
import sys

def test_key_handling():
    """Test key handling for high score view."""
    pygame.init()
    
    # Create a simple window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Key Test")
    
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    
    high_score_view = True
    high_score_difficulty = "NORMAL"
    
    print("Key test started. Press 1-5 to switch difficulties, ESC to quit")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif high_score_view:
                    if event.key == pygame.K_1:
                        high_score_difficulty = "EASY"
                        print(f"Switched to EASY, current: {high_score_difficulty}")
                    elif event.key == pygame.K_2:
                        high_score_difficulty = "NORMAL"
                        print(f"Switched to NORMAL, current: {high_score_difficulty}")
                    elif event.key == pygame.K_3:
                        high_score_difficulty = "HARD"
                        print(f"Switched to HARD, current: {high_score_difficulty}")
                    elif event.key == pygame.K_4:
                        high_score_difficulty = "EXPERT"
                        print(f"Switched to EXPERT, current: {high_score_difficulty}")
                    elif event.key == pygame.K_5:
                        high_score_difficulty = "INSANE"
                        print(f"Switched to INSANE, current: {high_score_difficulty}")
                    else:
                        print(f"Other key pressed: {event.key}")
        
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Draw current difficulty
        text = font.render(f"Current Difficulty: {high_score_difficulty}", True, (255, 255, 255))
        screen.blit(text, (50, 50))
        
        # Draw instructions
        inst_text = font.render("Press 1-5 to switch, ESC to quit", True, (255, 255, 255))
        screen.blit(inst_text, (50, 100))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    test_key_handling()
