"""Audio system for Escape the Dungeon of Doom."""

import logging
from typing import Optional

import pygame


class AudioSystem:
    """Audio system with graceful degradation for missing audio files."""

    def __init__(self) -> None:
        """Initialize the audio system."""
        self._music_playing = False
        self._music_paused = False
        self._sound_enabled = True
        self._music_volume = 0.7
        self._sfx_volume = 0.5
        self._initialized = False

        try:
            if pygame.mixer is not None:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                self._initialized = True
                logging.info("AudioSystem initialized successfully")
            else:
                logging.warning("pygame.mixer not available - audio disabled")
        except Exception as e:
            logging.warning(f"Failed to initialize audio: {e}")
            self._initialized = False

    def play_music(self, music_file: str, loop: bool = True) -> None:
        """Play background music.

        Args:
            music_file: Path to the music file.
            loop: Whether to loop the music (default True).
        """
        if not self._initialized:
            return

        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(self._music_volume)
            pygame.mixer.music.play(-1 if loop else 0)
            self._music_playing = True
            self._music_paused = False
            logging.debug(f"Playing music: {music_file}")
        except Exception as e:
            logging.debug(f"Could not play music {music_file}: {e}")

    def stop_music(self) -> None:
        """Stop the current music."""
        if not self._initialized:
            return

        try:
            pygame.mixer.music.stop()
            self._music_playing = False
            self._music_paused = False
            logging.debug("Music stopped")
        except Exception as e:
            logging.debug(f"Could not stop music: {e}")

    def pause_music(self) -> None:
        """Pause the current music."""
        if not self._initialized or not self._music_playing:
            return

        try:
            pygame.mixer.music.pause()
            self._music_paused = True
            logging.debug("Music paused")
        except Exception as e:
            logging.debug(f"Could not pause music: {e}")

    def resume_music(self) -> None:
        """Resume the paused music."""
        if not self._initialized or not self._music_paused:
            return

        try:
            pygame.mixer.music.unpause()
            self._music_paused = False
            logging.debug("Music resumed")
        except Exception as e:
            logging.debug(f"Could not resume music: {e}")

    def play_sound(self, sound_name: str) -> None:
        """Play a sound effect.

        Args:
            sound_name: Name of the sound to play.
        """
        if not self._initialized or not self._sound_enabled:
            return

        sound_map = {
            "attack": "attack.ogg",
            "hit": "hit.ogg",
            "pickup": "pickup.ogg",
            "door_open": "door_open.ogg",
        }

        sound_file = sound_map.get(sound_name)
        if sound_file:
            try:
                sound = pygame.mixer.Sound(sound_file)
                sound.set_volume(self._sfx_volume)
                sound.play()
                logging.debug(f"Playing sound: {sound_name}")
            except Exception as e:
                logging.debug(f"Could not play sound {sound_name}: {e}")

    def set_volume(
        self, music_volume: Optional[float] = None, sfx_volume: Optional[float] = None
    ) -> None:
        """Set the volume levels.

        Args:
            music_volume: Music volume (0.0 to 1.0).
            sfx_volume: SFX volume (0.0 to 1.0).
        """
        if music_volume is not None:
            self._music_volume = max(0.0, min(1.0, music_volume))
            if self._initialized:
                pygame.mixer.music.set_volume(self._music_volume)

        if sfx_volume is not None:
            self._sfx_volume = max(0.0, min(1.0, sfx_volume))

    def is_initialized(self) -> bool:
        """Check if audio system is initialized.

        Returns:
            True if audio is available, False otherwise.
        """
        return self._initialized

    def is_music_playing(self) -> bool:
        """Check if music is currently playing.

        Returns:
            True if music is playing, False otherwise.
        """
        return self._music_playing and not self._music_paused
