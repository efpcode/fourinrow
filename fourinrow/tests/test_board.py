# -*- coding: utf-8 -*-
from inspect import iscoroutinefunction
from turtle import position

import pytest
from fourinrow.fourinrow import (
    BoardValues,
    IsOutOfRange,
    PlayerTokens,
    create_board,
    move_diagonal,
    move_linear,
    token_equality,
)


def test_board_defaults() -> None:
    board = create_board()
    none_vals = sum([value.count(None) for value in board])
    expected_value = len(board) * len(board[0])
    assert none_vals == expected_value


def test_default_tokens() -> None:
    assert PlayerTokens.NO_PLAYER.value == "\u2610"
    assert PlayerTokens.PLAYER_1.value == "\U0001F534"
    assert PlayerTokens.PLAYER_2.value == "\U0001F535"
    assert PlayerTokens.CPU.value == "\U0001F916"


def test_move_linear() -> None:
    board_pos = (1, 2)
    new_pos_mv = move_linear(board_pos, 1)
    new_neg_mv = move_linear(board_pos, -1)
    new_pos_mv_v = move_linear(board_pos, 1, True)
    new_neg_mv_v = move_linear(board_pos, -1, True)
    assert new_pos_mv == (board_pos[0], board_pos[1] + 1)
    assert new_neg_mv == (board_pos[0], board_pos[1] - 1)
    assert new_pos_mv_v == (board_pos[0] + 1, board_pos[1])
    assert new_neg_mv_v == (board_pos[0] - 1, board_pos[1])


def test_none_linear_move() -> None:
    board_pos = (None, None)
    with pytest.raises(
        ValueError,
        match=f"Invalid values: Row is {board_pos[0]} or Column is {board_pos[1]}",
    ):
        move_linear(board_pos, 1)


def test_none_diagonal_move() -> None:
    board_pos = (None, None)
    with pytest.raises(
        ValueError,
        match=f"Invalid values: Row is {board_pos[0]} or Column is {board_pos[1]}",
    ):
        move_diagonal(board_pos, 1, "tlc")


def test_move_diagonal() -> None:
    board_pos = (0, 0)
    trc_pos = move_diagonal(board_pos, 1, "trc")
    brc_pos = move_diagonal(board_pos, 1, "brc")
    tlc_pos = move_diagonal(board_pos, 1, "tlc")
    blc_pos = move_diagonal(board_pos, 1, "blc")
    assert trc_pos == (board_pos[0] + 1, board_pos[1] + 1)
    assert brc_pos == (board_pos[0] + 1, board_pos[1] - 1)
    assert tlc_pos == (board_pos[0] - 1, board_pos[1] + 1)
    assert blc_pos == (board_pos[0] - 1, board_pos[1] - 1)


def test_token_equality():
    board = create_board(rows=2, columns=2)
    board[0][1] = PlayerTokens.PLAYER_1.value
    board[1][1] = PlayerTokens.PLAYER_1.value
    token_equal = token_equality(board, match_token=(0, 1), target_token=(1, 1))
    assert token_equal is True


@pytest.fixture
def board_creator() -> BoardValues:
    return BoardValues(rows=6, columns=7)


@pytest.fixture
def board_data(board_creator) -> BoardValues:
    board_creator.board[0][1] = PlayerTokens.PLAYER_1.value
    return board_creator


def test_create_board(board_creator):
    board = board_creator.create_board(board_creator.rows, board_creator.columns)
    assert len(board) == board_creator.rows
    assert len(board[0]) == board_creator.columns


def test_get_board_value(board_data):
    token = board_data.get_board_value((0, 1))
    assert token == PlayerTokens.PLAYER_1.value


def test_within_range(board_data):
    with pytest.raises(
        IsOutOfRange, match=f"Row: {(-1) +1}, Column: {8 +1} - Out of range"
    ):
        board_data.get_board_value((-1, 8))


def test_set_board_value(board_data):
    board_data.set_board_value(position=(1, 1), value=PlayerTokens.PLAYER_2.value)
    assert board_data.board[1][1] == PlayerTokens.PLAYER_2.value
    assert board_data.get_board_value((1, 1)) == PlayerTokens.PLAYER_2.value


def test_board_value_equality(board_data):
    board_data.set_board_value(position=(1, 4), value=PlayerTokens.PLAYER_1.value)
    assert board_data.board_value_equality(position=(0, 1), position2=(1, 4))
