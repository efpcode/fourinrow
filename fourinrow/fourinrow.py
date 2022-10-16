# -*- coding: utf-8 -*-
"""Four-in-a-row Game"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple


class SlotIsOccupiedError(Exception):
    """Handles slot is not empty exception"""

    def __init__(self, position: Tuple[int, int], message="Slot is occupied") -> None:
        self.position = position
        self.message = message
        super().__init__(message)

    def __str__(self):
        row, column = self.position
        return f"Row: {row +1}, Column: {column +1} - {self.message}"


class IsOutOfRange(Exception):
    """Handles when board postions passed are out of range"""

    def __init__(self, position: Tuple[int, int], message="Out of range") -> None:
        self.position = position
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        row, column = self.position
        return f"Row: {row +1}, Column: {column +1} - {self.message}"


def view_board_tokens(slot_value: str) -> str:
    """

    Parameters
    ----------
    slot_value : str
        The parameter called slot_value is positional value in the board.

    Returns
    -------
    slot_value : str
        The value of that position of the board.

    """
    if not slot_value:
        slot_value = PlayerTokens.NO_PLAYER.value
    return slot_value


def show_board(board: list) -> None:
    """Present the board in human friendly terms.

    Parameters
    ----------
    board: list
        The playing board.

    """

    for idx, row in enumerate(board, 1):
        print(idx, list(map(view_board_tokens, row)))
    cols = [f"{value:>5}" for value in range(1, (len(board[0]) + 1))]
    print("".join(cols))


class PlayerTokens(Enum):
    """The available tokens in the game."""

    PLAYER_1 = "\U0001F534"  # Red Circle
    PLAYER_2 = "\U0001F535"  # Blue Circle
    CPU = "\U0001F916"  # Robot Face
    NO_PLAYER = "\u2610"  # Empty square

    def __str__(self):
        return f"{self.value}"

    @classmethod
    def get_all_player_tokens(cls) -> list:
        """List all tokens in available in the game.

        Returns
        -------
        list
            The list of tokens

        """
        return [token.value for token in cls]


def select_a_slot(board: list) -> tuple:
    """Selects a position of the gaming board.

    Parameters
    ----------
    board: list
        The parameter board is the current gaming board.

    Returns
    -------
    tuple
        The value of row and column as a tuple (row, column)

    """
    rows_nums, columns_nums = range(len(board)), range(len(board[0]))

    while True:
        row, column = [input(f"Enter a {val} position") for val in ["row", "column"]]
        try:
            row, column = int(row) - 1, int(column) - 1  # count start from 1

            if not (row in rows_nums and column in columns_nums):
                raise IndexError

            if board[row][column]:
                raise SlotIsOccupiedError((row, column))

        except IndexError as error:
            print(f"{error} is not a valid option")
            continue

        except ValueError as error:
            print(f"{error} is not a digit")
            continue

        except SlotIsOccupiedError as error:
            print(error)
            continue

        else:
            return row, column


# TODO: Game logic
#    Position Walker
#    Check for winner -> Winner, Draw
#    Winner = [tk, tk, tk, tk] four elements have to have the same value


def board_moves(init_pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
    """Move initial board position in diagonal matter.

    Parameters
    ----------
    init_pos : Tuple[int, int]
        Starting position on the board (row, column)

    direction : str
        Valid values are lbc (left bottom corner), brc (bottom right corner),
        ltc (left top corner), up, down, left and right.
        The default value is trc (top right corner). Values indicate step
        direction.


    Returns
    -------
    new_row_pos, new_column_pos : Tuple[int, int]

    """
    if not init_pos:
        raise ValueError(f"Row: {init_pos[0]} or/and Column {init_pos[1]} are None")
    if not isinstance(direction, str):
        raise TypeError(f"direction: {direction} is not types str.")

    steps = {
        "lbc": (-1, -1),
        "brc": (1, -1),
        "ltc": (-1, 1),
        "up": (0, 1),
        "down": (0, -1),
        "left": (-1, 0),
        "right": (1, 0),
    }
    step = steps.get(direction.lower(), (1, 1))
    new_row_pos, new_column_pos = [
        (step[idx] + val) for idx, val in enumerate(init_pos)
    ]
    return new_row_pos, new_column_pos


@dataclass
class BoardValues:
    """Represents the bord and it values"""

    rows: int
    columns: int
    board: list = field(init=False, repr=False)

    def create_board(self, rows, columns):
        """

        Parameters
        ----------
        rows : int
            Number of rows
        columns : int
            Number of columns

        Returns
        -------
        Board : list
            The board: [(row, column), (row, column)]

        """
        board = []
        for _ in range(rows):
            board.append([None for _ in range(columns)])
        return board

    def get_board_value(self, pos: Tuple[int, int]) -> PlayerTokens:
        """Get board value from coordinates"""
        pos = self._position_in_range(pos)
        return self.board[pos[0]][pos[1]]

    def set_board_value(self, position: Tuple[int, int], value: PlayerTokens) -> None:
        """Set a value to board coordinates"""
        pos = self._position_in_range(position=position)
        new_board = self.board
        new_board[pos[0]][pos[1]] = value
        self.board = new_board

    def board_value_equality(
        self, position: Tuple[int, int], position2=Tuple[int, int]
    ) -> bool:
        """Checks if board coordinates have the same value"""
        value_pos = self.get_board_value(pos=position)
        value_pos2 = self.get_board_value(pos=position2)
        return value_pos is value_pos2

    def _position_in_range(self, position: Tuple[int, int]) -> Tuple[int, int]:
        row, column = position
        is_pos_negative = all(map(lambda x: x >= 0, position))
        is_within_range = all(
            (len(self.board) - 1 >= row, len(self.board[0]) - 1 >= column)
        )

        if not (is_pos_negative and is_within_range):
            raise IsOutOfRange(position=position)
        return position

    def __post_init__(self):
        new_board = self.create_board(self.rows, self.columns)
        self.board = new_board
        return self.board


if __name__ == "__main__":
    print("Welcome")
