# -*- coding: utf-8 -*-
from fourinrow.fourinrow import board_tokens, create_board, PlayerTokens


def test_display_empty_token():
    board = create_board(2, 2)
    for row, _ in enumerate(board):
        for column, _ in enumerate(_):
            token = board_tokens(board[row][column])
            assert token == PlayerTokens.NO_PLAYER.value


def test_display_token_defaults():
    tokens = PlayerTokens.get_all_player_tokens()
    for idx, player in enumerate(PlayerTokens):
        token = board_tokens(player.value)
        assert token == tokens[idx]


def test_display_token_edit_value():
    board = create_board(1, 1)
    board[0][0] = 1
    token = board_tokens(board[0][0])
    assert token == 1
