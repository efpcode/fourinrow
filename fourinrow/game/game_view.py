# -*- coding: utf-8 -*-
"""All things connected with the view or presentation of game"""
from fourinrow.game.game_model import PlayerTokens


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
