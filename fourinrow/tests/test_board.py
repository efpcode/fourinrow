# -*- coding: utf-8 -*-
from fourinrow.fourinrow import create_board, PlayerTokens


def test_board_defaults():
    """Checks the defaults values of board.
    Correct answer should be nr rows x columns.
    """
    board = create_board()
    none_vals = sum([value.count(None) for value in board])
    expected_value = len(board) * len(board[0])
    assert none_vals == expected_value


def test_default_tokens():
    assert PlayerTokens.NO_PLAYER.value == "\u2610"
    assert PlayerTokens.PLAYER_1.value == "\U0001F534"
    assert PlayerTokens.PLAYER_2.value == "\U0001F535"
    assert PlayerTokens.CPU.value == "\U0001F916"
