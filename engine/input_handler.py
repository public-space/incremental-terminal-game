"""
Input Handler Module
=====================

Command processing and input management for terminal games.
Handles command registration, parsing, validation, and execution.

Classes:
    Command: Individual command definition
    InputHandler: Main input processing system

Usage:
    handler = InputHandler()
    handler.register_command('build', build_callback, 'Build a structure')
    handler.process_input('build farm')
"""

import logging
from typing import Callable, Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import shlex

logger = logging.getLogger(__name__)


@dataclass
class Command:
    """
    Represents a game command.

    Attributes:
        name (str): Primary command name
        callback (Callable): Function to execute
        description (str): Command description for help
        aliases (List[str]): Alternative names for command
        args_help (str): Argument usage help
        category (str): Command category for organization
        enabled (bool): Whether command is currently enabled
    """
    name: str
    callback: Callable
    description: str = ""
    aliases: List[str] = field(default_factory=list)
    args_help: str = ""
    category: str = "General"
    enabled: bool = True

    def matches(self, input_name: str) -> bool:
        """
        Check if input matches this command.

        Args:
            input_name: Input command name

        Returns:
            bool: True if matches name or alias
        """
        return input_name.lower() in [self.name.lower()] + [a.lower() for a in self.aliases]


class InputHandler:
    """
    Handles user input and command processing.

    Attributes:
        commands (Dict[str, Command]): Registered commands
        command_history (List[str]): Input history
        max_history (int): Maximum history entries
    """

    def __init__(self, max_history: int = 100):
        """
        Initialize the input handler.

        Args:
            max_history: Maximum command history entries
        """
        self.commands: Dict[str, Command] = {}
        self.command_history: List[str] = []
        self.max_history = max_history
        logger.info("InputHandler initialized")

    def register_command(
        self,
        name: str,
        callback: Callable,
        description: str = "",
        aliases: Optional[List[str]] = None,
        args_help: str = "",
        category: str = "General"
    ) -> Command:
        """
        Register a new command.

        Args:
            name: Command name
            callback: Function to call (receives args list)
            description: Command description
            aliases: Alternative command names
            args_help: Argument usage string
            category: Command category

        Returns:
            Command: The registered command

        Raises:
            ValueError: If command name already exists
        """
        name_lower = name.lower()

        if name_lower in self.commands:
            raise ValueError(f"Command '{name}' already registered")

        command = Command(
            name=name_lower,
            callback=callback,
            description=description,
            aliases=aliases or [],
            args_help=args_help,
            category=category
        )

        self.commands[name_lower] = command

        # Register aliases
        for alias in command.aliases:
            self.commands[alias.lower()] = command

        logger.info(f"Command registered: {name} (aliases: {aliases or []})")
        return command

    def unregister_command(self, name: str):
        """
        Unregister a command.

        Args:
            name: Command name to remove
        """
        name_lower = name.lower()

        if name_lower in self.commands:
            command = self.commands[name_lower]

            # Remove command and all aliases
            del self.commands[name_lower]
            for alias in command.aliases:
                if alias.lower() in self.commands:
                    del self.commands[alias.lower()]

            logger.info(f"Command unregistered: {name}")

    def parse_input(self, user_input: str) -> Tuple[Optional[str], List[str]]:
        """
        Parse user input into command and arguments.

        Args:
            user_input: Raw user input

        Returns:
            tuple: (command_name, arguments_list) or (None, []) if empty
        """
        user_input = user_input.strip()

        if not user_input:
            return None, []

        try:
            # Use shlex for proper quote handling
            parts = shlex.split(user_input)
        except ValueError:
            # Fallback to simple split if shlex fails
            parts = user_input.split()

        command_name = parts[0].lower() if parts else None
        args = parts[1:] if len(parts) > 1 else []

        return command_name, args

    def process_input(self, user_input: str) -> Optional[Any]:
        """
        Process user input and execute command.

        Args:
            user_input: Raw user input

        Returns:
            Any: Command return value, or None if no command
        """
        # Add to history
        if user_input.strip():
            self.command_history.append(user_input)
            if len(self.command_history) > self.max_history:
                self.command_history.pop(0)

        # Parse input
        command_name, args = self.parse_input(user_input)

        if not command_name:
            return None

        # Find command
        command = self.find_command(command_name)

        if not command:
            logger.debug(f"Unknown command: {command_name}")
            print(f"Unknown command: '{command_name}'. Type 'help' for available commands.")
            return None

        if not command.enabled:
            logger.debug(f"Command disabled: {command_name}")
            print(f"Command '{command_name}' is currently disabled.")
            return None

        # Execute command
        try:
            logger.debug(f"Executing command: {command_name} with args: {args}")
            result = command.callback(args)
            return result

        except TypeError as e:
            logger.error(f"Command argument error: {e}")
            print(f"Error: Invalid arguments for '{command_name}'.")
            if command.args_help:
                print(f"Usage: {command_name} {command.args_help}")
            return None

        except Exception as e:
            logger.error(f"Command execution error: {e}", exc_info=True)
            print(f"Error executing '{command_name}': {e}")
            return None

    def find_command(self, name: str) -> Optional[Command]:
        """
        Find a command by name or alias.

        Args:
            name: Command name or alias

        Returns:
            Command or None: The command if found
        """
        return self.commands.get(name.lower())

    def get_commands_by_category(self) -> Dict[str, List[Command]]:
        """
        Get commands organized by category.

        Returns:
            dict: {category: [commands]}
        """
        categorized: Dict[str, List[Command]] = {}

        # Use set to avoid duplicate commands (from aliases)
        seen_commands = set()

        for command in self.commands.values():
            if command.name in seen_commands:
                continue

            seen_commands.add(command.name)

            if command.category not in categorized:
                categorized[command.category] = []

            categorized[command.category].append(command)

        return categorized

    def generate_help(self, command_name: Optional[str] = None) -> str:
        """
        Generate help text.

        Args:
            command_name: Specific command to get help for (None = all)

        Returns:
            str: Help text
        """
        if command_name:
            # Help for specific command
            command = self.find_command(command_name)

            if not command:
                return f"Unknown command: '{command_name}'"

            help_text = f"\n{command.name.upper()}"

            if command.aliases:
                help_text += f" (aliases: {', '.join(command.aliases)})"

            help_text += f"\n{'─' * 40}\n"

            if command.description:
                help_text += f"{command.description}\n"

            if command.args_help:
                help_text += f"\nUsage: {command.name} {command.args_help}\n"

            return help_text

        else:
            # Help for all commands
            help_text = "\n=== AVAILABLE COMMANDS ===\n"

            categorized = self.get_commands_by_category()

            for category in sorted(categorized.keys()):
                help_text += f"\n{category}:\n"

                for command in sorted(categorized[category], key=lambda c: c.name):
                    if not command.enabled:
                        continue

                    # Format command line
                    cmd_line = f"  {command.name:<12}"

                    if command.aliases:
                        cmd_line += f" [{', '.join(command.aliases)}]"

                    cmd_line = cmd_line.ljust(30)

                    if command.description:
                        cmd_line += f" - {command.description}"

                    help_text += cmd_line + "\n"

            help_text += "\nType 'help <command>' for detailed help on a specific command.\n"

            return help_text

    def enable_command(self, name: str):
        """
        Enable a command.

        Args:
            name: Command name
        """
        command = self.find_command(name)
        if command:
            command.enabled = True
            logger.info(f"Command enabled: {name}")

    def disable_command(self, name: str):
        """
        Disable a command.

        Args:
            name: Command name
        """
        command = self.find_command(name)
        if command:
            command.enabled = False
            logger.info(f"Command disabled: {name}")

    def get_history(self, count: Optional[int] = None) -> List[str]:
        """
        Get command history.

        Args:
            count: Number of recent commands (None = all)

        Returns:
            list: Command history
        """
        if count is None:
            return self.command_history.copy()
        else:
            return self.command_history[-count:]

    def clear_history(self):
        """Clear command history."""
        self.command_history.clear()
        logger.info("Command history cleared")

    def autocomplete(self, partial: str) -> List[str]:
        """
        Get autocomplete suggestions.

        Args:
            partial: Partial command name

        Returns:
            list: Matching command names
        """
        partial_lower = partial.lower()
        matches = []

        seen = set()

        for command in self.commands.values():
            if command.name in seen:
                continue

            if command.name.startswith(partial_lower):
                matches.append(command.name)
                seen.add(command.name)

        return sorted(matches)


