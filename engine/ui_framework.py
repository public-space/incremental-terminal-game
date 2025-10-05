"""
UI Framework Module
===================

Terminal rendering framework for text-based games.
Handles colors, layouts, panels, and screen management.

Classes:
    Color: ANSI color codes and formatting
    Panel: Bordered panel for organizing content
    UIFramework: Main UI rendering system

Usage:
    ui = UIFramework()
    ui.clear_screen()
    ui.print_colored("Hello!", Color.GREEN)
    panel = Panel("Title", width=40, border_style="double")
    ui.render_panel(panel, content)
"""

import logging
import os
import sys
import shutil
from typing import List, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class Color:
    """
    ANSI color codes for terminal output.

    Attributes:
        Reset, color codes, and text styles
    """
    # Reset
    RESET = '\033[0m'

    # Regular colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    # Text styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'

    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        """
        Create RGB color code (256-color mode).

        Args:
            r: Red (0-255)
            g: Green (0-255)
            b: Blue (0-255)

        Returns:
            str: ANSI color code
        """
        return f'\033[38;2;{r};{g};{b}m'

    @staticmethod
    def bg_rgb(r: int, g: int, b: int) -> str:
        """
        Create RGB background color code.

        Args:
            r: Red (0-255)
            g: Green (0-255)
            b: Blue (0-255)

        Returns:
            str: ANSI background color code
        """
        return f'\033[48;2;{r};{g};{b}m'


class BorderStyle(Enum):
    """Border styles for panels."""
    SINGLE = 'single'
    DOUBLE = 'double'
    ROUNDED = 'rounded'
    BOLD = 'bold'
    ASCII = 'ascii'


class Panel:
    """
    A bordered panel for organizing content.

    Attributes:
        title (str): Panel title
        width (int): Panel width in characters
        border_style (str): Border style ('single', 'double', 'rounded', 'bold', 'ascii')
        title_color (str): Color code for title
        border_color (str): Color code for border
    """

    BORDERS = {
        'single': {
            'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘',
            'h': '─', 'v': '│', 't': '┬', 'b': '┴', 'l': '├', 'r': '┤', 'c': '┼'
        },
        'double': {
            'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝',
            'h': '═', 'v': '║', 't': '╦', 'b': '╩', 'l': '╠', 'r': '╣', 'c': '╬'
        },
        'rounded': {
            'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯',
            'h': '─', 'v': '│', 't': '┬', 'b': '┴', 'l': '├', 'r': '┤', 'c': '┼'
        },
        'bold': {
            'tl': '┏', 'tr': '┓', 'bl': '┗', 'br': '┛',
            'h': '━', 'v': '┃', 't': '┳', 'b': '┻', 'l': '┣', 'r': '┫', 'c': '╋'
        },
        'ascii': {
            'tl': '+', 'tr': '+', 'bl': '+', 'br': '+',
            'h': '-', 'v': '|', 't': '+', 'b': '+', 'l': '+', 'r': '+', 'c': '+'
        }
    }

    def __init__(
        self,
        title: str = "",
        width: int = 60,
        border_style: str = 'single',
        title_color: str = Color.BRIGHT_CYAN,
        border_color: str = Color.CYAN
    ):
        """
        Initialize a panel.

        Args:
            title: Panel title
            width: Panel width
            border_style: Border style name
            title_color: ANSI color code for title
            border_color: ANSI color code for border
        """
        self.title = title
        self.width = width
        self.border_style = border_style
        self.title_color = title_color
        self.border_color = border_color
        self.borders = self.BORDERS.get(border_style, self.BORDERS['single'])

    def render_top(self) -> str:
        """
        Render top border with title.

        Returns:
            str: Top border line
        """
        b = self.borders

        if self.title:
            title_text = f" {self.title} "
            title_len = len(title_text)
            remaining = self.width - title_len - 2

            if remaining < 0:
                title_text = title_text[:self.width - 4] + ".. "
                remaining = 0

            left_border = b['h'] * 1
            right_border = b['h'] * remaining

            line = (f"{self.border_color}{b['tl']}{left_border}"
                   f"{self.title_color}{title_text}"
                   f"{self.border_color}{right_border}{b['tr']}{Color.RESET}")
        else:
            line = f"{self.border_color}{b['tl']}{b['h'] * (self.width - 2)}{b['tr']}{Color.RESET}"

        return line

    def render_bottom(self) -> str:
        """
        Render bottom border.

        Returns:
            str: Bottom border line
        """
        b = self.borders
        return f"{self.border_color}{b['bl']}{b['h'] * (self.width - 2)}{b['br']}{Color.RESET}"

    def render_line(self, content: str, align: str = 'left') -> str:
        """
        Render a content line with side borders.

        Args:
            content: Line content
            align: Text alignment ('left', 'center', 'right')

        Returns:
            str: Bordered line
        """
        b = self.borders

        # Remove color codes for length calculation
        import re
        content_plain = re.sub(r'\033\[[0-9;]+m', '', content)
        content_len = len(content_plain)

        available_width = self.width - 4  # Account for borders and padding

        if content_len > available_width:
            # Truncate if too long
            content = content[:available_width - 2] + ".."
            padding = ""
        else:
            padding_len = available_width - content_len

            if align == 'center':
                left_pad = padding_len // 2
                right_pad = padding_len - left_pad
                padding_left = " " * left_pad
                padding_right = " " * right_pad
                content = f"{padding_left}{content}{padding_right}"
                padding = ""
            elif align == 'right':
                padding = " " * padding_len
                content = f"{padding}{content}"
                padding = ""
            else:  # left
                padding = " " * padding_len

        return f"{self.border_color}{b['v']}{Color.RESET} {content}{padding} {self.border_color}{b['v']}{Color.RESET}"

    def render_divider(self) -> str:
        """
        Render a horizontal divider.

        Returns:
            str: Divider line
        """
        b = self.borders
        return f"{self.border_color}{b['l']}{b['h'] * (self.width - 2)}{b['r']}{Color.RESET}"


