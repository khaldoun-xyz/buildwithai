"""Rendering system for Tetris game."""

import pygame
from typing import Tuple, List, Optional
from .tetromino import Tetromino
from .board import Board


class Renderer:
    """Handles all rendering for the Tetris game."""
    
    # Colors - Enhanced palette
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (64, 64, 64)
    
    # Fancy colors
    NEON_BLUE = (0, 255, 255)
    NEON_GREEN = (0, 255, 0)
    NEON_PINK = (255, 0, 255)
    NEON_YELLOW = (255, 255, 0)
    NEON_ORANGE = (255, 165, 0)
    NEON_RED = (255, 0, 0)
    NEON_PURPLE = (128, 0, 255)
    
    # Gradient colors
    GRADIENT_START = (20, 20, 40)
    GRADIENT_END = (40, 20, 60)
    
    # UI colors
    UI_BG = (30, 30, 50)
    UI_BORDER = (100, 100, 150)
    UI_HIGHLIGHT = (150, 150, 200)
    
    # Grid settings
    CELL_SIZE = 30
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    BOARD_X = 50
    BOARD_Y = 50
    
    def __init__(self, screen_width: int = 800, screen_height: int = 700):
        """Initialize the renderer.
        
        Args:
            screen_width: Width of the game window.
            screen_height: Height of the game window.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Tetris")
        
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Calculate UI positions
        self.info_x = self.BOARD_X + (self.GRID_WIDTH * self.CELL_SIZE) + 50
        self.info_y = self.BOARD_Y
    
    def clear_screen(self) -> None:
        """Clear the screen with gradient background."""
        # Create gradient background
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            r = int(self.GRADIENT_START[0] + (self.GRADIENT_END[0] - self.GRADIENT_START[0]) * ratio)
            g = int(self.GRADIENT_START[1] + (self.GRADIENT_END[1] - self.GRADIENT_START[1]) * ratio)
            b = int(self.GRADIENT_START[2] + (self.GRADIENT_END[2] - self.GRADIENT_START[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen_width, y))
    
    def draw_board(self, board: Board) -> None:
        """Draw the game board with fancy effects.
        
        Args:
            board: The game board to draw.
        """
        # Draw board background with gradient
        board_rect = pygame.Rect(
            self.BOARD_X, self.BOARD_Y,
            self.GRID_WIDTH * self.CELL_SIZE,
            self.GRID_HEIGHT * self.CELL_SIZE
        )
        
        # Create gradient background for board
        for y in range(self.GRID_HEIGHT * self.CELL_SIZE):
            ratio = y / (self.GRID_HEIGHT * self.CELL_SIZE)
            r = int(20 + (40 - 20) * ratio)
            g = int(20 + (30 - 20) * ratio)
            b = int(30 + (50 - 30) * ratio)
            pygame.draw.line(self.screen, (r, g, b), 
                           (self.BOARD_X, self.BOARD_Y + y), 
                           (self.BOARD_X + self.GRID_WIDTH * self.CELL_SIZE, self.BOARD_Y + y))
        
        # Draw fancy border with glow effect
        pygame.draw.rect(self.screen, self.UI_BORDER, board_rect, 3)
        pygame.draw.rect(self.screen, self.UI_HIGHLIGHT, board_rect, 1)
        
        # Draw grid lines with subtle glow
        for x in range(self.GRID_WIDTH + 1):
            start_pos = (self.BOARD_X + x * self.CELL_SIZE, self.BOARD_Y)
            end_pos = (self.BOARD_X + x * self.CELL_SIZE, self.BOARD_Y + self.GRID_HEIGHT * self.CELL_SIZE)
            pygame.draw.line(self.screen, (60, 60, 80), start_pos, end_pos, 1)
        
        for y in range(self.GRID_HEIGHT + 1):
            start_pos = (self.BOARD_X, self.BOARD_Y + y * self.CELL_SIZE)
            end_pos = (self.BOARD_X + self.GRID_WIDTH * self.CELL_SIZE, self.BOARD_Y + y * self.CELL_SIZE)
            pygame.draw.line(self.screen, (60, 60, 80), start_pos, end_pos, 1)
        
        # Draw placed blocks with fancy effects
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                color = board.get_cell(x, y)
                if color:
                    self._draw_fancy_cell(x, y, color)
    
    def draw_tetromino(self, tetromino: Tetromino, ghost: bool = False) -> None:
        """Draw a tetromino.
        
        Args:
            tetromino: The tetromino to draw.
            ghost: If True, draw as ghost (semi-transparent).
        """
        blocks = tetromino.get_blocks()
        color = tetromino.color
        
        if ghost:
            # Make color semi-transparent
            color = tuple(int(c * 0.3) for c in color)
        
        for x, y in blocks:
            if 0 <= x < self.GRID_WIDTH and 0 <= y < self.GRID_HEIGHT:
                self._draw_cell(x, y, color, ghost)
    
    def _draw_cell(self, x: int, y: int, color: Tuple[int, int, int], ghost: bool = False) -> None:
        """Draw a single cell.
        
        Args:
            x: X coordinate on the grid.
            y: Y coordinate on the grid.
            color: RGB color tuple.
            ghost: If True, draw with border only.
        """
        cell_rect = pygame.Rect(
            self.BOARD_X + x * self.CELL_SIZE + 1,
            self.BOARD_Y + y * self.CELL_SIZE + 1,
            self.CELL_SIZE - 2,
            self.CELL_SIZE - 2
        )
        
        if ghost:
            pygame.draw.rect(self.screen, color, cell_rect)
            pygame.draw.rect(self.screen, self.WHITE, cell_rect, 2)
        else:
            pygame.draw.rect(self.screen, color, cell_rect)
            pygame.draw.rect(self.screen, self.WHITE, cell_rect, 1)
    
    def _draw_fancy_cell(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """Draw a fancy cell with 3D effect and glow.
        
        Args:
            x: X coordinate on the grid.
            y: Y coordinate on the grid.
            color: RGB color tuple.
        """
        cell_rect = pygame.Rect(
            self.BOARD_X + x * self.CELL_SIZE + 1,
            self.BOARD_Y + y * self.CELL_SIZE + 1,
            self.CELL_SIZE - 2,
            self.CELL_SIZE - 2
        )
        
        # Create glow effect
        glow_color = tuple(min(255, c + 50) for c in color)
        glow_rect = pygame.Rect(cell_rect.x - 2, cell_rect.y - 2, 
                               cell_rect.width + 4, cell_rect.height + 4)
        pygame.draw.rect(self.screen, glow_color, glow_rect, 2)
        
        # Draw main cell with gradient effect
        pygame.draw.rect(self.screen, color, cell_rect)
        
        # Add 3D effect with highlights and shadows
        highlight_color = tuple(min(255, c + 80) for c in color)
        shadow_color = tuple(max(0, c - 80) for c in color)
        
        # Top and left highlights
        pygame.draw.line(self.screen, highlight_color, 
                        (cell_rect.left, cell_rect.top), 
                        (cell_rect.right, cell_rect.top), 2)
        pygame.draw.line(self.screen, highlight_color, 
                        (cell_rect.left, cell_rect.top), 
                        (cell_rect.left, cell_rect.bottom), 2)
        
        # Bottom and right shadows
        pygame.draw.line(self.screen, shadow_color, 
                        (cell_rect.left, cell_rect.bottom - 1), 
                        (cell_rect.right, cell_rect.bottom - 1), 2)
        pygame.draw.line(self.screen, shadow_color, 
                        (cell_rect.right - 1, cell_rect.top), 
                        (cell_rect.right - 1, cell_rect.bottom), 2)
        
        # Inner border
        pygame.draw.rect(self.screen, self.WHITE, cell_rect, 1)
    
    def _draw_fancy_cell_small(self, cell_rect: pygame.Rect, color: Tuple[int, int, int]) -> None:
        """Draw a small fancy cell for UI elements.
        
        Args:
            cell_rect: Rectangle to draw the cell in.
            color: RGB color tuple.
        """
        # Create glow effect
        glow_color = tuple(min(255, c + 30) for c in color)
        glow_rect = pygame.Rect(cell_rect.x - 1, cell_rect.y - 1, 
                               cell_rect.width + 2, cell_rect.height + 2)
        pygame.draw.rect(self.screen, glow_color, glow_rect, 1)
        
        # Draw main cell
        pygame.draw.rect(self.screen, color, cell_rect)
        
        # Add 3D effect
        highlight_color = tuple(min(255, c + 60) for c in color)
        shadow_color = tuple(max(0, c - 60) for c in color)
        
        # Highlights
        pygame.draw.line(self.screen, highlight_color, 
                        (cell_rect.left, cell_rect.top), 
                        (cell_rect.right, cell_rect.top), 1)
        pygame.draw.line(self.screen, highlight_color, 
                        (cell_rect.left, cell_rect.top), 
                        (cell_rect.left, cell_rect.bottom), 1)
        
        # Shadows
        pygame.draw.line(self.screen, shadow_color, 
                        (cell_rect.left, cell_rect.bottom - 1), 
                        (cell_rect.right, cell_rect.bottom - 1), 1)
        pygame.draw.line(self.screen, shadow_color, 
                        (cell_rect.right - 1, cell_rect.top), 
                        (cell_rect.right - 1, cell_rect.bottom), 1)
    
    def _draw_fancy_panel(self, rect: pygame.Rect, title: str) -> None:
        """Draw a fancy UI panel with title.
        
        Args:
            rect: Rectangle for the panel.
            title: Title text for the panel.
        """
        # Draw panel background with gradient
        for y in range(rect.height):
            ratio = y / rect.height
            r = int(self.UI_BG[0] + (self.UI_BG[0] + 20 - self.UI_BG[0]) * ratio)
            g = int(self.UI_BG[1] + (self.UI_BG[1] + 20 - self.UI_BG[1]) * ratio)
            b = int(self.UI_BG[2] + (self.UI_BG[2] + 20 - self.UI_BG[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), 
                           (rect.left, rect.top + y), 
                           (rect.right, rect.top + y))
        
        # Draw borders
        pygame.draw.rect(self.screen, self.UI_BORDER, rect, 2)
        pygame.draw.rect(self.screen, self.UI_HIGHLIGHT, rect, 1)
        
        # Draw title
        title_text = self.font_small.render(title, True, self.UI_HIGHLIGHT)
        title_rect = title_text.get_rect(center=(rect.centerx, rect.top + 15))
        self.screen.blit(title_text, title_rect)
    
    def draw_next_piece(self, tetromino: Tetromino, preview_pieces: list = None) -> None:
        """Draw the next piece preview with fancy styling.
        
        Args:
            tetromino: The next piece to draw.
            preview_pieces: List of additional preview pieces.
        """
        # Calculate panel height based on number of preview pieces
        num_previews = len(preview_pieces) if preview_pieces else 0
        panel_height = 120 + (num_previews * 40)
        
        # Draw fancy panel background
        panel_rect = pygame.Rect(self.info_x - 10, self.info_y - 10, 200, panel_height)
        self._draw_fancy_panel(panel_rect, "NEXT PIECES")
        
        # Draw next piece
        next_x = self.info_x + 20
        next_y = self.info_y + 50
        
        shape = tetromino.get_current_shape()
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    cell_rect = pygame.Rect(
                        next_x + col_idx * 25,
                        next_y + row_idx * 25,
                        22,
                        22
                    )
                    self._draw_fancy_cell_small(cell_rect, tetromino.color)
        
        # Draw additional preview pieces
        if preview_pieces:
            for i, piece in enumerate(preview_pieces[:3]):  # Limit to 3 previews
                preview_y = next_y + 60 + (i * 40)
                shape = piece.get_current_shape()
                for row_idx, row in enumerate(shape):
                    for col_idx, cell in enumerate(row):
                        if cell == '#':
                            cell_rect = pygame.Rect(
                                next_x + col_idx * 20,
                                preview_y + row_idx * 20,
                                18,
                                18
                            )
                            self._draw_fancy_cell_small(cell_rect, piece.color)
    
    def draw_info(self, score: int, level: int, lines_cleared: int, difficulty: str = "NORMAL") -> None:
        """Draw game information with fancy styling.
        
        Args:
            score: Current score.
            level: Current level.
            lines_cleared: Total lines cleared.
            difficulty: Current difficulty mode.
        """
        y_offset = self.info_y + 200
        
        # Draw fancy info panel
        info_panel_rect = pygame.Rect(self.info_x - 10, y_offset - 10, 200, 180)
        self._draw_fancy_panel(info_panel_rect, "GAME INFO")
        
        # Difficulty with neon effect
        diff_text = self.font_medium.render(f"MODE: {difficulty}", True, self.NEON_YELLOW)
        self.screen.blit(diff_text, (self.info_x, y_offset + 20))
        
        # Score with neon effect
        score_text = self.font_medium.render(f"SCORE: {score:,}", True, self.NEON_GREEN)
        self.screen.blit(score_text, (self.info_x, y_offset + 50))
        
        # Level with neon effect
        level_text = self.font_medium.render(f"LEVEL: {level}", True, self.NEON_BLUE)
        self.screen.blit(level_text, (self.info_x, y_offset + 80))
        
        # Lines cleared with neon effect
        lines_text = self.font_medium.render(f"LINES: {lines_cleared}", True, self.NEON_PINK)
        self.screen.blit(lines_text, (self.info_x, y_offset + 110))
        
        # Special shapes indicator for Expert/Insane
        if difficulty in ['EXPERT', 'INSANE']:
            special_text = self.font_small.render("SPECIAL SHAPES ACTIVE!", True, self.NEON_YELLOW)
            self.screen.blit(special_text, (self.info_x, y_offset + 140))
    
    def draw_controls(self) -> None:
        """Draw control instructions with fancy styling."""
        controls = [
            "CONTROLS",
            "← → Move",
            "↑ Rotate CW",
            "Z Rotate CCW",
            "↓ Soft Drop",
            "Space Hard Drop",
            "P Pause",
            "1-5 Difficulty",
            "H High Scores",
            "ESC Quit"
        ]
        
        y_offset = self.info_y + 350
        
        # Draw fancy controls panel
        controls_panel_rect = pygame.Rect(self.info_x - 10, y_offset - 10, 200, 220)
        self._draw_fancy_panel(controls_panel_rect, "CONTROLS")
        
        for i, control in enumerate(controls):
            if i == 0:
                # Title
                color = self.NEON_YELLOW
                font = self.font_medium
            else:
                # Control items
                color = self.UI_HIGHLIGHT
                font = self.font_small
            
            text = font.render(control, True, color)
            self.screen.blit(text, (self.info_x, y_offset + 20 + i * 22))
    
    def draw_difficulty_selection(self, selected_difficulty: int = 1) -> None:
        """Draw difficulty selection screen.
        
        Args:
            selected_difficulty: Currently selected difficulty (0-4).
        """
        # Create overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw main panel
        main_panel_rect = pygame.Rect(
            self.screen_width // 2 - 300,
            self.screen_height // 2 - 200,
            600, 400
        )
        self._draw_fancy_panel(main_panel_rect, "SELECT DIFFICULTY")
        
        # Title
        title_text = self.font_large.render("CHOOSE YOUR CHALLENGE", True, self.NEON_BLUE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 150))
        self.screen.blit(title_text, title_rect)
        
        # Difficulty options
        difficulties = [
            ("1 - EASY", "Slow speed, 3 previews, ghost piece", self.NEON_GREEN),
            ("2 - NORMAL", "Standard Tetris experience", self.NEON_BLUE),
            ("3 - HARD", "Faster speed, fewer previews", self.NEON_ORANGE),
            ("4 - EXPERT", "Very fast, special shapes, no ghost", self.NEON_RED),
            ("5 - INSANE", "Extreme speed, special shapes, no previews", self.NEON_PURPLE)
        ]
        
        for i, (name, desc, color) in enumerate(difficulties):
            y_pos = self.screen_height // 2 - 80 + i * 50
            
            # Highlight selected difficulty
            if i == selected_difficulty:
                pygame.draw.rect(self.screen, (50, 50, 100), 
                               (self.screen_width // 2 - 280, y_pos - 5, 560, 40))
            
            # Difficulty name
            name_text = self.font_medium.render(name, True, color)
            name_rect = name_text.get_rect(center=(self.screen_width // 2, y_pos))
            self.screen.blit(name_text, name_rect)
            
            # Description
            desc_text = self.font_small.render(desc, True, self.UI_HIGHLIGHT)
            desc_rect = desc_text.get_rect(center=(self.screen_width // 2, y_pos + 20))
            self.screen.blit(desc_text, desc_rect)
        
        # Instructions
        inst_text = self.font_small.render("Press 1-5 to select, ENTER to start", True, self.UI_HIGHLIGHT)
        inst_rect = inst_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 180))
        self.screen.blit(inst_text, inst_rect)
        
        # High scores option
        hs_text = self.font_small.render("Press H to view High Scores", True, self.NEON_YELLOW)
        hs_rect = hs_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 210))
        self.screen.blit(hs_text, hs_rect)
    
    def draw_high_score_entry(self, score: int, level: int, lines: int, difficulty: str, player_name: str = "") -> None:
        """Draw high score entry screen.
        
        Args:
            score: Final score achieved.
            level: Level reached.
            lines: Lines cleared.
            difficulty: Difficulty mode.
            player_name: Current player name input.
        """
        # Create overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw main panel
        main_panel_rect = pygame.Rect(
            self.screen_width // 2 - 300,
            self.screen_height // 2 - 150,
            600, 300
        )
        self._draw_fancy_panel(main_panel_rect, "NEW HIGH SCORE!")
        
        # Congratulations text
        congrats_text = self.font_large.render("CONGRATULATIONS!", True, self.NEON_GREEN)
        congrats_rect = congrats_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
        self.screen.blit(congrats_text, congrats_rect)
        
        # Score details
        score_text = self.font_medium.render(f"Score: {score:,}", True, self.NEON_BLUE)
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 60))
        self.screen.blit(score_text, score_rect)
        
        level_text = self.font_medium.render(f"Level: {level} | Lines: {lines}", True, self.NEON_PINK)
        level_rect = level_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 30))
        self.screen.blit(level_text, level_rect)
        
        # Player name input
        name_label = self.font_medium.render("Enter your name:", True, self.UI_HIGHLIGHT)
        name_label_rect = name_label.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 10))
        self.screen.blit(name_label, name_label_rect)
        
        # Name input box
        name_box_rect = pygame.Rect(
            self.screen_width // 2 - 150,
            self.screen_height // 2 + 40,
            300, 40
        )
        pygame.draw.rect(self.screen, self.UI_BG, name_box_rect)
        pygame.draw.rect(self.screen, self.UI_BORDER, name_box_rect, 2)
        
        # Player name text
        name_text = self.font_medium.render(player_name + "_", True, self.WHITE)
        name_text_rect = name_text.get_rect(center=name_box_rect.center)
        self.screen.blit(name_text, name_text_rect)
        
        # Instructions
        inst_text = self.font_small.render("Type your name and press ENTER to save", True, self.UI_HIGHLIGHT)
        inst_rect = inst_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 100))
        self.screen.blit(inst_text, inst_rect)
    
    def draw_high_scores(self, scores: dict, current_difficulty: str = "NORMAL") -> None:
        """Draw high scores leaderboard.
        
        Args:
            scores: Dictionary of scores by difficulty.
            current_difficulty: Currently selected difficulty to highlight.
        """
        # Create overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw main panel
        main_panel_rect = pygame.Rect(
            self.screen_width // 2 - 400,
            self.screen_height // 2 - 250,
            800, 500
        )
        self._draw_fancy_panel(main_panel_rect, "HIGH SCORES")
        
        # Title
        title_text = self.font_large.render("LEADERBOARD", True, self.NEON_BLUE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 200))
        self.screen.blit(title_text, title_rect)
        
        # Difficulty tabs
        difficulties = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'INSANE']
        tab_width = 120
        tab_height = 40
        
        for i, diff in enumerate(difficulties):
            tab_x = self.screen_width // 2 - 300 + i * tab_width
            tab_y = self.screen_height // 2 - 150
            
            # Tab background
            tab_color = self.UI_HIGHLIGHT if diff == current_difficulty else self.UI_BG
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, tab_height)
            pygame.draw.rect(self.screen, tab_color, tab_rect)
            pygame.draw.rect(self.screen, self.UI_BORDER, tab_rect, 2)
            
            # Tab text
            tab_text = self.font_small.render(diff, True, self.WHITE)
            tab_text_rect = tab_text.get_rect(center=tab_rect.center)
            self.screen.blit(tab_text, tab_text_rect)
        
        # Display scores for current difficulty
        if current_difficulty in scores:
            score_list = scores[current_difficulty]
            y_start = self.screen_height // 2 - 80
            
            for i, entry in enumerate(score_list[:10]):  # Top 10
                y_pos = y_start + i * 35
                
                # Rank
                rank_text = self.font_small.render(f"{i+1:2d}.", True, self.NEON_YELLOW)
                self.screen.blit(rank_text, (self.screen_width // 2 - 350, y_pos))
                
                # Player name
                name_text = self.font_small.render(entry['player'][:15], True, self.WHITE)
                self.screen.blit(name_text, (self.screen_width // 2 - 300, y_pos))
                
                # Score
                score_text = self.font_small.render(f"{entry['score']:,}", True, self.NEON_GREEN)
                score_rect = score_text.get_rect(right=self.screen_width // 2 + 200)
                score_rect.y = y_pos
                self.screen.blit(score_text, score_rect)
                
                # Level and lines
                details_text = self.font_small.render(f"L{entry['level']} | {entry['lines']} lines", True, self.UI_HIGHLIGHT)
                details_rect = details_text.get_rect(right=self.screen_width // 2 + 320)
                details_rect.y = y_pos
                self.screen.blit(details_text, details_rect)
        
        # Instructions
        inst_text = self.font_small.render("Press 1-5 to switch difficulties, ESC to close", True, self.UI_HIGHLIGHT)
        inst_rect = inst_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 200))
        self.screen.blit(inst_text, inst_rect)
    
    def draw_pause_screen(self) -> None:
        """Draw fancy pause screen overlay."""
        # Create semi-transparent overlay with gradient
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(150)
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            r = int(0 + (20 - 0) * ratio)
            g = int(0 + (10 - 0) * ratio)
            b = int(0 + (30 - 0) * ratio)
            pygame.draw.line(overlay, (r, g, b), (0, y), (self.screen_width, y))
        self.screen.blit(overlay, (0, 0))
        
        # Draw fancy pause panel
        pause_panel_rect = pygame.Rect(
            self.screen_width // 2 - 200, 
            self.screen_height // 2 - 100, 
            400, 200
        )
        self._draw_fancy_panel(pause_panel_rect, "GAME PAUSED")
        
        # Pause text with glow effect
        pause_text = self.font_large.render("PAUSED", True, self.NEON_BLUE)
        text_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 20))
        self.screen.blit(pause_text, text_rect)
        
        # Resume instruction
        resume_text = self.font_medium.render("Press P to resume", True, self.UI_HIGHLIGHT)
        resume_rect = resume_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 30))
        self.screen.blit(resume_text, resume_rect)
    
    def draw_game_over_screen(self, final_score: int) -> None:
        """Draw fancy game over screen.
        
        Args:
            final_score: The final score achieved.
        """
        # Create dramatic overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            r = int(20 + (0 - 20) * ratio)
            g = int(10 + (0 - 10) * ratio)
            b = int(30 + (0 - 30) * ratio)
            pygame.draw.line(overlay, (r, g, b), (0, y), (self.screen_width, y))
        self.screen.blit(overlay, (0, 0))
        
        # Draw fancy game over panel
        game_over_panel_rect = pygame.Rect(
            self.screen_width // 2 - 250, 
            self.screen_height // 2 - 120, 
            500, 240
        )
        self._draw_fancy_panel(game_over_panel_rect, "GAME OVER")
        
        # Game Over text with dramatic effect
        game_over_text = self.font_large.render("GAME OVER", True, self.NEON_RED)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score with neon effect
        score_text = self.font_medium.render(f"FINAL SCORE: {final_score:,}", True, self.NEON_GREEN)
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 10))
        self.screen.blit(score_text, score_rect)
        
        # Restart instruction
        restart_text = self.font_small.render("Press R to restart or ESC to quit", True, self.UI_HIGHLIGHT)
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 40))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_game_mode_selection(self) -> None:
        """Draw game mode selection screen."""
        # Create overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw main panel
        main_panel_rect = pygame.Rect(
            self.screen_width // 2 - 300,
            self.screen_height // 2 - 150,
            600, 300
        )
        self._draw_fancy_panel(main_panel_rect, "SELECT GAME MODE")
        
        # Title
        title_text = self.font_large.render("CHOOSE YOUR MODE", True, self.NEON_BLUE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # Game mode options
        modes = [
            ("1 - SINGLE PLAYER", "Classic Tetris experience", self.NEON_GREEN),
            ("2 - MULTIPLAYER", "Play with friends locally", self.NEON_ORANGE)
        ]
        
        for i, (name, desc, color) in enumerate(modes):
            y_pos = self.screen_height // 2 - 30 + i * 60
            
            # Mode name
            name_text = self.font_medium.render(name, True, color)
            name_rect = name_text.get_rect(center=(self.screen_width // 2, y_pos))
            self.screen.blit(name_text, name_rect)
            
            # Description
            desc_text = self.font_small.render(desc, True, self.UI_HIGHLIGHT)
            desc_rect = desc_text.get_rect(center=(self.screen_width // 2, y_pos + 25))
            self.screen.blit(desc_text, desc_rect)
        
        # Instructions
        inst_text = self.font_small.render("Press 1 or 2 to select, H for high scores", True, self.UI_HIGHLIGHT)
        inst_rect = inst_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 120))
        self.screen.blit(inst_text, inst_rect)
    
    def draw_multiplayer_setup(self, selected_players: int, player_names: list, current_player_editing: int, selected_difficulty: int) -> None:
        """Draw multiplayer setup screen.
        
        Args:
            selected_players: Number of players selected (2-4).
            player_names: List of player names.
            current_player_editing: Index of currently editing player.
            selected_difficulty: Selected difficulty level.
        """
        # Create overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw main panel
        main_panel_rect = pygame.Rect(
            self.screen_width // 2 - 400,
            self.screen_height // 2 - 200,
            800, 400
        )
        self._draw_fancy_panel(main_panel_rect, "MULTIPLAYER SETUP")
        
        # Title
        title_text = self.font_large.render("MULTIPLAYER SETUP", True, self.NEON_BLUE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 150))
        self.screen.blit(title_text, title_rect)
        
        # Player count selection
        player_count_text = self.font_medium.render("Number of Players:", True, self.NEON_YELLOW)
        self.screen.blit(player_count_text, (self.screen_width // 2 - 350, self.screen_height // 2 - 100))
        
        for i in range(2, 5):
            x_pos = self.screen_width // 2 - 250 + (i - 2) * 80
            y_pos = self.screen_height // 2 - 100
            
            # Highlight selected
            if i == selected_players:
                pygame.draw.rect(self.screen, (50, 50, 100), (x_pos - 5, y_pos - 5, 70, 30))
            
            count_text = self.font_medium.render(f"{i}", True, self.NEON_GREEN if i == selected_players else self.UI_HIGHLIGHT)
            count_rect = count_text.get_rect(center=(x_pos + 30, y_pos + 10))
            self.screen.blit(count_text, count_rect)
        
        # Player names
        names_text = self.font_medium.render("Player Names:", True, self.NEON_YELLOW)
        self.screen.blit(names_text, (self.screen_width // 2 - 350, self.screen_height // 2 - 50))
        
        for i in range(selected_players):
            y_pos = self.screen_height // 2 - 20 + i * 30
            
            # Highlight currently editing
            if i == current_player_editing:
                pygame.draw.rect(self.screen, (50, 50, 100), (self.screen_width // 2 - 200, y_pos - 5, 300, 25))
            
            # Player label
            label_text = self.font_small.render(f"Player {i + 1}:", True, self.UI_HIGHLIGHT)
            self.screen.blit(label_text, (self.screen_width // 2 - 350, y_pos))
            
            # Name input
            name_text = self.font_small.render(player_names[i] + ("_" if i == current_player_editing else ""), True, self.WHITE)
            self.screen.blit(name_text, (self.screen_width // 2 - 200, y_pos))
        
        # Difficulty selection
        diff_text = self.font_medium.render("Difficulty:", True, self.NEON_YELLOW)
        self.screen.blit(diff_text, (self.screen_width // 2 - 350, self.screen_height // 2 + 80))
        
        difficulties = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'INSANE']
        for i, diff in enumerate(difficulties):
            x_pos = self.screen_width // 2 - 250 + i * 80
            y_pos = self.screen_height // 2 + 80
            
            # Highlight selected
            if i == selected_difficulty:
                pygame.draw.rect(self.screen, (50, 50, 100), (x_pos - 5, y_pos - 5, 70, 25))
            
            diff_text = self.font_small.render(diff, True, self.NEON_GREEN if i == selected_difficulty else self.UI_HIGHLIGHT)
            diff_rect = diff_text.get_rect(center=(x_pos + 35, y_pos + 7))
            self.screen.blit(diff_text, diff_rect)
        
        # Control instructions
        controls_text = self.font_small.render("CONTROLS:", True, self.NEON_YELLOW)
        self.screen.blit(controls_text, (self.screen_width // 2 - 350, self.screen_height // 2 + 120))
        
        # Player control schemes
        control_schemes = [
            ("Player 1: Arrow Keys + Z + Space + P", self.NEON_GREEN),
            ("Player 2: WASD + Q + E + T", self.NEON_BLUE),
            ("Player 3: IJKL + U + O + P", self.NEON_ORANGE),
            ("Player 4: Arrow Keys + Z + Space + P", self.NEON_PINK)
        ]
        
        for i, (scheme, color) in enumerate(control_schemes):
            y_pos = self.screen_height // 2 + 140 + i * 20
            scheme_text = self.font_small.render(scheme, True, color)
            self.screen.blit(scheme_text, (self.screen_width // 2 - 350, y_pos))
        
        # Instructions
        inst_text = self.font_small.render("1-3: Players | TAB: Difficulty | ↑↓: Edit names | ENTER: Start", True, self.UI_HIGHLIGHT)
        inst_rect = inst_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 240))
        self.screen.blit(inst_text, inst_rect)
    
    def draw_multiplayer_game(self, multiplayer_game) -> None:
        """Draw multiplayer game with multiple boards.
        
        Args:
            multiplayer_game: MultiplayerGame instance.
        """
        num_players = multiplayer_game.num_players
        player_states = multiplayer_game.get_player_states()
        
        # Calculate board positions
        if num_players == 2:
            board_width = 300
            board_height = 600
            board_spacing = 50
            start_x = (self.screen_width - (num_players * board_width + (num_players - 1) * board_spacing)) // 2
            
            for i, player in enumerate(player_states):
                board_x = start_x + i * (board_width + board_spacing)
                board_y = 50
                self._draw_player_board(player, board_x, board_y, board_width, board_height, i + 1)
        
        elif num_players == 3:
            # 2x2 grid with one empty space
            board_width = 250
            board_height = 500
            board_spacing = 30
            start_x = (self.screen_width - (2 * board_width + board_spacing)) // 2
            start_y = 50
            
            for i, player in enumerate(player_states):
                if i < 2:
                    board_x = start_x + i * (board_width + board_spacing)
                    board_y = start_y
                else:
                    board_x = start_x + board_width // 2
                    board_y = start_y + board_height + board_spacing
                
                self._draw_player_board(player, board_x, board_y, board_width, board_height, i + 1)
        
        else:  # 4 players
            # 2x2 grid
            board_width = 200
            board_height = 400
            board_spacing = 20
            start_x = (self.screen_width - (2 * board_width + board_spacing)) // 2
            start_y = 50
            
            for i, player in enumerate(player_states):
                row = i // 2
                col = i % 2
                board_x = start_x + col * (board_width + board_spacing)
                board_y = start_y + row * (board_height + board_spacing)
                self._draw_player_board(player, board_x, board_y, board_width, board_height, i + 1)
        
        # Draw control instructions at the bottom
        self._draw_multiplayer_controls(num_players)
        
        # Draw game over screen if all players are done
        if multiplayer_game.game_over:
            self._draw_multiplayer_game_over(multiplayer_game)
    
    def _draw_player_board(self, player_state: dict, x: int, y: int, width: int, height: int, player_id: int) -> None:
        """Draw a single player's board.
        
        Args:
            player_state: Player state dictionary.
            x: X position of board.
            y: Y position of board.
            width: Width of board area.
            height: Height of board area.
            player_id: Player number.
        """
        # Calculate cell size based on board dimensions
        cell_size = min(width // 10, height // 20)
        board_width = cell_size * 10
        board_height = cell_size * 20
        
        # Center the board in the allocated space
        board_x = x + (width - board_width) // 2
        board_y = y + (height - board_height) // 2
        
        # Draw player info
        info_y = y - 30
        name_text = self.font_small.render(f"Player {player_id}: {player_state['name']}", True, self.NEON_YELLOW)
        self.screen.blit(name_text, (x, info_y))
        
        score_text = self.font_small.render(f"Score: {player_state['score']:,}", True, self.NEON_GREEN)
        self.screen.blit(score_text, (x, info_y + 20))
        
        # Draw board background
        board_rect = pygame.Rect(board_x, board_y, board_width, board_height)
        pygame.draw.rect(self.screen, self.UI_BG, board_rect)
        pygame.draw.rect(self.screen, self.UI_BORDER, board_rect, 2)
        
        # Draw grid lines
        for i in range(11):
            line_x = board_x + i * cell_size
            pygame.draw.line(self.screen, (60, 60, 80), 
                           (line_x, board_y), (line_x, board_y + board_height), 1)
        
        for i in range(21):
            line_y = board_y + i * cell_size
            pygame.draw.line(self.screen, (60, 60, 80), 
                           (board_x, line_y), (board_x + board_width, line_y), 1)
        
        # Draw placed blocks
        for grid_y in range(20):
            for grid_x in range(10):
                color = player_state['board'].get_cell(grid_x, grid_y)
                if color:
                    cell_rect = pygame.Rect(
                        board_x + grid_x * cell_size + 1,
                        board_y + grid_y * cell_size + 1,
                        cell_size - 2,
                        cell_size - 2
                    )
                    pygame.draw.rect(self.screen, color, cell_rect)
                    pygame.draw.rect(self.screen, self.WHITE, cell_rect, 1)
        
        # Draw current piece
        if player_state['current_piece'] and not player_state['game_over']:
            piece = player_state['current_piece']
            blocks = piece.get_blocks()
            for block_x, block_y in blocks:
                if 0 <= block_x < 10 and 0 <= block_y < 20:
                    cell_rect = pygame.Rect(
                        board_x + block_x * cell_size + 1,
                        board_y + block_y * cell_size + 1,
                        cell_size - 2,
                        cell_size - 2
                    )
                    pygame.draw.rect(self.screen, piece.color, cell_rect)
                    pygame.draw.rect(self.screen, self.WHITE, cell_rect, 1)
        
        # Draw game over overlay
        if player_state['game_over']:
            overlay = pygame.Surface((board_width, board_height))
            overlay.set_alpha(128)
            overlay.fill(self.BLACK)
            self.screen.blit(overlay, (board_x, board_y))
            
            game_over_text = self.font_medium.render("GAME OVER", True, self.NEON_RED)
            text_rect = game_over_text.get_rect(center=(board_x + board_width // 2, board_y + board_height // 2))
            self.screen.blit(game_over_text, text_rect)
    
    def _draw_multiplayer_game_over(self, multiplayer_game) -> None:
        """Draw multiplayer game over screen.
        
        Args:
            multiplayer_game: MultiplayerGame instance.
        """
        # Create overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw main panel
        main_panel_rect = pygame.Rect(
            self.screen_width // 2 - 300,
            self.screen_height // 2 - 200,
            600, 400
        )
        self._draw_fancy_panel(main_panel_rect, "GAME OVER")
        
        # Title
        title_text = self.font_large.render("MULTIPLAYER GAME OVER", True, self.NEON_RED)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 150))
        self.screen.blit(title_text, title_rect)
        
        # Leaderboard
        leaderboard = multiplayer_game.get_leaderboard()
        leaderboard_text = self.font_medium.render("FINAL SCORES", True, self.NEON_YELLOW)
        leaderboard_rect = leaderboard_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
        self.screen.blit(leaderboard_text, leaderboard_rect)
        
        for i, player in enumerate(leaderboard):
            y_pos = self.screen_height // 2 - 60 + i * 30
            
            # Rank
            rank_text = self.font_small.render(f"{i+1}.", True, self.NEON_GREEN)
            self.screen.blit(rank_text, (self.screen_width // 2 - 200, y_pos))
            
            # Player name
            name_text = self.font_small.render(player['name'], True, self.WHITE)
            self.screen.blit(name_text, (self.screen_width // 2 - 150, y_pos))
            
            # Score
            score_text = self.font_small.render(f"{player['score']:,}", True, self.NEON_BLUE)
            score_rect = score_text.get_rect(right=self.screen_width // 2 + 150)
            score_rect.y = y_pos
            self.screen.blit(score_text, score_rect)
        
        # Instructions
        inst_text = self.font_small.render("Press R to restart or ESC to quit", True, self.UI_HIGHLIGHT)
        inst_rect = inst_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 120))
        self.screen.blit(inst_text, inst_rect)
    
    def _draw_multiplayer_controls(self, num_players: int) -> None:
        """Draw control instructions for multiplayer game.
        
        Args:
            num_players: Number of players in the game.
        """
        # Draw control panel at the bottom
        panel_y = self.screen_height - 120
        panel_rect = pygame.Rect(0, panel_y, self.screen_width, 120)
        
        # Semi-transparent background
        overlay = pygame.Surface((self.screen_width, 120))
        overlay.set_alpha(150)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, panel_y))
        
        # Title
        title_text = self.font_medium.render("CONTROLS", True, self.NEON_YELLOW)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, panel_y + 10))
        self.screen.blit(title_text, title_rect)
        
        # Control schemes for active players
        control_schemes = [
            ("P1: ←→↓↑ Z Space P", self.NEON_GREEN),
            ("P2: A D S W Q E T", self.NEON_BLUE),
            ("P3: J L K I U O P", self.NEON_ORANGE),
            ("P4: ←→↓↑ Z Space P", self.NEON_PINK)
        ]
        
        # Calculate spacing for controls
        controls_per_row = 2
        control_width = self.screen_width // controls_per_row
        control_height = 25
        
        for i in range(num_players):
            row = i // controls_per_row
            col = i % controls_per_row
            
            x_pos = col * control_width + 20
            y_pos = panel_y + 40 + row * control_height
            
            scheme, color = control_schemes[i]
            scheme_text = self.font_small.render(scheme, True, color)
            self.screen.blit(scheme_text, (x_pos, y_pos))
        
        # Global controls
        global_text = self.font_small.render("Global: 1-5 Difficulty | R Restart | ESC Menu", True, self.UI_HIGHLIGHT)
        global_rect = global_text.get_rect(center=(self.screen_width // 2, panel_y + 90))
        self.screen.blit(global_text, global_rect)
    
    def update_display(self) -> None:
        """Update the display."""
        pygame.display.flip()
