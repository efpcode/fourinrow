# -*- coding: utf-8 -*-
from fourinrow.fourinrow import board_tokens, create_board
from fourinrow.fourinrow import PlayerTokens, show_board


def test_display_empty_token() -> None:
    board = create_board(2, 2)
    for row, _ in enumerate(board):
        for column, _ in enumerate(_):
            token = board_tokens(board[row][column])
            assert token == PlayerTokens.NO_PLAYER.value


def test_display_token_defaults() -> None:
    tokens = PlayerTokens.get_all_player_tokens()
    for idx, player in enumerate(PlayerTokens):
        token = board_tokens(player.value)
        assert token == tokens[idx]


def test_display_token_edit_value() -> None:
    board = create_board(1, 1)
    board[0][0] = 1
    token = board_tokens(board[0][0])
    assert token == 1


def test_display_board(capsys) -> None:
    board = create_board(1, 1)
    show_board(board)
    board_img = capsys.readouterr()
    expected_layout = "1 ['☐']\n    1\n"
    assert board_img.out == expected_layout
