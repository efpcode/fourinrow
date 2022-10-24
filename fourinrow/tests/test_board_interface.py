# -*- coding: utf-8 -*-
from typing import Tuple

import pytest
from fourinrow.fourinrow import (
    BoardValues,
    GameLogic,
    PlayerTokens,
    SlotIsOccupiedError,
    select_a_slot,
)


@pytest.fixture
def game_board():
    return BoardValues(6, 7)


@pytest.fixture
def win_board():
    game_board = BoardValues(3, 3)
    game_board.set_board_value((0, 0), PlayerTokens.PLAYER_1.value)
    game_board.set_board_value((1, 0), PlayerTokens.PLAYER_1.value)
    game_board.set_board_value((1, 1), PlayerTokens.PLAYER_1.value)
    game_board.set_board_value((2, 2), PlayerTokens.PLAYER_1.value)
    return game_board


def test_pick_position(monkeypatch, game_board):
    monkeypatch.setattr("builtins.input", lambda _: 2)
    value = select_a_slot(game_board.board)
    assert value == (1, 1)


def test_occupied_slot(monkeypatch, game_board):
    monkeypatch.setattr("builtins.input", lambda _: 2)
    row, column = select_a_slot(game_board.board)
    game_board.board[row][column] = 1

    with pytest.raises(
        SlotIsOccupiedError, match="Row: 2, Column: 2 - Slot is occupied"
    ):
        if game_board.board[row][column]:
            raise SlotIsOccupiedError((row, column))


# Todo Create Walker
# Needs to move one step - done
# Needs to remember last valid position - variable
# Needs to retrace steps - done
# Needs to count - variable
# Needs mock data to validate - think 3x3 and tictactoe.
# Needs to check tokens are the same


def test_board_walker(win_board):
    init_pos = (1, 1)
    game = GameLogic(3, 1)
    win_pos = game.board_walker(init_pos, win_board)
    assert win_pos == ((0, 0), (1, 1), (2, 2))


def test_no_wins(win_board):
    init_pos = (1, 0)
    game = GameLogic(3, 1)
    no_wins = game.board_walker(init_pos, win_board)
    assert no_wins == ((1, 0),)
