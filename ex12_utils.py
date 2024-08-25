from boggle_board_randomizer import *

AREA = 3

""" 
the size of the square representing the current cube and its possible choices
excluding itself
 """

"""words_dict load the boggle_dict, used for testing"""


def words_dict():
    """converts the boggle_dict to list"""
    f = open("boggle_dict.txt", "r")
    d = f.read().split('\n')
    return d


# functions to help is_valid_path
def in_bounds(y, x):
    """checks if a single cube is in bounds"""
    return 0 <= y < BOARD_SIZE and 0 <= x < BOARD_SIZE


def _path_in_words_list(board, path, words):
    """checks whether the word represented by the path is in the words list"""
    word = ""
    for coordinate in path:
        y = coordinate[0]
        x = coordinate[1]
        if in_bounds(y, x):  # checks if this cube exists before asking for its value
            word += board[y][x]
    return word in words


def right_coordinates(path):
    """receives a path and returns True if the coordinates are in a right order"""
    for i in range(len(path[:-1])):  # the last coordinate is being tested with the second coordinate from the end
        coordinate = path[i]
        y = coordinate[0]
        x = coordinate[1]
        optionsList = [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1), (y, x - 1), (y, x + 1), (y + 1, x - 1), (y + 1, x),
                       (y + 1, x + 1)]  # all possible options for the next coordinate
        if path[i + 1] not in optionsList:
            # checks whether the next coordinate is in a right place according to the current coordinate
            return False
    return True


def _path_is_valid(path):
    """
    checks the validity of the path's coordinates, if all coordinates in path appear no more than once -
     it means no repetitions of cubes in board
    """
    return all([path.count(coordinate) == 1 for coordinate in path])


def path_in_bounds(path):
    """checks whether all the coordinates in path are in bounds"""
    for coordinate in path:
        y = coordinate[0]
        x = coordinate[1]
        if y < 0 or x < 0 or x >= BOARD_SIZE or y >= BOARD_SIZE:
            return False
    return True


def is_valid_path(board, path, words):
    """checks if the path is a valid path that describes a word that exists in the word collection.
     If true, the function returns the word found. If the path is invalid or the word does not exist in
     the dictionary returns None"""
    if _path_in_words_list(board, path, words) and _path_is_valid(path) and path_in_bounds(path) and right_coordinates(
            path):  # all conditions are true
        return converts_path_to_word(path, board)
    return None


# functions to help find_length_n_paths


def converts_path_to_word(path, board):
    """receives a path representing a word, converts the path to a word by adding the values in each coordinate of the
     path"""
    word = ""
    for coordinate in path:
        y = coordinate[0]
        x = coordinate[1]
        word += board[y][x]
    return word


def word_length(path, board):
    """receives a path representing a word and returns the word length"""
    return len(converts_path_to_word(path, board))


def words_dict_by_length(words, n):
    """receives words list and creates a new words list that contains the words that their length is between n to 2n,
     (here we want to minimize the words list as good as we can, we know each cube contains one or two letters so the
      length of the words we are looking for is between n to 2n)"""
    new = []
    for word in words:
        if n <= len(word) <= 2 * n:
            new.append(word)
    return new


def shorten_by_substring(substring, words):
    """receives a substring and a list of words, returns a new list that contains only the words that starts with the
     substring. This method help us to optimize the backtracking we are doing in the recursive methods,
      we know that the right words won't include the words that do not start with the current path we find, so we update
       the list accordingly"""
    new = []
    for word in words:
        if word.startswith(substring):
            new.append(word)
    return new


def helper_find_length_n_paths(board, y, x, i, length, words, path, res):
    """A recursive method that returns the paths of the words that are in length n that starts in (y,x) cube"""
    if i == length - 1:  # stop condition
        # if we have a right path without the last coordinate, we will check if the path with the last coordinate
        # (the whole path) represents a word in the words list
        if _path_in_words_list(board, path + [(y, x)], words):
            res.append(path + [(y, x)])
            return
    path.append((y, x))  # creates a new possible path
    optionsList = [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1), (y, x - 1), (y, x + 1), (y + 1, x - 1), (y + 1, x),
                   (y + 1, x + 1)]
    # in each cube we can move to maximum 8 different cubes (sides and diagonals)-> included in the options list
    substring = converts_path_to_word(path, board)
    # the current substring is the current word represented by the current path
    words = shorten_by_substring(substring, words)  # reduces the words by the substring
    if words:  # if there are right words
        for option in optionsList:
            if option not in path:  # making sure we are not repeating a cube
                row = option[0]
                col = option[1]
                if in_bounds(row, col):
                    if any(word.startswith(substring) for word in words):
                        # backtracking, continues the recursion only with words that starts with the substring
                        helper_find_length_n_paths(board, row, col, i + 1, length, words, path, res)
    path.pop()
    return res


def find_length_n_paths(n, board, words):
    """returns all the paths in length n in the board that represent words in the words collections"""
    new_words = words_dict_by_length(words, n)
    res = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            cube_res = helper_find_length_n_paths(board, i, j, 0, n, new_words, [], [])
            if cube_res:
                res.extend(cube_res)
            # adds the right words for each cube in the board
    return res


def _helper_find_length_n_words(board, y, x, i, length, words, path, res):
    """returns all the paths in the board that represent words in length n for cube (y,x)"""
    if word_length(path, board) == length - 1:  # if the last coordinate in the path contains 1 letter
        if len(board[y][x]) == 1:
            if _path_in_words_list(board, path + [(y, x)], words):
                res.append(path + [(y, x)])
                if len(path + [(y, x)]) == 1:  # if the word is a letter
                    return [path + [(y, x)]]
                return
    elif word_length(path, board) == length - 2:  # if the last coordinate in the path contains 2 letters
        if len(board[y][x]) == 2:
            if _path_in_words_list(board, path + [(y, x)], words):
                res.append(path + [(y, x)])
                return
    path.append((y, x))
    optionsList = [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1), (y, x - 1), (y, x + 1), (y + 1, x - 1), (y + 1, x),
                   (y + 1, x + 1)]
    substring = converts_path_to_word(path, board)
    words = shorten_by_substring(substring, words)
    if words:  # if there are right words
        for option in optionsList:
            if option not in path:
                row = option[0]
                col = option[1]
                if in_bounds(row, col):
                    if any(word.startswith(substring) for word in words):  # backtracking
                        _helper_find_length_n_words(board, row, col, i + 1, length, words, path, res)
    path.pop()
    return res


def find_length_n_words(n, board, words):
    """returns all the paths in the board that represent words in length n"""
    new_words = words_dict_by_length(words, n)
    res = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            cube_res = _helper_find_length_n_words(board, i, j, 0, n, new_words, [], [])
            if cube_res:
                res.extend(cube_res)
    return res


def max_score_paths(board, words):
    """returns a list of paths that provide the maximum score per game for the board and the collection of words
     provided."""
    result = []
    for word in words:
        lst = find_length_n_words(len(word), board, [word])  # all the paths suits for a word
        if lst:  # if there is a least 1 path
            paths_lengths = [len(path) for path in lst]  # list with the length of the paths the word has
            result.append(lst[paths_lengths.index(
                max(paths_lengths))])  # appends to the result the longest path for the current word
    return result




