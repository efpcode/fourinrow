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


def move_diagonal(init_pos, step, direction):
    """Move initial board position in diagonal matter.

    Parameters
    ----------
    init_pos : tuple
    step : int
    direction : str

    Returns
    -------
    tuple

    """
    row = None
    column = None
    if direction == "trc":
        _, column = move_linear(init_pos, step)
        row, _ = move_linear(init_pos, step, True)
    elif direction == "brc":
        _, column = move_linear(init_pos, (step * -1))
        row, _ = move_linear(init_pos, step, True)
    elif direction == "tlc":
        _, column = move_linear(init_pos, step)
        row, _ = move_linear(init_pos, (step * -1), True)
    else:
        _, column = move_linear(init_pos, (step * -1))
        row, _ = move_linear(init_pos, (step * -1), True)
        return row, column
    return row, column


def token_equality(
    board: list, match_token: Tuple[int, int], target_token: Tuple[int, int]
) -> bool:
    """Check if tow slots postion have the same token.

    Parameters
    ----------
    board : list
        Current playing board of n-rows X n-columns
    match_token : Tuple[int][int]
        Board position expressed as coordinates (row, column). Pattern to match against.
    target_token : Tuple[int][int]
        Board position expressed as coordinates (row, column). Target for match.

    Returns
    -------
    bool
        True if match- and target- token are equal. Otherwise returns False.
    """
    pattern_token = board[match_token[0]][match_token[1]]
    test_token = board[target_token[0]][target_token[1]]
    return pattern_token == test_token


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
