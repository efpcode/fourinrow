# -*- coding: utf-8 -*-
import pytest

from fourinrow.fourinrow import create_board, PlayerTokens
from fourinrow.fourinrow import move_linear, move_diagonal


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


def test_move_linear():
    board_pos = (1, 2)
    new_pos_mv = move_linear(board_pos, 1)
    new_neg_mv = move_linear(board_pos, -1)
    new_pos_mv_v = move_linear(board_pos, 1, True)
    new_neg_mv_v = move_linear(board_pos, -1, True)
    assert new_pos_mv == (board_pos[0], board_pos[1] + 1)
    assert new_neg_mv == (board_pos[0], board_pos[1] - 1)
    assert new_pos_mv_v == (board_pos[0] + 1, board_pos[1])
    assert new_neg_mv_v == (board_pos[0] - 1, board_pos[1])


def test_none_move_linear():
    board_pos = (None, None)
    with pytest.raises(
        ValueError,
        match=f"Invalid values: Row is {board_pos[0]} or Column is " f"{board_pos[1]}",
    ):
        move_linear(board_pos, 1)


def test_move_diagonal():
    board_pos = (0, 0)
    trc_pos = move_diagonal(board_pos, 1, "trc")
    brc_pos = move_diagonal(board_pos, 1, "brc")
    tlc_pos = move_diagonal(board_pos, 1, "tlc")
    blc_pos = move_diagonal(board_pos, 1, "blc")
    assert trc_pos == (board_pos[0] + 1, board_pos[1] + 1)
    assert brc_pos == (board_pos[0] + 1, board_pos[1] - 1)
    assert tlc_pos == (board_pos[0] - 1, board_pos[1] + 1)
    assert blc_pos == (board_pos[0] - 1, board_pos[1] - 1)
