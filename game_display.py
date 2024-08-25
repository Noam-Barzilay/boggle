import tkinter as tk

import ex12_utils
import logic
from boggle_board_randomizer import BOARD_SIZE

# declaring constants
GAME_NAME = "BOGGLE"
LOAD = "LOADING GAME..."
NOT_CLICKED = "blue"
CLICKED = "red"
SCORE = "SCORE: {}"
ENTER = "Enter a word"
START = "START GAME"
GREETING = "WELCOME TO BOGGLE!!"
ROUND_TIME = 180  # 180 seconds == 3 minutes
PLAY_AGAIN = "The time is over\n Do you want to play again?"


class Board:
    """Board is the window of the game, displays a board with the randomized letters, time left, score and words that
     have been guessed right. The game is being managed and presented to the player in this window"""

    def __init__(self):
        """constructor of the board object"""
        self.count = ROUND_TIME
        self.buttons = []  # all buttons that will be created together in a for loop next
        self.root = tk.Tk()
        self.button_id = -1  # initial value for a button id
        self.button_name_x = 0
        self.button_name_y = 0
        self.button_name = [0, 0]  # initial location of cube
        self.path = []  # acts like a stack, used to present the path entered by the player
        self.paths_guessed_right = []
        self.words_guessed_right = []
        self.score = 0
        self.boggle = logic.Boggle(logic.words_dict())  # creates a new boggle object, the object helps us to define the
        # board and its solutions
        # now we will create 16 buttons
        self.root.title(GAME_NAME)  # the title of the window
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                self.button_id += 1  # each button has its own unique id, helps us to determine which button was pressed
                # later
                self.button_name_x = x  # button's column
                self.button_name_y = y  # button's row
                self.button_name = tuple([self.button_name_y, self.button_name_x])  # the name of the button tells us
                # its location
                self.buttons.append(tk.Button(self.root, bg=NOT_CLICKED, fg="white", height=6, width=6,
                                              font=("Helvetica", 12),
                                              text=self.boggle.board[y][x],
                                              command=lambda x=self.button_id, y=self.button_name: self.action(x, y)))
                self.buttons[self.button_id].grid(row=3 * y, column=3 * x, rowspan=3, columnspan=3)  # adds the buttons
        self.word = tk.Label(self.root, text=ENTER, justify="center")  # thw word that is being displayed on
        # the screen, we get the word from the path
        self.word.grid(row=1, column=12, rowspan=1, columnspan=3)
        self.check_word = tk.Button(self.root, text="Check Word", bg="blue", fg="white",
                                    font=("Helvetica"), command=self.check_word)  # the check word button, the player
        # clicks it when he wants to know if the word he chose is right
        self.check_word.grid(row=2, column=12, rowspan=1, columnspan=3)  # score the player has earned
        self.score_display = tk.Label(self.root, text="SCORE: 0", justify="center")
        self.score_display.grid(row=11, column=12, rowspan=1, columnspan=3)
        self.words_display = tk.Listbox(self.root, fg="blue", bg="light blue", height=20)  # displays the words that
        # the player has already guessed right
        self.words_display.grid(row=2, column=12, rowspan=20, columnspan=4)
        self.time = tk.Label(self.root, text="", justify="center", font=1)  # time presented in window, 3 min countdown
        self.time.grid(row=0, column=12, columnspan=4)
        self.update_time()
        self.root.mainloop()

    def update_time(self):
        if self.count > 0:
            mins, second = divmod(self.count, 60)
            curr_time = f"{str(mins).zfill(2)}:{str(second).zfill(2)}"
            self.time.config(text=curr_time)
            self.time.after(1000, self.update_time)
            self.count -= 1
        else:  # if time is over
            self.time.config(text="00:00")
            self.root.destroy()  # destroy the current window
            window = PlayAgainWindow()

    def current_word(self):
        """helps present the word the player chose till now, substring of a word or the whole word"""
        word = ex12_utils.converts_path_to_word(self.path, self.boggle.board)
        self.word.config(text=word)

    def action(self, button, button_name):
        """responsible for action when a letter is being clicked"""
        if self.buttons[button].cget('bg') == NOT_CLICKED:  # in case the player clicked a letter that has not been
            # clicked before in this try
            if not self.path:  # if path is empty, i.e this is the first letter of a new try
                self.path.append(button_name)  # adds the location of the letter to the path
                self.buttons[button].config(bg=CLICKED)  # changes the button color in order to know that this letter
                # was being chosen
            elif logic.check_next_coordinate(self.path[-1], button_name):  # checks if the location of the next letter
                # suites the game roles
                self.buttons[button].config(bg=CLICKED)
                self.path.append(button_name)
        else:
            if button_name == self.path[-1]:  # the player wants to remove his last letter choice
                self.path.pop()
                self.buttons[button].config(bg=NOT_CLICKED)  # changes the color again
        self.current_word()  # updates the display of the current substring/ word at each click on a letter

    def check_word(self):
        """responsible in a case the player clicks the check word button, if the word is right: adds score and changes
         all the letters to initial color"""
        if self.boggle.is_solution(self.path):  # checks if the word entered is one of this board solutions
            self.add_score()
            if self.path not in self.paths_guessed_right:  # if the player did not guess this word before
                self.paths_guessed_right.append(self.path)
            word = ex12_utils.converts_path_to_word(self.path, self.boggle.board)
            if word not in self.words_guessed_right:  # if the player did not guess this word before, appends it to the
                # words that the player has already guessed
                self.words_display.insert(len(self.words_guessed_right), word)  # the place of the word in the list is
                # the place of the word in the list of words the player guessed
                self.words_guessed_right.append(word)
            self.score_display.config(text=SCORE.format(self.score))  # updates the score
            self.word.config(text=ENTER)  # updates the place the current word is shown
            self.path = []  # initialize the path
            for button in self.buttons:
                button.config(bg=NOT_CLICKED)  # changes the buttons again to not clicked coloe

    def add_score(self):
        """in case the word entered is correct we want to add score, if the word was entered before (its in the visible
         words list), we will not add score. The score is n^2, when n is the length of the path"""
        word = ex12_utils.converts_path_to_word(self.path, self.boggle.board)
        if word not in self.words_guessed_right:
            self.score += (len(self.path)) ** 2


