#!/usr/bin/env python3
"""
Textual Main Screen Prototype
==============================

Prototype of colony.sh main screen using Textual framework.
Demonstrates zero-flicker rendering with reactive game state updates.
"""

import sys
import os
import asyncio

# Add paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)  # For engine/
sys.path.insert(0, os.path.join(project_root, 'colony'))  # For content/

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Static, Label
from textual.reactive import reactive
from textual import work

# Import game engine
from engine import GameState
from content.loader import load_new_game


class ResourceDisplay(Static):
    """Widget displaying resources with generation rates."""

    resources = reactive({})

    def watch_resources(self, resources: dict) -> None:
        """Update display when resources change."""
        lines = []
        for name, res in resources.items():
            icon = res.metadata.get('icon', '⚙')
            amount = res.amount
            rate = res.generation_rate

            # Format with color based on rate
            rate_color = "green" if rate >= 0 else "red"
            rate_str = f"[{rate_color}]{rate:+.1f}/s[/{rate_color}]"

            line = f"{icon} {name.upper()}: {amount:.1f} {rate_str}"
            lines.append(line)

        self.update("\n".join(lines))


class BuildingDisplay(Static):
    """Widget displaying buildings and their counts."""

    buildings = reactive([])

    def watch_buildings(self, buildings: list) -> None:
        """Update display when buildings change."""
        if not buildings:
            self.update("No structures built")
            return

        lines = []
        for building in buildings:
            icon = building.metadata.get('icon', '⚒')
            name = building.display_name
            count = building.count

            # Show production info
            if building.produces:
                prod_str = ", ".join([f"+{v:.1f} {k}/s" for k, v in building.produces.items()])
                line = f"{icon} {name} x{count} [{prod_str}]"
            else:
                line = f"{icon} {name} x{count}"

            lines.append(line)

        self.update("\n".join(lines))


class EventLogDisplay(Static):
    """Widget displaying event log messages."""

    events = reactive([])

    def watch_events(self, events: list) -> None:
        """Update display when events change."""
        if not events:
            self.update("No events")
            return

        # Show last 5 events
        recent = events[-5:]
        lines = [f"[dim]Sol {e.get('sol', 0)}:[/dim] {e.get('message', '')}" for e in recent]
        self.update("\n".join(lines))


class GameStatsDisplay(Static):
    """Widget displaying game statistics."""

    stats = reactive({})

    def watch_stats(self, stats: dict) -> None:
        """Update display when stats change."""
        sol = stats.get('sol', 0)
        tick = stats.get('tick_count', 0)
        time_played = stats.get('total_playtime', 0)

        self.update(
            f"[cyan]Sol {sol}[/cyan]  "
            f"[dim]Tick {tick}[/dim]  "
            f"[dim]Time: {time_played:.1f}s[/dim]"
        )


class ColonyMainScreen(App):
    """Main game screen for colony.sh."""

    CSS = """
    Screen {
        background: $background;
    }

    #main_container {
        layout: vertical;
        height: 100%;
        padding: 1;
    }

    #stats_bar {
        height: 3;
        border: solid cyan;
        padding: 1;
    }

    #game_area {
        layout: horizontal;
        height: 1fr;
        margin-top: 1;
    }

    #left_panel {
        width: 1fr;
        border: solid green;
        padding: 1;
    }

    #right_panel {
        width: 1fr;
        border: solid yellow;
        padding: 1;
        margin-left: 1;
    }

    #event_log {
        height: 8;
        border: solid blue;
        padding: 1;
        margin-top: 1;
    }

    .panel_title {
        color: cyan;
        text-style: bold;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        ("b", "build", "Build"),
        ("r", "research", "Research"),
        ("i", "info", "Info"),
        ("s", "save", "Save"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.game_state: GameState = None
        self.event_list = []

    def compose(self) -> ComposeResult:
        """Create UI layout."""
        yield Header()

        with Vertical(id="main_container"):
            with Container(id="stats_bar"):
                yield GameStatsDisplay("", id="stats")

            with Horizontal(id="game_area"):
                with Vertical(id="left_panel"):
                    yield Label("RESOURCES", classes="panel_title")
                    yield ResourceDisplay("", id="resources")

                with Vertical(id="right_panel"):
                    yield Label("STRUCTURES", classes="panel_title")
                    yield BuildingDisplay("", id="buildings")

            with Container(id="event_log"):
                yield Label("EVENT LOG", classes="panel_title")
                yield EventLogDisplay("", id="events")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize game state and start game loop."""
        # Load game state
        self.game_state = load_new_game()

        # Add some test events
        self.event_list = [
            {"sol": 0, "message": "Colony initialization sequence started"},
            {"sol": 0, "message": "Solar Array online"},
            {"sol": 0, "message": "Hab Module pressurized"},
            {"sol": 0, "message": "3 colonists awake from cryo-sleep"},
        ]

        # Start game loop
        self.run_game_loop()

        # Initial UI update
        self.update_ui()

    @work(exclusive=True)
    async def run_game_loop(self) -> None:
        """Game loop that updates state at tick rate."""
        tick_interval = 0.1  # 10 ticks per second

        while True:
            await asyncio.sleep(tick_interval)

            # Update game state
            if self.game_state:
                self.game_state.update(tick_interval)
                self.update_ui()

    def update_ui(self) -> None:
        """Update all UI widgets with current game state."""
        if not self.game_state:
            return

        # Update stats
        stats_widget = self.query_one("#stats", GameStatsDisplay)
        stats_widget.stats = {
            'sol': self.game_state.metadata.get('sol', 0),
            'tick_count': self.game_state.metadata.get('tick_count', 0),
            'total_playtime': self.game_state.metadata.get('total_playtime', 0),
        }

        # Update resources
        resource_widget = self.query_one("#resources", ResourceDisplay)
        resource_widget.resources = self.game_state.resources.resources

        # Update buildings
        building_widget = self.query_one("#buildings", BuildingDisplay)
        building_widget.buildings = self.game_state.buildings.get_owned_buildings()

        # Update event log
        event_widget = self.query_one("#events", EventLogDisplay)
        event_widget.events = self.event_list

    def action_build(self) -> None:
        """Build menu placeholder."""
        self.notify("Build menu - not implemented in prototype")

    def action_research(self) -> None:
        """Research menu placeholder."""
        self.notify("Research menu - not implemented in prototype")

    def action_info(self) -> None:
        """Info screen placeholder."""
        self.notify("Info screen - not implemented in prototype")

    def action_save(self) -> None:
        """Save game placeholder."""
        self.notify("Save game - not implemented in prototype")


def main():
    """Run the prototype."""
    app = ColonyMainScreen()
    app.run()


if __name__ == "__main__":
    main()
