#!/usr/bin/env python3
"""
Textual Hello World Test
========================

Simple test to validate Textual installation and basic functionality.
Tests:
- App creation and rendering
- Worker for game loop simulation
- Reactive variables for auto-updating display
"""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static, Label
from textual.reactive import reactive
from textual import work
import asyncio


class GameDisplay(Static):
    """Widget that displays game state."""

    counter = reactive(0)

    def watch_counter(self, counter: int) -> None:
        """Update display when counter changes."""
        self.update(f"Counter: {counter}")


class HelloWorldApp(App):
    """A simple Textual app with a game loop."""

    CSS = """
    Screen {
        align: center middle;
    }

    Container {
        width: 60;
        height: 15;
        border: solid green;
        padding: 2;
    }

    #title {
        text-align: center;
        color: cyan;
        text-style: bold;
    }

    #counter {
        text-align: center;
        color: yellow;
        margin-top: 2;
    }

    #status {
        text-align: center;
        color: green;
        margin-top: 2;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        with Container():
            yield Label("Textual Hello World Test", id="title")
            yield GameDisplay("Counter: 0", id="counter")
            yield Label("Game loop running...", id="status")
        yield Footer()

    def on_mount(self) -> None:
        """Start game loop when app mounts."""
        self.run_game_loop()

    @work(exclusive=True)
    async def run_game_loop(self) -> None:
        """Simulate a game loop that updates every second."""
        counter_widget = self.query_one("#counter", GameDisplay)

        for i in range(1, 11):
            await asyncio.sleep(1.0)  # Wait 1 second
            counter_widget.counter = i

        # Update status when done
        status_widget = self.query_one("#status", Label)
        status_widget.update("Game loop complete! Press 'q' to quit.")


def main():
    """Run the hello world test."""
    app = HelloWorldApp()
    app.run()


if __name__ == "__main__":
    main()
