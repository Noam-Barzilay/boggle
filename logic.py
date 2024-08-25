import boggle_board_randomizer
import ex12_utils
import time


def words_dict():
    """converts the boggle_dict to list"""
    f = open("boggle_dict.txt", "r")
    d = f.read().split('\n')
    return d


def check_next_coordinate(coordinate, next_coordinate):
    """check the next coordinate to see if it is in an appropriate location"""
    y = coordinate[0]
    x = coordinate[1]
    optionsList = [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1), (y, x - 1), (y, x + 1), (y + 1, x - 1), (y + 1, x),
                   (y + 1, x + 1)]  # all possible options for the next coordinate
    if next_coordinate in optionsList:
        return True
    return False


def countdown(t, board):
    """ counts from 3 minutes (180 seconds) to 0 """
    while t:
        mins, second = divmod(t, 60)
        curr_time = f"{str(mins).zfill(2)}:{str(second).zfill(2)}"
        board.time.config(text=curr_time)
        time.sleep(1)
        t -= 1


class Boggle:

    def __init__(self, words):
        """boggle game constructor"""
        self.words = words  # list of words that represent the right words in our game
        self.board = boggle_board_randomizer.randomize_board()

    def is_solution(self, path):
        """returns True if a word is a possible solution in the current board"""
        word = ex12_utils.converts_path_to_word(path, self.board)
        return word in self.words

