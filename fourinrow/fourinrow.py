# -*- coding: utf-8 -*-
"""Four-in-a-row Game"""
from random import choice
from game.game_view import intro_screen
from game.game_model import (
    select_player,
    GameConfig,
    game_set_config,
    BoardValues,
    show_board,
    select_a_slot,
    board_walker,
    switch_player,
)

# TODO: Initialize game
#  Welcome screen
#  Select Players -> p1 and p2
#  Set nr minimum a like to win and nr rounds

# TODO: Loop Game
#  Pick random player
#  Add token to slot
#  Check slot is empty
#  Check if placed token equals win
#  Switch player
#  Loop until winner, repeat nr of rounds
#  Keep score


def main():
    """Runs game"""
    print(intro_screen())
    counter = 0
    player_1 = select_player()
    player_2 = select_player(player_name=player_1.name, player_picked=player_1)
    nr_tokens_to_win, nr_rounds = game_set_config()
    game_rules = GameConfig(nr_tokens_to_win, nr_rounds)
    nr_columns, nr_rows = game_rules.board_dimensions()
    game_board = BoardValues(nr_columns, nr_rows)
    current_player = choice([player_2, player_1])
    while counter < nr_rounds:
        print()
        print(f"{current_player.name} - {current_player.value} PLAYING -")
        print()
        show_board(game_board.board)
        board_cords = select_a_slot(game_board.board)
        game_board.set_board_value(board_cords, current_player.value)
        tiles_hit = board_walker(nr_tokens_to_win, board_cords, game_board)
        show_board(game_board.board)
        if len(tiles_hit) == nr_tokens_to_win:
            game_board = BoardValues(nr_columns, nr_rows)
            print(f"{current_player.name} -{current_player.value}  - Won !")
            counter += 1
            print()
            print("- New round- ")
            print()
            continue
        current_player = switch_player(
            [player_1, player_2], current_player=current_player
        )


if __name__ == "__main__":
    main()
