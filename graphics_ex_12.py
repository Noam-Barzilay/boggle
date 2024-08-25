import tkinter as tk
import game_display


""" creating the opening screen """

# creating the tkinter root object
root = tk.Tk()
# creating the layout
root.geometry("850x550")

# creating the labels
greeting = tk.Label(text="Welcome to Boggle!", bg="yellow", font=1, height=20, width=100)
# creating the start button, and if pressed, go to main screen
start_game_button = tk.Button(text="START GAME", font=1, height=10, width=150, command=game_display.Board)
# inserting an image
img = tk.PhotoImage(file="picture.png")
label_img = tk.Label(root, image=img)

# packing the objects
label_img.pack(side=tk.LEFT)
greeting.pack()
start_game_button.pack()
root.mainloop()










