# -*- coding: utf-8 -*-
import pytest
from fourinrow.fourinrow import select_a_slot, create_board
from fourinrow.fourinrow import SlotIsOccupiedError


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
