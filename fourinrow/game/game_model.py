# -*- coding: utf-8 -*-
"""All things that are thought as board data"""
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple

from game.game_exceptions import IsOutOfRange, SlotIsOccupiedError


class PlayerTokens(Enum):
    """The available tokens in the game."""

    PLAYER_1 = "\U0001F534"  # Red Circle
    PLAYER_2 = "\U0001F535"  # Blue Circle
    CPU = "\U0001F916"  # Robot Face
    NO_PLAYER = "\U00002B1B"  # Empty square

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


def board_moves(
    init_pos: Tuple[int, int], direction: str = "trc", is_reverse=False
) -> Tuple[int, int]:
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

    is_reverse : bool
        Reverse the direction of the move.


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
    if is_reverse:
        step = step[0] * -1, step[1] * -1
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

    # class methods
    @classmethod
    def is_board_complete(cls, current_playing_board):
        """Returns bool if slot empty or not"""
        return all((value for row in current_playing_board for value in row))

    # Methods

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
        row, column = [input(f"Enter a {val} position: ") for val in ["row", "column"]]
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


def select_a_column(board: list) -> tuple:

    """Selects a position of the gaming board.

    Parameters
    ----------
    board: list
        The parameter board is the current gaming board.

    Returns
    -------
    tuple
    """
    columns_nums = range(len(board[0]))

    while True:
        column = input(f"Enter a column nr from 1 - {len(columns_nums)}: ")
        try:
            column = int(column) - 1  # count start from 1
            if not column in range(len(board[0])):
                raise ValueError
            all_column_pos = (
                (row, column) for row in range(len(board)) if not board[row][column]
            )
            all_col_sorted = sorted(all_column_pos, key=lambda x: x[0], reverse=True)
            if not all_col_sorted:
                raise IndexError

        except (TypeError, ValueError) as error:
            print(f"{error} is not a valid option")
            continue
        except IndexError as error:
            print(
                f"All column values are occupied for "
                f"{column + 1}: {error} please try another column."
            )
            continue
        else:
            return all_col_sorted[0]


def select_player(
    player_name: str = None, player_picked: PlayerTokens = None
) -> PlayerTokens:
    """

    Parameters
    ----------
    player_name : str
        The parameter specifies wanted player
    player_picked : PlayerTokens (optional)
        Filters available player list with passed parameter.


    Returns
    -------
    new_player : PlayerTokens
        Selected player as instance of PlayerTokens

    """
    all_players = {
        "player1": PlayerTokens.PLAYER_1,
        "player2": PlayerTokens.PLAYER_2,
        "cpu": PlayerTokens.CPU,
    }
    pattern = re.compile(r"[\W_]")

    while True:
        if not player_name:
            player_name = input(
                f"Please select a players: {', '.join(all_players.keys())}: "
            )
        player_name = pattern.sub("", player_name).lower()

        try:
            new_player = all_players[player_name]

            if player_picked:
                if player_picked == new_player:
                    raise ValueError("Player not available")

        except KeyError:
            print("Not a valid entry, please try again")
            player_name = None
            continue
        except ValueError:
            del all_players[pattern.sub("", player_name)]
            player_name = None
            continue
        else:
            return new_player


def switch_player(players: list, current_player: PlayerTokens):
    """Player switcher

    Parameters
    ----------
    players : list
    current_player : PlayerTokens

    Returns
    -------
        Switched player as PlayerTokens instance

    """
    tmp_list = players[:]
    tmp_list.pop(tmp_list.index(current_player))
    return tmp_list[0]


@dataclass
class GameConfig:
    """Represent the rules set of the game"""

    nr_tokens_to_win: int
    nr_rounds: int

    def board_dimensions(self) -> Tuple[int, int]:
        """Calculates 'proper' board dimensions"""
        nums_columns = self.nr_tokens_to_win + max(range(self.nr_tokens_to_win))
        return nums_columns - 1, nums_columns


def show_board(board: list) -> None:
    """Present the board in human friendly terms.

    Parameters
    ----------
    board: list
        The playing board.

    """

    for idx, row in enumerate(board, 1):
        print(idx, list(map(view_board_tokens, row)))
    cols = [f"{value:>6}" for value in range(1, (len(board[0]) + 1))]
    print("".join(cols))


def view_board_tokens(slot_value: str) -> str:
    """Display board tokens fix none issue.

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


def board_walker(
    nr_tokens_to_win, init_pos: Tuple[int, int], board: BoardValues
) -> tuple:
    """

    Parameters
    ----------
    init_pos : Tuple[int, int]
        Start position for placed token
    board : BoardValues
        Current gaming board


    Returns
    -------
        Will return a single or nth elements of tuples that corresponds
        to board positions.

    """
    reset_val = init_pos
    last_valid_pos = init_pos
    board_pos = [init_pos]
    directions = ["up", "right", "brc", "trc"]
    reverse_val = False
    errors = 0
    is_loop = True
    val = directions.pop(0)

    while is_loop:
        next_pos = board_moves(last_valid_pos, direction=val, is_reverse=reverse_val)
        try:
            if not board.board_value_equality(last_valid_pos, next_pos):
                raise IsOutOfRange(last_valid_pos, next_pos)
        except IsOutOfRange:
            reverse_val = reverse_val is not True
            last_valid_pos = reset_val
            errors += 1
            if not errors % 2:
                try:
                    val = directions.pop(0)
                except IndexError:
                    board_pos = [reset_val]
                    is_loop = False
                else:
                    board_pos = [reset_val]
            continue
        else:
            board_pos.append(next_pos)
            last_valid_pos = next_pos
            if len(board_pos) == nr_tokens_to_win:
                is_loop = False
    board_pos.sort()

    return tuple(board_pos)


def game_set_config() -> Tuple[int, int]:
    """
    Setups the conditions of the game
    Returns
    -------

    """
    general_txt = "Set number of "
    game_options = ["identitcal tokens to win: ", "rounds to play: "]
    while True:
        try:
            game_settings = [
                int(input("".join([general_txt, i]))) for i in game_options
            ]
        except (ValueError, TypeError):
            print("Please try again")
            continue
        else:
            return tuple(game_settings)