class UIFramework:
    """
    Main UI framework for terminal rendering.

    Attributes:
        width (int): Terminal width
        height (int): Terminal height
        use_colors (bool): Whether to use ANSI colors
    """

    def __init__(self, use_colors: bool = True):
        """
        Initialize the UI framework.

        Args:
            use_colors: Enable ANSI color codes
        """
        self.use_colors = use_colors
        self.width, self.height = self.get_terminal_size()
        logger.info(f"UIFramework initialized (terminal: {self.width}x{self.height})")

    @staticmethod
    def get_terminal_size() -> Tuple[int, int]:
        """
        Get terminal dimensions.

        Returns:
            tuple: (width, height) in characters
        """
        try:
            size = shutil.get_terminal_size()
            return size.columns, size.lines
        except Exception:
            return 80, 24  # Default fallback

    def clear_screen(self):
        """Clear the terminal screen using ANSI escape sequences."""
        # Use ANSI escape codes instead of os.system() to reduce flicker
        # \033[H moves cursor to 0,0
        # \033[2J clears entire screen
        print('\033[H\033[2J', end='', flush=True)
        logger.debug("Screen cleared")

    def move_cursor(self, x: int, y: int):
        """
        Move cursor to position.

        Args:
            x: Column (0-based)
            y: Row (0-based)
        """
        print(f'\033[{y + 1};{x + 1}H', end='')

    def hide_cursor(self):
        """Hide the terminal cursor."""
        print('\033[?25l', end='')

    def show_cursor(self):
        """Show the terminal cursor."""
        print('\033[?25h', end='')

    def print_colored(self, text: str, color: str = "", style: str = "", end: str = '\n'):
        """
        Print colored text.

        Args:
            text: Text to print
            color: ANSI color code
            style: ANSI style code
            end: Line ending
        """
        if self.use_colors:
            print(f"{style}{color}{text}{Color.RESET}", end=end)
        else:
            print(text, end=end)

    def print_centered(self, text: str, width: Optional[int] = None, color: str = ""):
        """
        Print centered text.

        Args:
            text: Text to center
            width: Width to center within (default: terminal width)
            color: ANSI color code
        """
        if width is None:
            width = self.width

        padding = (width - len(text)) // 2
        centered = " " * padding + text
        self.print_colored(centered, color=color)

    def print_bar(
        self,
        current: float,
        maximum: float,
        width: int = 20,
        filled_char: str = '█',
        empty_char: str = '░',
        show_percentage: bool = True,
        color: str = Color.GREEN
    ) -> str:
        """
        Create a progress bar.

        Args:
            current: Current value
            maximum: Maximum value
            width: Bar width in characters
            filled_char: Character for filled portion
            empty_char: Character for empty portion
            show_percentage: Show percentage text
            color: Bar color

        Returns:
            str: Formatted progress bar
        """
        if maximum == 0:
            percentage = 0
        else:
            percentage = min(100, (current / maximum) * 100)

        filled_width = int((percentage / 100) * width)
        empty_width = width - filled_width

        bar = f"{color}{filled_char * filled_width}{Color.DIM}{empty_char * empty_width}{Color.RESET}"

        if show_percentage:
            bar += f" {percentage:.0f}%"

        return bar

    def render_panel(self, panel: Panel, lines: List[str], align: str = 'left'):
        """
        Render a panel with content.

        Args:
            panel: Panel to render
            lines: Content lines
            align: Text alignment
        """
        print(panel.render_top())

        for line in lines:
            print(panel.render_line(line, align=align))

        print(panel.render_bottom())

    def render_table(
        self,
        headers: List[str],
        rows: List[List[str]],
        column_widths: Optional[List[int]] = None,
        border_style: str = 'single'
    ):
        """
        Render a table.

        Args:
            headers: Column headers
            rows: Table rows
            column_widths: Width for each column (auto if None)
            border_style: Border style
        """
        if column_widths is None:
            # Calculate column widths
            column_widths = []
            for i, header in enumerate(headers):
                max_width = len(header)
                for row in rows:
                    if i < len(row):
                        max_width = max(max_width, len(str(row[i])))
                column_widths.append(max_width + 2)

        borders = Panel.BORDERS[border_style]

        # Top border
        top = borders['tl']
        for i, width in enumerate(column_widths):
            top += borders['h'] * width
            if i < len(column_widths) - 1:
                top += borders['t']
        top += borders['tr']
        print(f"{Color.CYAN}{top}{Color.RESET}")

        # Headers
        header_line = f"{Color.CYAN}{borders['v']}{Color.RESET}"
        for i, (header, width) in enumerate(zip(headers, column_widths)):
            padded = f" {header}".ljust(width)
            header_line += f"{Color.BOLD}{Color.BRIGHT_CYAN}{padded}{Color.RESET}"
            header_line += f"{Color.CYAN}{borders['v']}{Color.RESET}"
        print(header_line)

        # Header divider
        divider = borders['l']
        for i, width in enumerate(column_widths):
            divider += borders['h'] * width
            if i < len(column_widths) - 1:
                divider += borders['c']
        divider += borders['r']
        print(f"{Color.CYAN}{divider}{Color.RESET}")

        # Rows
        for row in rows:
            row_line = f"{Color.CYAN}{borders['v']}{Color.RESET}"
            for i, width in enumerate(column_widths):
                cell = str(row[i]) if i < len(row) else ""
                padded = f" {cell}".ljust(width)
                row_line += f"{padded}"
                row_line += f"{Color.CYAN}{borders['v']}{Color.RESET}"
            print(row_line)

        # Bottom border
        bottom = borders['bl']
        for i, width in enumerate(column_widths):
            bottom += borders['h'] * width
            if i < len(column_widths) - 1:
                bottom += borders['b']
        bottom += borders['br']
        print(f"{Color.CYAN}{bottom}{Color.RESET}")

    def print_separator(self, char: str = '─', color: str = Color.CYAN):
        """
        Print a full-width separator line.

        Args:
            char: Character to use
            color: Line color
        """
        self.print_colored(char * self.width, color=color)

    def format_number(self, num: float, decimals: int = 1) -> str:
        """
        Format number with K/M/B suffixes.

        Args:
            num: Number to format
            decimals: Decimal places

        Returns:
            str: Formatted number
        """
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.{decimals}f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.{decimals}f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.{decimals}f}K"
        else:
            return f"{num:.{decimals}f}"

    def input_prompt(self, prompt: str, color: str = Color.BRIGHT_YELLOW) -> str:
        """
        Display input prompt with color.

        Args:
            prompt: Prompt text
            color: Prompt color

        Returns:
            str: User input
        """
        if self.use_colors:
            return input(f"{color}{prompt}{Color.RESET}")
        else:
            return input(prompt)


