"""
Animator Module
================

ASCII animation utilities for terminal games.
Handles spinners, blinking text, frame animations, and visual effects.

Classes:
    Animation: Frame-based animation
    Animator: Animation management system

Usage:
    animator = Animator()
    spinner = animator.create_spinner('dots')
    animator.update(delta_time=0.1)
    frame = animator.get_frame(spinner)
"""

import logging
import time
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class AnimationType(Enum):
    """Animation types."""
    LOOP = 'loop'          # Continuous loop
    ONCE = 'once'          # Play once and stop
    PINGPONG = 'pingpong'  # Loop back and forth
    BLINK = 'blink'        # On/off toggle


@dataclass
class Animation:
    """
    Represents an animation sequence.

    Attributes:
        name (str): Animation name
        frames (List[str]): Animation frames
        frame_duration (float): Duration per frame in seconds
        animation_type (AnimationType): Animation behavior
        current_frame (int): Current frame index
        elapsed (float): Time elapsed in current frame
        active (bool): Whether animation is playing
        reverse (bool): Reverse playback (for pingpong)
    """
    name: str
    frames: List[str]
    frame_duration: float = 0.1
    animation_type: AnimationType = AnimationType.LOOP
    current_frame: int = 0
    elapsed: float = 0.0
    active: bool = True
    reverse: bool = False

    def get_current_frame(self) -> str:
        """
        Get current animation frame.

        Returns:
            str: Current frame text
        """
        if not self.frames:
            return ""

        if not self.active and self.animation_type == AnimationType.ONCE:
            return self.frames[-1]

        return self.frames[self.current_frame]

    def update(self, delta_time: float):
        """
        Update animation state.

        Args:
            delta_time: Time elapsed since last update
        """
        if not self.active:
            return

        self.elapsed += delta_time

        if self.elapsed >= self.frame_duration:
            self.elapsed = 0

            if self.animation_type == AnimationType.LOOP:
                self.current_frame = (self.current_frame + 1) % len(self.frames)

            elif self.animation_type == AnimationType.ONCE:
                if self.current_frame < len(self.frames) - 1:
                    self.current_frame += 1
                else:
                    self.active = False

            elif self.animation_type == AnimationType.PINGPONG:
                if self.reverse:
                    self.current_frame -= 1
                    if self.current_frame <= 0:
                        self.current_frame = 0
                        self.reverse = False
                else:
                    self.current_frame += 1
                    if self.current_frame >= len(self.frames) - 1:
                        self.current_frame = len(self.frames) - 1
                        self.reverse = True

            elif self.animation_type == AnimationType.BLINK:
                self.current_frame = 1 - self.current_frame  # Toggle 0/1

    def reset(self):
        """Reset animation to start."""
        self.current_frame = 0
        self.elapsed = 0.0
        self.active = True
        self.reverse = False


