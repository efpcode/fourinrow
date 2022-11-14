# -*- coding: utf-8 -*-
from typing import Tuple

import pytest
from random import choice
from fourinrow.game.game_model import (
    PlayerTokens,
    BoardValues,
    select_a_slot,
    select_player,
    switch_player,
    GameConfig,
    board_walker,
)
from fourinrow.game.game_exceptions import SlotIsOccupiedError


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


@pytest.fixture
def players():
    p1 = select_player("player1")
    p2 = select_player("player2", player_picked=p1)
    return [p1, p2]


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


def test_board_walker(win_board):
    init_pos = (1, 1)
    game = GameConfig(3, 1)
    win_pos = board_walker(game.nr_tokens_to_win, init_pos, win_board)
    assert win_pos == ((0, 0), (1, 1), (2, 2))


def test_no_wins(win_board):
    init_pos = (1, 0)
    game = GameConfig(3, 1)
    no_wins = board_walker(game.nr_tokens_to_win, init_pos, win_board)
    assert no_wins == ((1, 0),)


def test_select_player():
    picked_players = ["Player 1", "Player2", "RObot"]
    expected_values = [PlayerTokens.PLAYER_1, PlayerTokens.PLAYER_2, PlayerTokens.CPU]
    for idx, player in enumerate(picked_players):
        assert select_player(player) == expected_values[idx]


def test_select_player_picked(monkeypatch):
    picked_player = PlayerTokens.PLAYER_1
    monkeypatch.setattr("builtins.input", lambda _: "player2")
    assert (
        select_player("player1", player_picked=picked_player) == PlayerTokens.PLAYER_2
    )


def test_switch_player(players):
    all_values = players[:]
    is_playing = choice(players)
    all_values.pop(all_values.index(is_playing))
    new_player = switch_player(players, is_playing)
    assert all_values[0] == new_player


def test_board_dimensions():
    board_rules = GameConfig(4, 1)
    row, column = board_rules.board_dimensions()
    assert row == 6
    assert column == 7
