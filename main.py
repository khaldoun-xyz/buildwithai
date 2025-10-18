"""Main entry point for the Tetris game."""

import pygame
import sys
from game.tetris import TetrisGame
from game.multiplayer import MultiplayerGame
from game.renderer import Renderer
from game.audio import AudioManager
from game.highscore import HighScoreManager


def main():
    """Main game loop."""
    pygame.init()
    
    # Initialize components
    renderer = Renderer()
    audio = AudioManager()
    high_score_manager = HighScoreManager()
    
    clock = pygame.time.Clock()
    running = True
    game = None
    multiplayer_game = None
    game_mode_selection = True
    difficulty_selection = False
    multiplayer_setup = False
    selected_difficulty = 1  # Default to Normal
    selected_players = 2  # Default to 2 players
    high_score_entry = False
    high_score_view = False
    player_name = ""
    high_score_difficulty = "NORMAL"
    player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
    current_player_editing = 0
    
    # Start background music
    audio.start_music()
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if high_score_entry:
                        high_score_entry = False
                        if multiplayer_game:
                            multiplayer_setup = True
                        else:
                            difficulty_selection = True
                    elif high_score_view:
                        high_score_view = False
                        if multiplayer_game:
                            multiplayer_setup = True
                        else:
                            difficulty_selection = True
                    elif multiplayer_setup:
                        multiplayer_setup = False
                        game_mode_selection = True
                        multiplayer_game = None
                    elif difficulty_selection:
                        difficulty_selection = False
                        game_mode_selection = True
                    elif game_mode_selection:
                        running = False
                    else:
                        if multiplayer_game:
                            multiplayer_setup = True
                        else:
                            difficulty_selection = True
                        game = None
                        multiplayer_game = None
                
                elif game_mode_selection:
                    # Game mode selection
                    if event.key == pygame.K_1:
                        # Single player mode
                        difficulty_selection = True
                        game_mode_selection = False
                    elif event.key == pygame.K_2:
                        # Multiplayer mode
                        multiplayer_setup = True
                        game_mode_selection = False
                    elif event.key == pygame.K_h:
                        # View high scores
                        high_score_view = True
                        game_mode_selection = False
                        high_score_difficulty = "NORMAL"
                
                elif multiplayer_setup:
                    # Multiplayer setup mode
                    if event.key == pygame.K_1:
                        selected_players = 2
                    elif event.key == pygame.K_2:
                        selected_players = 3
                    elif event.key == pygame.K_3:
                        selected_players = 4
                    elif event.key == pygame.K_RETURN:
                        # Start multiplayer game
                        difficulty_names = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'INSANE']
                        multiplayer_game = MultiplayerGame(selected_players, difficulty_names[selected_difficulty])
                        for i in range(selected_players):
                            multiplayer_game.set_player_name(i + 1, player_names[i])
                        multiplayer_setup = False
                    elif event.key == pygame.K_TAB:
                        # Switch to difficulty selection
                        difficulty_selection = True
                        multiplayer_setup = False
                    elif event.key == pygame.K_BACKSPACE:
                        # Edit player names
                        if len(player_names[current_player_editing]) > 0:
                            player_names[current_player_editing] = player_names[current_player_editing][:-1]
                    elif event.unicode.isprintable() and len(player_names[current_player_editing]) < 15:
                        player_names[current_player_editing] += event.unicode
                    elif event.key == pygame.K_UP:
                        current_player_editing = (current_player_editing - 1) % selected_players
                    elif event.key == pygame.K_DOWN:
                        current_player_editing = (current_player_editing + 1) % selected_players
                
                elif difficulty_selection:
                    # Difficulty selection mode
                    if event.key == pygame.K_1:
                        selected_difficulty = 0
                    elif event.key == pygame.K_2:
                        selected_difficulty = 1
                    elif event.key == pygame.K_3:
                        selected_difficulty = 2
                    elif event.key == pygame.K_4:
                        selected_difficulty = 3
                    elif event.key == pygame.K_5:
                        selected_difficulty = 4
                    elif event.key == pygame.K_RETURN:
                        # Start game with selected difficulty
                        difficulty_names = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'INSANE']
                        game = TetrisGame(difficulty_names[selected_difficulty])
                        difficulty_selection = False
                    elif event.key == pygame.K_h:
                        # View high scores
                        high_score_view = True
                        difficulty_selection = False  # Exit difficulty selection mode
                        high_score_difficulty = "NORMAL"  # Initialize with default difficulty
                
                elif high_score_entry:
                    # High score entry mode
                    if event.key == pygame.K_RETURN:
                        if player_name.strip():
                            # Save the high score
                            difficulty_names = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'INSANE']
                            high_score_manager.add_score(
                                high_score_difficulty,
                                player_name.strip(),
                                game.score,
                                game.level,
                                game.lines_cleared
                            )
                        high_score_entry = False
                        difficulty_selection = True
                        game = None
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.unicode.isprintable() and len(player_name) < 15:
                        player_name += event.unicode
                
                elif high_score_view:
                    # High score view mode
                    if event.key == pygame.K_1:
                        high_score_difficulty = "EASY"
                    elif event.key == pygame.K_2:
                        high_score_difficulty = "NORMAL"
                    elif event.key == pygame.K_3:
                        high_score_difficulty = "HARD"
                    elif event.key == pygame.K_4:
                        high_score_difficulty = "EXPERT"
                    elif event.key == pygame.K_5:
                        high_score_difficulty = "INSANE"
                
                elif game is not None:
                    # Game mode
                    if event.key == pygame.K_p:
                        game.pause()
                    
                    elif event.key == pygame.K_r and game.game_over:
                        # Check if this is a high score
                        if high_score_manager.is_high_score(game.difficulty, game.score):
                            high_score_entry = True
                            high_score_difficulty = game.difficulty
                            player_name = ""
                        else:
                            game.reset()
                            audio.play_placement()
                    
                    elif event.key == pygame.K_1:
                        game.change_difficulty('EASY')
                    elif event.key == pygame.K_2:
                        game.change_difficulty('NORMAL')
                    elif event.key == pygame.K_3:
                        game.change_difficulty('HARD')
                    elif event.key == pygame.K_4:
                        game.change_difficulty('EXPERT')
                    elif event.key == pygame.K_5:
                        game.change_difficulty('INSANE')
                    
                    elif not game.game_over and not game.paused:
                        if event.key == pygame.K_LEFT:
                            if game.move_left():
                                audio.play_rotation()
                        
                        elif event.key == pygame.K_RIGHT:
                            if game.move_right():
                                audio.play_rotation()
                        
                        elif event.key == pygame.K_UP:
                            if game.rotate_clockwise():
                                audio.play_rotation()
                        
                        elif event.key == pygame.K_z:
                            if game.rotate_counter_clockwise():
                                audio.play_rotation()
                        
                        elif event.key == pygame.K_DOWN:
                            if game.soft_drop():
                                audio.play_placement()
                        
                        elif event.key == pygame.K_SPACE:
                            if game.hard_drop():
                                audio.play_placement()
                
                elif multiplayer_game is not None:
                    # Multiplayer game mode
                    if event.key == pygame.K_r and multiplayer_game.game_over:
                        # Reset multiplayer game
                        multiplayer_game.reset()
                        audio.play_placement()
                    
                    elif event.key == pygame.K_1:
                        multiplayer_game.change_difficulty('EASY')
                    elif event.key == pygame.K_2:
                        multiplayer_game.change_difficulty('NORMAL')
                    elif event.key == pygame.K_3:
                        multiplayer_game.change_difficulty('HARD')
                    elif event.key == pygame.K_4:
                        multiplayer_game.change_difficulty('EXPERT')
                    elif event.key == pygame.K_5:
                        multiplayer_game.change_difficulty('INSANE')
                    
                    elif not multiplayer_game.game_over:
                        # Handle input for all players
                        for player_id in range(1, multiplayer_game.num_players + 1):
                            if multiplayer_game.handle_input(player_id, event.key):
                                # Play appropriate sound effect
                                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_z]:
                                    audio.play_rotation()
                                elif event.key in [pygame.K_DOWN, pygame.K_SPACE]:
                                    audio.play_placement()
                                break
        
        # Handle continuous key presses for soft drop
        if game is not None and not game.game_over and not game.paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                if game.soft_drop():
                    audio.play_placement()
        
        # Handle continuous key presses for multiplayer
        if multiplayer_game is not None and not multiplayer_game.game_over:
            keys = pygame.key.get_pressed()
            for player_id in range(1, multiplayer_game.num_players + 1):
                player = multiplayer_game.players[player_id - 1]
                if not player['game_over'] and not player['game'].paused:
                    controls = player['controls']
                    if keys[controls['down']]:
                        if player['game'].soft_drop():
                            audio.play_placement()
        
        # Update game
        if game is not None:
            game.update()
            
            # Check for line clears and play appropriate sound
            if hasattr(game, '_last_lines_cleared'):
                current_lines = game.lines_cleared
                if current_lines > game._last_lines_cleared:
                    lines_cleared_this_frame = current_lines - game._last_lines_cleared
                    audio.play_line_clear(lines_cleared_this_frame)
                game._last_lines_cleared = current_lines
            else:
                game._last_lines_cleared = game.lines_cleared
            
            # Check for game over
            if game.game_over and not hasattr(game, '_game_over_sound_played'):
                audio.play_game_over()
                game._game_over_sound_played = True
        
        # Update multiplayer game
        if multiplayer_game is not None:
            multiplayer_game.update()
            
            # Check for line clears and play appropriate sound for each player
            for player in multiplayer_game.players:
                if not player['game_over']:
                    if hasattr(player['game'], '_last_lines_cleared'):
                        current_lines = player['game'].lines_cleared
                        if current_lines > player['game']._last_lines_cleared:
                            lines_cleared_this_frame = current_lines - player['game']._last_lines_cleared
                            audio.play_line_clear(lines_cleared_this_frame)
                        player['game']._last_lines_cleared = current_lines
                    else:
                        player['game']._last_lines_cleared = player['game'].lines_cleared
                    
                    # Check for game over
                    if player['game'].game_over and not hasattr(player['game'], '_game_over_sound_played'):
                        audio.play_game_over()
                        player['game']._game_over_sound_played = True
            
            # Check if multiplayer game is over
            if multiplayer_game.game_over and not hasattr(multiplayer_game, '_game_over_sound_played'):
                audio.play_game_over()
                multiplayer_game._game_over_sound_played = True
        
        # Render
        renderer.clear_screen()
        
        if high_score_entry:
            # Draw high score entry screen
            renderer.draw_high_score_entry(
                game.score, game.level, game.lines_cleared, 
                high_score_difficulty, player_name
            )
        elif high_score_view:
            # Draw high scores screen
            all_scores = high_score_manager.get_all_scores()
            renderer.draw_high_scores(all_scores, high_score_difficulty)
        elif game_mode_selection:
            # Draw game mode selection screen
            renderer.draw_game_mode_selection()
        elif multiplayer_setup:
            # Draw multiplayer setup screen
            renderer.draw_multiplayer_setup(selected_players, player_names, current_player_editing, selected_difficulty)
        elif difficulty_selection:
            # Draw difficulty selection screen
            renderer.draw_difficulty_selection(selected_difficulty)
        elif multiplayer_game is not None:
            # Draw multiplayer game
            renderer.draw_multiplayer_game(multiplayer_game)
        elif game is not None:
            # Draw game
            renderer.draw_board(game.board)
            
            if game.current_piece:
                # Draw ghost piece if enabled
                if game.difficulty_config['ghost_piece']:
                    ghost_blocks = game.board.get_ghost_position(game.current_piece)
                    for x, y in ghost_blocks:
                        if 0 <= x < renderer.GRID_WIDTH and 0 <= y < renderer.GRID_HEIGHT:
                            renderer._draw_cell(x, y, game.current_piece.color, ghost=True)
                
                # Draw current piece
                renderer.draw_tetromino(game.current_piece)
            
            if game.next_piece:
                renderer.draw_next_piece(game.next_piece, game.preview_pieces)
            
            renderer.draw_info(game.score, game.level, game.lines_cleared, game.difficulty)
            renderer.draw_controls()
            
            if game.paused:
                renderer.draw_pause_screen()
            elif game.game_over:
                renderer.draw_game_over_screen(game.score)
        
        renderer.update_display()
        clock.tick(60)
    
    # Cleanup
    audio.cleanup()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
