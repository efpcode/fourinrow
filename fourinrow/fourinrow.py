# -*- coding: utf-8 -*-
"""Four-in-a-row Game"""
from fourinrow.game.game_view import intro_screen

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

if __name__ == "__main__":
    print(intro_screen())
