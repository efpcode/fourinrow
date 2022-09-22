# -*- coding: utf-8 -*-
import pytest
from fourinrow.fourinrow import select_a_slot, create_board
from fourinrow.fourinrow import SlotIsOccupiedError
from fourinrow.fourinrow import move_linear


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


def test_move_linear():
    board_pos = (1, 2)
    new_pos_mv = move_linear(board_pos, 1)
    new_neg_mv = move_linear(board_pos, -1)
    new_pos_mv_v = move_linear(board_pos, 1, True)
    new_neg_mv_v = move_linear(board_pos, -1, True)
    expected_value = (board_pos[0], board_pos[1] + 1)
    expected_value2 = (board_pos[0], board_pos[1] - 1)
    expected_value3 = (board_pos[0] + 1, board_pos[1])
    expected_value4 = (board_pos[0] - 1, board_pos[1])
    assert new_pos_mv == expected_value
    assert new_neg_mv == expected_value2
    assert new_pos_mv_v == expected_value3
    assert new_neg_mv_v == expected_value4
