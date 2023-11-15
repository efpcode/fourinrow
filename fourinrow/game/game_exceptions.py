# -*- coding: utf-8 -*-
"""All things that are used with player interaction"""
from typing import Tuple


class IsOutOfRange(Exception):
    """Handles when board positions passed are out of range"""

    def __init__(self, position: Tuple[int, int], message="Out of range") -> None:
        self.position = position
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        row, column = self.position
        return f"Row: {row +1}, Column: {column +1} - {self.message}"


class SlotIsOccupiedError(Exception):
    """Handles slot is not empty exception"""

    def __init__(self, position: Tuple[int, int], message="Slot is occupied") -> None:
        self.position = position
        self.message = message
        super().__init__(message)

    def __str__(self):
        row, column = self.position
        return f"Row: {row +1}, Column: {column +1} - {self.message}"
