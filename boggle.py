import sys

import game_display

"""this file runs the game from the command line"""


def play():
    game = game_display.StartWindow()  # starts the game


if __name__ == '__main__':
    play_boggle = sys.argv[1]
    if play_boggle == "boggle.py":
        play()