class StartWindow:
    """ creating the opening screen """

    def __init__(self):
        self.root2 = tk.Tk()
        self.greeting = tk.Label(self.root2, text=GREETING, bg="blue", font=1, height=1, width=40,
                                 fg="white")
        # creating the start button
        self.start_game_button = tk.Button(self.root2, text=START, font=1, height=1, width=40,
                                           command=self.open_game_window, bg= "blue")
        # inserting an image
        img = tk.PhotoImage(file="picture.png")
        self.label_img = tk.Label(self.root2, image=img)
        # packing the objects
        self.label_img.grid(row=1, column=0)
        self.greeting.grid(row=0, column=0)
        self.start_game_button.grid(row=2, column=0)
        self.root2.title(GAME_NAME)
        self.root2.mainloop()
        exit()

    def open_game_window(self):
        """switch from the start game window to the game itself"""
        self.start_game_button.config(text=LOAD)
        self.root2.destroy()
        game = Board()


class PlayAgainWindow:
    """ creating the 'game over' screen """

    def __init__(self):
        self.root3 = tk.Tk()
        self.message = tk.Label(self.root3, text=PLAY_AGAIN, font=1, width=25, height=5, fg="blue")
        self.message.grid(columnspan=10)
        self.yes_decision = tk.Button(self.root3, text="YES", width=40, height=5, command=self.continue_game, bg="blue",
                                      fg="white")
        self.yes_decision.grid(rowspan=1, columnspan=10)
        self.no_decision = tk.Button(self.root3, text="NO", width=40, height=5, command=self.close_program, bg="blue",
                                     fg="white")
        self.no_decision.grid(rowspan=1, columnspan=10)
        self.root3.mainloop()

    def continue_game(self):
        # calling the board object
        self.root3.destroy()
        game = Board()

    def close_program(self):
        self.root3.destroy()
        exit()

