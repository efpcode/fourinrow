# -*- coding: utf-8 -*-
"""Four-in-a-row Game"""
from enum import Enum
from typing import Tuple


class SlotIsOccupiedError(Exception):
    """Handles slot is not empty exception"""

    def __init__(self, position: tuple, message="Slot is occupied"):
        self.position = position
        self.message = message
        super().__init__(message)

    def __str__(self):
        row, column = self.position
        return f"Row: {row +1}, Column: {column +1} - {self.message}"


def create_board(rows: int = 6, columns: int = 7) -> list:
    """Creates playing board by rows X column

    Parameters
    ----------
    rows : int
        The rows parameter is the number of rows of the board.
    columns : int
        The columns parameter is the number of columns of the  board.


    Returns
    -------
    board: list
        The board with rows X columns [(row, column), (row, column)....]

    """
    board = []
    for _ in range(rows):
        board.append([None for _ in range(columns)])
    return board


def board_tokens(slot_value: str) -> str:
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
        print(idx, list(map(board_tokens, row)))
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


def move_linear(init_pos: Tuple[int, int], step: int, v_move: bool = False) -> tuple:
    """Moves horizontal or vertical from initial board position

    Parameters
    ----------
    init_pos : tuple
        The parameter init_pos is the initial position on the board.
    step : int
        The step parameter, determines movement distance from initial point.
    v_move: bool
        The v_move, is bool if set to value True direction is vertical.

    Returns
    -------
    tuple : int
         New position for row and column (row, column)

    """
    if None in init_pos:
        raise ValueError(
            f"Invalid values: Row is {init_pos[0]} or Column is {init_pos[1]}"
        )
    if v_move:
        return init_pos[0] + step, init_pos[1]
    return init_pos[0], init_pos[1] + step


if __name__ == "__main__":
    print("Welcome")
