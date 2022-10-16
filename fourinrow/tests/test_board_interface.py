# -*- coding: utf-8 -*-
import pytest
from fourinrow.fourinrow import SlotIsOccupiedError, BoardValues, select_a_slot


@pytest.fixture
def game_board():
    return BoardValues(6, 7)


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
# Needs to check tokes are the same