# Example usage
if __name__ == "__main__":
    ui = UIFramework()

    ui.clear_screen()

    # Title
    ui.print_centered("=== UI FRAMEWORK DEMO ===", color=Color.BRIGHT_CYAN)
    ui.print_centered("Terminal Rendering Test", color=Color.CYAN)
    print()

    # Color test
    print("Color Test:")
    ui.print_colored("  RED text", color=Color.RED)
    ui.print_colored("  GREEN text", color=Color.GREEN)
    ui.print_colored("  BLUE text", color=Color.BLUE)
    ui.print_colored("  BOLD YELLOW", color=Color.YELLOW, style=Color.BOLD)
    print()

    # Progress bars
    print("Progress Bars:")
    print("  Health: " + ui.print_bar(75, 100, width=20, color=Color.GREEN))
    print("  Mana:   " + ui.print_bar(40, 100, width=20, color=Color.BLUE))
    print("  XP:     " + ui.print_bar(90, 100, width=20, color=Color.YELLOW))
    print()

    # Panel test
    panel = Panel("Resources", width=50, border_style='double', title_color=Color.BRIGHT_GREEN)
    ui.render_panel(panel, [
        f"{Color.YELLOW}Gold:{Color.RESET} 1,234",
        f"{Color.GREEN}Wood:{Color.RESET} 567",
        f"{Color.CYAN}Stone:{Color.RESET} 890"
    ])
    print()

    # Table test
    ui.render_table(
        headers=["Building", "Count", "Production"],
        rows=[
            ["Farm", "5", "+10 food/s"],
            ["Mine", "3", "+6 stone/s"],
            ["Barracks", "2", "+4 soldiers/s"]
        ],
        border_style='single'
    )
    print()

    ui.print_separator()
    ui.print_colored("Demo complete!", color=Color.BRIGHT_GREEN, style=Color.BOLD)