class Animator:
    """
    Manages multiple animations.

    Attributes:
        animations (Dict[str, Animation]): Active animations
        presets (Dict[str, List[str]]): Preset animation frames
    """

    # Preset animations
    SPINNERS = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'line': ['|', '/', '-', '\\'],
        'arrow': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'circle': ['◐', '◓', '◑', '◒'],
        'square': ['◰', '◳', '◲', '◱'],
        'pulse': ['·', '•', '●', '•'],
        'toggle': ['◻', '◼'],
        'clock': ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛'],
    }

    PROGRESS_BARS = {
        'blocks': ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█'],
        'dots': ['⣀', '⣄', '⣤', '⣦', '⣶', '⣷', '⣿'],
        'arrows': ['▹', '▸', '▹▸', '▸▹', '▹▸▹'],
    }

    EFFECTS = {
        'sparkle': ['✦', '✧', '✨', '✧', '✦'],
        'star': ['☆', '★', '☆'],
        'heart': ['♡', '♥', '♡'],
        'fire': ['🔥', '🔶', '🔥'],
        'wave': ['~', '≈', '~', '≈'],
    }

    def __init__(self):
        """Initialize the animator."""
        self.animations: Dict[str, Animation] = {}
        logger.info("Animator initialized")

    def create_animation(
        self,
        name: str,
        frames: List[str],
        frame_duration: float = 0.1,
        animation_type: AnimationType = AnimationType.LOOP
    ) -> Animation:
        """
        Create a new animation.

        Args:
            name: Animation identifier
            frames: List of frame strings
            frame_duration: Duration per frame
            animation_type: Animation behavior

        Returns:
            Animation: The created animation

        Raises:
            ValueError: If animation name already exists
        """
        if name in self.animations:
            raise ValueError(f"Animation '{name}' already exists")

        animation = Animation(
            name=name,
            frames=frames,
            frame_duration=frame_duration,
            animation_type=animation_type
        )

        self.animations[name] = animation
        logger.debug(f"Animation created: {name} ({len(frames)} frames)")
        return animation

    def create_spinner(
        self,
        name: str,
        style: str = 'dots',
        frame_duration: float = 0.1
    ) -> Animation:
        """
        Create a spinner animation from preset.

        Args:
            name: Animation identifier
            style: Spinner style ('dots', 'line', 'arrow', etc.)
            frame_duration: Duration per frame

        Returns:
            Animation: The created spinner
        """
        if style not in self.SPINNERS:
            style = 'dots'

        return self.create_animation(
            name=name,
            frames=self.SPINNERS[style],
            frame_duration=frame_duration,
            animation_type=AnimationType.LOOP
        )

    def create_blink(
        self,
        name: str,
        text: str,
        blink_duration: float = 0.5
    ) -> Animation:
        """
        Create a blinking text animation.

        Args:
            name: Animation identifier
            text: Text to blink
            blink_duration: Blink interval

        Returns:
            Animation: The created blink animation
        """
        return self.create_animation(
            name=name,
            frames=[text, ''],
            frame_duration=blink_duration,
            animation_type=AnimationType.BLINK
        )

    def create_text_sequence(
        self,
        name: str,
        texts: List[str],
        frame_duration: float = 1.0,
        loop: bool = True
    ) -> Animation:
        """
        Create a text sequence animation.

        Args:
            name: Animation identifier
            texts: List of text strings
            frame_duration: Duration per text
            loop: Whether to loop

        Returns:
            Animation: The created animation
        """
        anim_type = AnimationType.LOOP if loop else AnimationType.ONCE

        return self.create_animation(
            name=name,
            frames=texts,
            frame_duration=frame_duration,
            animation_type=anim_type
        )

    def get_animation(self, name: str) -> Optional[Animation]:
        """
        Get an animation by name.

        Args:
            name: Animation identifier

        Returns:
            Animation or None: The animation if found
        """
        return self.animations.get(name)

    def get_frame(self, name: str) -> str:
        """
        Get current frame of an animation.

        Args:
            name: Animation identifier

        Returns:
            str: Current frame, or empty string if not found
        """
        animation = self.get_animation(name)
        return animation.get_current_frame() if animation else ""

    def update(self, delta_time: float):
        """
        Update all animations.

        Args:
            delta_time: Time elapsed since last update
        """
        for animation in self.animations.values():
            animation.update(delta_time)

    def reset_animation(self, name: str):
        """
        Reset an animation to start.

        Args:
            name: Animation identifier
        """
        animation = self.get_animation(name)
        if animation:
            animation.reset()

    def stop_animation(self, name: str):
        """
        Stop an animation.

        Args:
            name: Animation identifier
        """
        animation = self.get_animation(name)
        if animation:
            animation.active = False

    def start_animation(self, name: str):
        """
        Start/resume an animation.

        Args:
            name: Animation identifier
        """
        animation = self.get_animation(name)
        if animation:
            animation.active = True

    def remove_animation(self, name: str):
        """
        Remove an animation.

        Args:
            name: Animation identifier
        """
        if name in self.animations:
            del self.animations[name]
            logger.debug(f"Animation removed: {name}")

    def clear_animations(self):
        """Clear all animations."""
        self.animations.clear()
        logger.info("All animations cleared")

    @staticmethod
    def create_loading_bar(
        current: float,
        maximum: float,
        width: int = 20,
        filled: str = '█',
        empty: str = '░'
    ) -> str:
        """
        Create a static progress bar.

        Args:
            current: Current value
            maximum: Maximum value
            width: Bar width
            filled: Filled character
            empty: Empty character

        Returns:
            str: Progress bar string
        """
        if maximum == 0:
            percentage = 0
        else:
            percentage = min(100, (current / maximum) * 100)

        filled_width = int((percentage / 100) * width)
        empty_width = width - filled_width

        return filled * filled_width + empty * empty_width

    @staticmethod
    def animate_number(
        start: float,
        end: float,
        progress: float
    ) -> float:
        """
        Interpolate between two numbers.

        Args:
            start: Start value
            end: End value
            progress: Progress (0.0 to 1.0)

        Returns:
            float: Interpolated value
        """
        progress = max(0.0, min(1.0, progress))
        return start + (end - start) * progress

    @staticmethod
    def create_marquee(
        text: str,
        width: int,
        position: int
    ) -> str:
        """
        Create a scrolling marquee effect.

        Args:
            text: Text to scroll
            width: Display width
            position: Scroll position

        Returns:
            str: Visible portion of text
        """
        # Add spacing
        full_text = text + "  " * 5

        # Calculate visible portion
        position = position % len(full_text)
        visible = (full_text + full_text)[position:position + width]

        return visible.ljust(width)


# Example usage
if __name__ == "__main__":
    import sys
    import time

    animator = Animator()

    # Create various animations
    spinner = animator.create_spinner('loading', style='dots', frame_duration=0.1)
    blink = animator.create_blink('alert', '⚠️ WARNING', blink_duration=0.5)
    progress = animator.create_text_sequence(
        'status',
        ['Initializing...', 'Loading assets...', 'Starting game...', 'Ready!'],
        frame_duration=1.0,
        loop=False
    )

    print("=== ANIMATOR DEMO ===\n")

    # Run animation demo
    start_time = time.time()
    last_update = start_time

    print("Running animations for 5 seconds...\n")

    while time.time() - start_time < 5:
        current_time = time.time()
        delta_time = current_time - last_update
        last_update = current_time

        # Update animations
        animator.update(delta_time)

        # Display
        spinner_frame = animator.get_frame('loading')
        blink_frame = animator.get_frame('alert')
        status_frame = animator.get_frame('status')

        # Clear line and print
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        sys.stdout.write(f"{spinner_frame} {status_frame} {blink_frame}")
        sys.stdout.flush()

        time.sleep(0.05)

    print("\n\n=== STATIC EFFECTS ===\n")

    # Progress bar demo
    for i in range(0, 101, 10):
        bar = Animator.create_loading_bar(i, 100, width=30)
        print(f"Progress: [{bar}] {i}%")

    # Marquee demo
    print("\n=== MARQUEE ===\n")
    marquee_text = "Welcome to the Incremental Game Engine!"

    for pos in range(30):
        marquee = Animator.create_marquee(marquee_text, width=40, position=pos)
        sys.stdout.write('\r' + marquee)
        sys.stdout.flush()
        time.sleep(0.1)

    print("\n\nDemo complete!")
