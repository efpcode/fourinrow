# -*- coding: utf-8 -*-
"""Four-in-a-row Game"""
from random import choice

from game.game_model import (
    BoardValues,
    GameConfig,
    board_walker,
    game_set_config,
    select_a_column,
    select_a_slot,
    select_player,
    show_board,
    switch_player,
)
from game.game_view import intro_screen


def game_mode():
    """The funtion return the game mode for four-in-a-row either freeform or classical mode."""
    while True:
        user_input = input("Do you wish to play freeform (y/n): ").lower()
        if not user_input in ["n", "y"]:
            print("Please enter either n or y")
            continue
        if user_input == "y":
            return select_a_slot
        return select_a_column


def main():
    """Runs game"""
    print(intro_screen())
    counter = 0
    player_1 = select_player()
    player_2 = select_player(player_name=player_1.name, player_picked=player_1)
    nr_tokens_to_win, nr_rounds = game_set_config()
    game_rules = GameConfig(nr_tokens_to_win, nr_rounds)
    nr_columns, nr_rows = game_rules.board_dimensions()
    select_token_pos = game_mode()
    game_board = BoardValues(nr_columns, nr_rows)
    current_player = choice([player_2, player_1])
    while counter < nr_rounds:
        print()
        print(f"{current_player.name} - {current_player.value} PLAYING -")
        print()
        show_board(game_board.board)
        board_cords = select_token_pos(game_board.board)
        game_board.set_board_value(board_cords, current_player.value)
        tiles_hit = board_walker(nr_tokens_to_win, board_cords, game_board)
        show_board(game_board.board)
        if BoardValues.is_board_complete(game_board.board):
            counter += 1
            print("- Draw - ")
            print()
            continue
        if len(tiles_hit) == nr_tokens_to_win:
            game_board = BoardValues(nr_columns, nr_rows)
            print(f"{current_player.name} - {current_player.value}  - Won !")
            counter += 1
            print()
            print()
            continue
        current_player = switch_player(
            [player_1, player_2], current_player=current_player
        )


if __name__ == "__main__":
    main()
