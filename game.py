import os
from random import choice
import tkinter as tk
from tkinter import messagebox
from functools import partial

class Game:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title('Hangman')
        self.main_window.geometry('600x400')
        self.main_window.eval('tk::PlaceWindow . center')
        self.main_window.configure(bg='lavender')
        self.create_widgets()
        self.word = self.choose_random_word()
        self.progress = '_' * len(self.word)
        self.wrong_letters = 0
        self.word_list = []
        self.used_letters = [] 
        self.print_progress(self.progress)
        tk.mainloop()

    def create_widgets(self):
        # Frames
        self.top_frame = tk.Frame(self.main_window)
        self.top_frame.pack(pady=10)
        self.dash_frame = tk.Frame(self.main_window)
        self.dash_frame.pack(pady=5)
        self.let1_frame = tk.Frame(self.main_window)
        self.let1_frame.pack(pady=5)
        self.let2_frame = tk.Frame(self.main_window)
        self.let2_frame.pack(pady=5)
        self.let3_frame = tk.Frame(self.main_window)
        self.let3_frame.pack(pady=5)

        # Hangman images
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_lst = [
            tk.PhotoImage(file=os.path.join(current_dir, f'hangman_{i}.png'))
            for i in range(7)
        ]
        self.image_label = tk.Label(self.top_frame, image=self.image_lst[0])
        self.image_label.pack()

        # Word display
        self.dashes = tk.StringVar()
        self.display_word = tk.Label(self.dash_frame, textvariable=self.dashes, bg='lavender', fg='black')
        self.display_word.pack()
        self.guess = tk.StringVar()

        # Letter buttons
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        frames = [self.let1_frame, self.let2_frame, self.let3_frame]
        self.button_dict = {}

        for i, letter in enumerate(alphabet):
            frame = frames[i // 9]  # Distribute letters evenly across rows
            button = tk.Button(frame, text=letter, padx=5, bg='lightblue', fg='white',
                               activebackground='blue', activeforeground='white',
                               command=partial(self.hide_button, letter))
            
            # Hover effect
            button.bind("<Enter>", lambda e, b=button: b.configure(bg='darkblue'))
            button.bind("<Leave>", lambda e, b=button: b.configure(bg='lightblue'))

            self.button_dict[letter] = button
            button.pack(side='left')

        # Quit button
        self.quit = tk.Button(self.let3_frame, text='QUIT', padx=5, command=self.main_window.destroy, fg='red')
        self.quit.pack(side='left')

    def choose_random_word(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, 'words.txt'), 'r') as file:
            word_list = [line.strip() for line in file]
        return choice(word_list)

    def hide_button(self, letter):
        """Handles the logic for checking the guessed letter and updating UI."""
        if letter in self.button_dict:
            self.button_dict[letter].pack_forget()

        guess = letter.lower()
        self.guess.set(guess)

        if self.progress != self.word and self.wrong_letters < 6:
            if guess in self.word:
                self.progress = self.update_progress(self.word, self.progress, guess)
                self.dashes.set(self.progress)

                if self.progress == self.word:
                    self.win_message(self.word)
                    self.play_again()
            else:
                self.wrong_letters += 1
                self.image_label.configure(image=self.image_lst[self.wrong_letters])

                if self.wrong_letters == 6:
                    self.lose_message(self.word)
                    self.play_again()
        else:
            self.win_message(self.word)

    def update_progress(self, word, current_progress, guessed_letter):
        """Reveals the guessed letter in the word."""
        return "".join(guessed_letter if word[i] == guessed_letter else current_progress[i] for i in range(len(word)))

    def print_progress(self, current_progress):
        self.dashes.set(current_progress)

    def win_message(self, word):
        self.dashes.set(f'Congratulations, you won! The word was: {word}')

    def lose_message(self, word):
        self.dashes.set(f'Sorry you lost. The word was: {word}')

    def play_again(self):
        """Asks the user if they want to replay the game."""
        replay = messagebox.askquestion('Play Again', 'Do you want to play again?')
        if replay == 'yes':
            self.reset_game()
        else:
            self.main_window.destroy()

    def reset_game(self):
        """Resets the game state for a new round."""
        self.top_frame.destroy()
        self.dash_frame.destroy()
        self.let1_frame.destroy()
        self.let2_frame.destroy()
        self.let3_frame.destroy()
        self.create_widgets()
        self.word_list.append(self.word)
        while self.word in self.word_list:
            self.word = self.choose_random_word()
        self.progress = '_' * len(self.word)
        self.print_progress(self.progress)
        self.wrong_letters = 0

play = Game()
