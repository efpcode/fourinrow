# -*- coding: utf-8 -*-

from fourinrow.fourinrow import select_a_slot, create_board


def test_pick_position(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 2)
    board = create_board()
    value = select_a_slot(board)
    assert value == (1, 1)
