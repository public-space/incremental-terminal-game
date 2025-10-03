"""
Event Log System
================

Tracks game events with Sol (day) + time timestamps.
Dark, ominous message logging for colony.sh.
"""

import time
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogEntry:
    """
    A single log entry.

    Attributes:
        sol: Day number (Sol 0, Sol 1, etc.)
        timestamp: Human-readable time (HH:MM:SS)
        message: Event message
        category: Message type (info, warning, critical)
    """
    sol: int
    timestamp: str
    message: str
    category: str = 'info'

    def __str__(self) -> str:
        """Format log entry for display."""
        prefix = {
            'info': '  ',
            'warning': '⚠',
            'critical': '✖',
            'success': '✓',
        }.get(self.category, '  ')

        return f"[Sol {self.sol:03d} {self.timestamp}] {prefix} {self.message}"


class EventLog:
    """
    Event logging system with Sol timestamps.

    Attributes:
        entries: List of log entries
        max_entries: Maximum entries to keep (oldest removed)
        current_sol: Current Sol (day) number
        session_start: Session start time for timestamp calculation
    """

    def __init__(self, max_entries: int = 100):
        """
        Initialize event log.

        Args:
            max_entries: Maximum log entries to keep
        """
        self.entries: List[LogEntry] = []
        self.max_entries = max_entries
        self.current_sol = 0
        self.session_start = time.time()

    def set_sol(self, sol: int):
        """
        Set current Sol number.

        Args:
            sol: Sol number
        """
        self.current_sol = sol

    def _get_timestamp(self) -> str:
        """
        Get current timestamp string.

        Returns:
            str: HH:MM:SS formatted time
        """
        return datetime.now().strftime("%H:%M:%S")

    def log(self, message: str, category: str = 'info'):
        """
        Add a log entry.

        Args:
            message: Event message
            category: Message type (info, warning, critical, success)
        """
        entry = LogEntry(
            sol=self.current_sol,
            timestamp=self._get_timestamp(),
            message=message,
            category=category
        )

        self.entries.append(entry)

        # Trim old entries
        if len(self.entries) > self.max_entries:
            self.entries.pop(0)

    def info(self, message: str):
        """Log an info message."""
        self.log(message, 'info')

    def warning(self, message: str):
        """Log a warning message."""
        self.log(message, 'warning')

    def critical(self, message: str):
        """Log a critical message."""
        self.log(message, 'critical')

    def success(self, message: str):
        """Log a success message."""
        self.log(message, 'success')

    def get_recent(self, count: int = 10) -> List[LogEntry]:
        """
        Get recent log entries.

        Args:
            count: Number of recent entries

        Returns:
            list: Recent log entries (newest last)
        """
        return self.entries[-count:] if self.entries else []

    def get_all(self) -> List[LogEntry]:
        """
        Get all log entries.

        Returns:
            list: All log entries
        """
        return self.entries.copy()

    def clear(self):
        """Clear all log entries."""
        self.entries.clear()

    def to_dict(self) -> dict:
        """
        Serialize to dictionary.

        Returns:
            dict: Serialized event log
        """
        return {
            'entries': [
                {
                    'sol': e.sol,
                    'timestamp': e.timestamp,
                    'message': e.message,
                    'category': e.category
                }
                for e in self.entries
            ],
            'current_sol': self.current_sol,
            'max_entries': self.max_entries,
        }

    @staticmethod
    def from_dict(data: dict) -> 'EventLog':
        """
        Deserialize from dictionary.

        Args:
            data: Serialized event log

        Returns:
            EventLog: Restored event log
        """
        log = EventLog(max_entries=data.get('max_entries', 100))
        log.current_sol = data.get('current_sol', 0)

        for entry_data in data.get('entries', []):
            entry = LogEntry(
                sol=entry_data['sol'],
                timestamp=entry_data['timestamp'],
                message=entry_data['message'],
                category=entry_data.get('category', 'info')
            )
            log.entries.append(entry)

        return log


# Example usage
if __name__ == "__main__":
    print("=== EVENT LOG TEST ===\n")

    log = EventLog(max_entries=20)

    # Simulate game events
    log.set_sol(0)
    log.info("Colony initialization sequence started")
    log.success("Solar Array online")
    log.success("Hab Module pressurized")
    log.info("3 colonists awake from cryo-sleep")

    time.sleep(0.1)

    log.set_sol(1)
    log.info("Mining Rig constructed")
    log.warning("Energy reserves low")
    log.info("Research Terminal activated")

    time.sleep(0.1)

    log.set_sol(2)
    log.critical("Hull breach detected in Sector 7")
    log.success("Emergency protocols engaged")
    log.info("Repairs completed")

    # Display recent entries
    print("Recent Events:\n")
    for entry in log.get_recent(10):
        print(entry)

    # Test serialization
    print("\n\n=== Serialization Test ===\n")
    data = log.to_dict()
    restored_log = EventLog.from_dict(data)

    print(f"Original entries: {len(log.entries)}")
    print(f"Restored entries: {len(restored_log.entries)}")
    print(f"✓ Serialization successful!" if len(log.entries) == len(restored_log.entries) else "✖ Failed!")
