# -*- coding: utf-8 -*-
import pytest
from fourinrow.fourinrow import BoardValues, PlayerTokens, show_board, view_board_tokens


@pytest.fixture
def board():
    return BoardValues(6, 7)


@pytest.fixture
def small_board():
    return BoardValues(1, 1)


def test_display_empty_token(board) -> None:
    for row, _ in enumerate(board.board):
        for column, _ in enumerate(_):
            token = view_board_tokens(board.board[row][column])
            assert token == PlayerTokens.NO_PLAYER.value


def test_display_token_defaults() -> None:
    tokens = PlayerTokens.get_all_player_tokens()
    for idx, player in enumerate(PlayerTokens):
        token = view_board_tokens(player.value)
        assert token == tokens[idx]


def test_display_token_edit_value(board) -> None:
    board.set_board_value((0, 0), PlayerTokens.CPU.value)
    token = view_board_tokens(board.board[0][0])
    assert token is PlayerTokens.CPU.value


def test_display_board(capsys, small_board) -> None:
    show_board(small_board.board)
    board_img = capsys.readouterr()
    expected_layout = "1 ['☐']\n    1\n"
    assert board_img.out == expected_layout
