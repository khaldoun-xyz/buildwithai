"""Audio system for Tetris game."""

import pygame
import os
from typing import Optional


class AudioManager:
    """Manages all audio for the Tetris game."""
    
    def __init__(self):
        """Initialize the audio manager."""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.audio_enabled = True
        except pygame.error:
            self.audio_enabled = False
        
        self.sounds = {}
        self.music_playing = False
        self.volume = 0.7
        
        # Create basic sound effects (simplified)
        self._create_sounds()
    
    def _create_sounds(self) -> None:
        """Create basic sound effects."""
        if not self.audio_enabled:
            return
        
        # Create simple placeholder sounds
        # In a real implementation, you would load actual sound files
        # For now, we'll just create empty sound objects
        try:
            # Create minimal sound effects
            self.sounds['line_clear'] = None
            self.sounds['tetris'] = None
            self.sounds['placement'] = None
            self.sounds['rotation'] = None
            self.sounds['game_over'] = None
        except Exception:
            # If sound creation fails, disable audio
            self.audio_enabled = False
    
    def play_sound(self, sound_name: str) -> None:
        """Play a sound effect.
        
        Args:
            sound_name: Name of the sound to play.
        """
        if not self.audio_enabled:
            return
        
        if sound_name in self.sounds and self.sounds[sound_name] is not None:
            try:
                sound = self.sounds[sound_name]
                sound.set_volume(self.volume)
                sound.play()
            except Exception:
                # If sound playback fails, continue silently
                pass
    
    def play_line_clear(self, lines_cleared: int) -> None:
        """Play appropriate sound for line clearing.
        
        Args:
            lines_cleared: Number of lines cleared.
        """
        if lines_cleared == 4:
            self.play_sound('tetris')
        elif lines_cleared > 0:
            self.play_sound('line_clear')
    
    def play_placement(self) -> None:
        """Play block placement sound."""
        self.play_sound('placement')
    
    def play_rotation(self) -> None:
        """Play rotation sound."""
        self.play_sound('rotation')
    
    def play_game_over(self) -> None:
        """Play game over sound."""
        self.play_sound('game_over')
    
    def start_music(self) -> None:
        """Start background music (placeholder)."""
        # In a real implementation, you would load and play background music
        # For now, we'll just set a flag
        self.music_playing = True
    
    def stop_music(self) -> None:
        """Stop background music."""
        if self.audio_enabled:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        self.music_playing = False
    
    def set_volume(self, volume: float) -> None:
        """Set the volume for all sounds.
        
        Args:
            volume: Volume level (0.0 to 1.0).
        """
        self.volume = max(0.0, min(1.0, volume))
        if self.audio_enabled:
            try:
                pygame.mixer.music.set_volume(self.volume)
            except Exception:
                pass
    
    def toggle_mute(self) -> None:
        """Toggle mute state."""
        if self.volume > 0:
            self.old_volume = self.volume
            self.set_volume(0.0)
        else:
            self.set_volume(getattr(self, 'old_volume', 0.7))
    
    def cleanup(self) -> None:
        """Clean up audio resources."""
        if self.audio_enabled:
            try:
                pygame.mixer.quit()
            except Exception:
                pass
