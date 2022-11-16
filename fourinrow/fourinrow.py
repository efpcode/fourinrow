# -*- coding: utf-8 -*-
"""Four-in-a-row Game"""
from game.game_view import intro_screen
from game.game_model import select_player

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
    player_1 = select_player()
    print(player_1.name)
    player_2 = select_player(player_name=player_1.name, player_picked=player_1)
    print(player_1, player_2)


if __name__ == "__main__":
    main()
