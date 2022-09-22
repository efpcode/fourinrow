# -*- coding: utf-8 -*-
from enum import Enum
from typing import Tuple

# TODO: Custom Exceptions
#       Slot is occupied
#


class SlotIsOccupiedError(Exception):
    def __init__(self, position: tuple, message="Slot is occupied"):
        self.position = position
        self.message = message
        super().__init__(message)

    def __str__(self):
        row, column = self.position
        return f"Row: {row +1}, Column: {column +1} - {self.message}"


# TODO: Create board
#       Data Structure nested list
#       Row[[Columns]] = row = 6, columns=7
#       Show board


def create_board(rows: int = 6, columns: int = 7) -> list:
    """

    :param rows:
    :param columns:
    :return: rows[columns]
    """
    board = []
    for _ in range(rows):
        board.append([None for _ in range(columns)])
    return board


def board_tokens(cell: str) -> str:
    if not cell:
        cell = PlayerTokens.NO_PLAYER.value
    return cell


def show_board(board):
    for idx, row in enumerate(board, 1):
        print(idx, list(map(lambda x: board_tokens(x), row)))
    cols = [f"{value:>5}" for value in range(1, (len(board[0]) + 1))]
    print("".join(cols))


# TODO: Create Interface
#     Player Token
#     Placing Token only on None/Empty slot
class PlayerTokens(Enum):
    PLAYER_1 = "\U0001F534"  # Red Circle
    PLAYER_2 = "\U0001F535"  # Blue Circle
    CPU = "\U0001F916"  # Robot Face
    NO_PLAYER = "\u2610"  # Empty square

    def __str__(self):
        return f"{self.value}"

    @classmethod
    def get_all_player_tokens(cls) -> list:
        return [token.value for token in cls]


def select_a_slot(board):
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
#       Position Walker
#       Check for winner -> Winner, Draw
#       Winner = [tk, tk, tk, tk] four elements have to have the same value


def move_linear(board_pos: Tuple[int, int], step: int, v_move: bool = False) -> tuple:
    if v_move:
        return board_pos[0] + step, board_pos[1]
    return board_pos[0], board_pos[1] + step


if __name__ == "__main__":
    print("Welcome")
