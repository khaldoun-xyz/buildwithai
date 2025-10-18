#!/usr/bin/env python3
"""Debug key handling."""

import pygame
import sys

def debug_keys():
    """Debug key handling."""
    pygame.init()
    
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Debug Keys")
    
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    
    print("Debug key test started. Press any key to see the key code.")
    print("Expected: K_1=49, K_2=50, K_3=51, K_4=52, K_5=53")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print(f"Key pressed: {event.key} (pygame.K_1={pygame.K_1}, pygame.K_2={pygame.K_2})")
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:
                    print("K_1 detected!")
                elif event.key == pygame.K_2:
                    print("K_2 detected!")
                elif event.key == pygame.K_3:
                    print("K_3 detected!")
                elif event.key == pygame.K_4:
                    print("K_4 detected!")
                elif event.key == pygame.K_5:
                    print("K_5 detected!")
        
        screen.fill((0, 0, 0))
        
        text = font.render("Press any key to see key code", True, (255, 255, 255))
        screen.blit(text, (50, 50))
        
        text2 = font.render("Expected: 1=49, 2=50, 3=51, 4=52, 5=53", True, (255, 255, 255))
        screen.blit(text2, (50, 80))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    debug_keys()
