# -*- coding: utf-8 -*-
import pytest
from fourinrow.fourinrow import SlotIsOccupiedError, create_board, select_a_slot


def test_pick_position(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 2)
    board = create_board()
    value = select_a_slot(board)
    assert value == (1, 1)


def test_occupied_slot(monkeypatch):
    board = create_board(2, 2)
    monkeypatch.setattr("builtins.input", lambda _: 2)
    row, column = select_a_slot(board)
    board[row][column] = 1

    with pytest.raises(
        SlotIsOccupiedError, match="Row: 2, Column: 2 - Slot is occupied"
    ):
        if board[row][column]:
            raise SlotIsOccupiedError((row, column))


# Todo Create Walker
# Needs to move one step - done
# Needs to remember last valid position - variable
# Needs to retrace steps - done
# Needs to count - variable
# Needs mock data to validate - think 3x3 and tictactoe.
# Needs to check tokes are the same
