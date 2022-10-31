# -*- coding: utf-8 -*-
"""All things that are used with player interaction"""
import re
from dataclasses import dataclass
from typing import Tuple

from fourinrow.game.game_model import (
    BoardValues,
    IsOutOfRange,
    PlayerTokens,
    SlotIsOccupiedError,
    board_moves,
)


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


def select_player(player_name: str, player_picked: PlayerTokens = None) -> PlayerTokens:
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
        "robot": PlayerTokens.CPU,
    }
    pattern = re.compile(r"[\W_]")

    while True:
        if not player_name:
            player_name = input(
                f"Please select a players: " f" {', '.join(all_players.keys())}: "
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


@dataclass
class GameLogic:
    """Represent the rules set of the game"""

    nr_tokens_to_win: int
    nr_rounds: int

    def board_walker(self, init_pos: Tuple[int, int], board: BoardValues) -> tuple:
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
            next_pos = board_moves(
                last_valid_pos, direction=val, is_reverse=reverse_val
            )
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
                if len(board_pos) == self.nr_tokens_to_win:
                    is_loop = False
        board_pos.sort()

        return tuple(board_pos)
