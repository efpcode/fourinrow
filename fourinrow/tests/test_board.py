# -*- coding: utf-8 -*-
import pytest
from fourinrow.game.game_model import (
    PlayerTokens,
    board_moves,
    BoardValues,
)
from fourinrow.game.game_exceptions import IsOutOfRange


def test_board_defaults() -> None:
    board = BoardValues(3, 3)
    none_vals = sum([value.count(None) for value in board.board])
    expected_value = len(board.board) * len(board.board[0])
    assert none_vals == expected_value


def test_default_tokens() -> None:
    assert PlayerTokens.NO_PLAYER.value == "\u2610"
    assert PlayerTokens.PLAYER_1.value == "\U0001F534"
    assert PlayerTokens.PLAYER_2.value == "\U0001F535"
    assert PlayerTokens.CPU.value == "\U0001F916"


@pytest.fixture
def start_pos() -> tuple:
    return -1, 1


def test_board_moves(start_pos) -> None:
    # Return default value of func.
    assert board_moves(start_pos, "test") == (0, 2)
    assert board_moves(start_pos, "Lbc") == (-2, 0)
    assert board_moves(start_pos, "bRc") == (0, 0)
    assert board_moves(start_pos, "LtC") == (-2, 2)
    assert board_moves(start_pos, "UP") == (-1, 2)
    assert board_moves(start_pos, "down") == (-1, 0)
    assert board_moves(start_pos, "left") == (-2, 1)
    assert board_moves(start_pos, "Right") == (0, 1)


def test_board_moves_reverse(start_pos) -> None:
    assert board_moves(start_pos, "up", is_reverse=True) == board_moves(
        start_pos, "down"
    )

    assert board_moves(start_pos, "ltc", is_reverse=True) == board_moves(
        start_pos, "brc"
    )


@pytest.mark.xfail(raises=TypeError, strict=True)
def test_board_moves_direction_not_str(start_pos):
    board_moves(start_pos, 1)


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