# Example usage
if __name__ == "__main__":
    handler = InputHandler()

    # Example commands
    def cmd_build(args):
        if not args:
            print("What do you want to build?")
            return

        building = args[0]
        print(f"Building {building}...")

    def cmd_recruit(args):
        if not args:
            print("What unit to recruit?")
            return

        unit = args[0]
        count = int(args[1]) if len(args) > 1 else 1
        print(f"Recruiting {count}x {unit}...")

    def cmd_save(args):
        filename = args[0] if args else "savegame.json"
        print(f"Saving to {filename}...")

    def cmd_quit(args):
        print("Goodbye!")
        return "QUIT"

    def cmd_help(args):
        command_name = args[0] if args else None
        print(handler.generate_help(command_name))

    # Register commands
    handler.register_command('build', cmd_build, 'Build a structure', aliases=['b'], args_help='<building_name>', category='Building')
    handler.register_command('recruit', cmd_recruit, 'Recruit units', aliases=['r'], args_help='<unit> [count]', category='Units')
    handler.register_command('save', cmd_save, 'Save the game', aliases=['s'], args_help='[filename]', category='System')
    handler.register_command('quit', cmd_quit, 'Exit the game', aliases=['q', 'exit'], category='System')
    handler.register_command('help', cmd_help, 'Show help', aliases=['h', '?'], args_help='[command]', category='System')

    # Test commands
    print("=== INPUT HANDLER TEST ===\n")

    test_inputs = [
        "help",
        "build farm",
        "b mill",
        "recruit worker 5",
        "r knight",
        "save mygame.json",
        "invalid_command",
        "help build"
    ]

    for user_input in test_inputs:
        print(f"\n> {user_input}")
        handler.process_input(user_input)

    print("\n\n=== Command History ===")
    for i, cmd in enumerate(handler.get_history(), 1):
        print(f"{i}. {cmd}")

    print("\n\n=== Autocomplete Test ===")
    print(f"Autocomplete 'b': {handler.autocomplete('b')}")
    print(f"Autocomplete 'rec': {handler.autocomplete('rec')}")
