import random
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
from functools import partial

class Game:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title('Hangman')
        self.main_window.geometry('400x250')
        self.main_window.configure(bg= 'thistle2')
        self.create_widgets()
        self.word = self.choose_random_word()
        self.progress = '_'*len(self.word)
        self.wrong_letters = 0
        self.word_list = []
        self.used_letters = []      #Append used letters to this list then loop through and recreate buttons for subsequent games
        self.print_progress(self.progress)
        tk.mainloop()
    
    def create_widgets(self):
        #Frames
        self.top_frame = tk.Frame(self.main_window)
        self.top_frame.pack()
        self.dash_frame = tk.Frame(self.main_window)
        self.dash_frame.pack()
        self.let1_frame = tk.Frame(self.main_window)
        self.let1_frame.pack()
        self.let2_frame = tk.Frame(self.main_window)
        self.let2_frame.pack()
        self.let3_frame = tk.Frame(self.main_window)
        self.let3_frame.pack()

        # Progression pictures for hangman drawing, changes with every wrong guess until person is fully drawn
        self.image = tk.PhotoImage(file="hangman.png")
        self.image1 = tk.PhotoImage(file="hangman_1.png")
        self.image2 = tk.PhotoImage(file="hangman_2.png")
        self.image3 = tk.PhotoImage(file="hangman_3.png")
        self.image4 = tk.PhotoImage(file="hangman_4.png")
        self.image5 = tk.PhotoImage(file="hangman_5.png")
        self.image6 = tk.PhotoImage(file="hangman_6.png")
        self.image_label =tk.Label(self.top_frame)
        self.image_label.configure(image= self.image)
        self.image_label.pack()
        self.image_lst = [self.image, self.image1, self.image2, self.image3, self.image4, self.image5, self.image6]

        #Word display
        self.dashes = tk.StringVar()
        self.display_word = tk.Label(self.dash_frame, textvariable= self.dashes)
        self.display_word.pack()
        self.guess = tk.StringVar()
        self.guess_label = tk.Label(self.let3_frame, textvariable= self.guess)

        # Letter buttons
        alphabet_row1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',]
        alphabet_row2 = [ 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',]
        alphabet_row3 = ['S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.button_dict = {}
        
        for i in alphabet_row1:
            self.button_dict[i] = tk.Button(self.let1_frame, text = i, padx= 5)
            self.obj = self.button_dict[i]
            self.button_dict[i].configure(command= partial(self.hide_button, self.obj))
            self.button_dict[i].pack(side= 'left')

        for i in alphabet_row2:
            self.button_dict[i] = tk.Button(self.let2_frame, text = i, padx= 5)
            self.obj = self.button_dict[i]
            self.button_dict[i].configure(command=partial(self.hide_button, self.obj))
            self.button_dict[i].pack(side= 'left')

        for i in alphabet_row3:
            self.button_dict[i] = tk.Button(self.let3_frame, text = i, padx= 5)
            self.obj = self.button_dict[i]
            self.button_dict[i].configure(command=partial(self.hide_button, self.obj))
            self.button_dict[i].pack(side= 'left')
        self.quit = tk.Button(self.let3_frame, text= 'QUIT', padx= 5, command= self.main_window.destroy, fg= 'red')
        self.quit.pack(side= 'left')

    def choose_random_word(self):
        file = open('words.txt','r')
        word_list = file.readlines()
        word_list = [sub.replace('\n', '') for sub in word_list]
        word = random.choice(word_list)
        return word

    def hide_button(self, widget):
        widget.pack_forget()            #Makes button disappear after being clicked
        guess = widget.cget('text')     #Retrieves guessed letter from button pressed
        guess = guess.lower()
        self.guess.set(guess)
        if self.progress != self.word and self.wrong_letters < 6:   #If word hasn't been fully guessed and user has not used all 6 guesses
            if guess in self.word:      #Entire conditional updates display to show progress or win/lose status
                self.update_progress(self.word, self.progress, guess)
                self.progress = self.update_progress(self.word, self.progress, guess)
                self.dashes.set(self.progress)
                if self.progress == self.word:
                    self.win_message(self.word)
                    self.play_again()
                else:
                    pass
            elif guess not in self.word and self.wrong_letters < 5:
                self.wrong_letters += 1
                x = self.wrong_letters
                self.image_label.configure(image= self.image_lst[x])
            else:
                self.wrong_letters += 1
                x = self.wrong_letters
                self.image_label.configure(image= self.image_lst[x])
                self.lose_message(self.word)
                self.play_again()
        else:
            self.win_message(self.word)
            print('You won')
    
    def update_progress(self, word, current_progress, guessed_letter):
        if guessed_letter in word:
            word_list = list(current_progress)
            for i in range(len(word)):
                if word[i] == guessed_letter:
                    word_list[i] = guessed_letter
            new_progress = ''.join(word_list)
        return new_progress
    
    def print_progress(self, current_progress):
        self.dashes.set(current_progress)
    
    def win_message(self, word):
        self.dashes.set(f'Congratulations, you won! The word was: {word}')
    
    def lose_message(self, word):
        self.dashes.set(f'Sorry you lost. The word was: {word}')

    def play_again(self):
        self.replay = tk.messagebox.askquestion('Play Again', 'Do you want to play again?')
        if self.replay == 'yes':
            self.top_frame.destroy()
            self.dash_frame.destroy()
            self.let1_frame.destroy()
            self.let2_frame.destroy()
            self.let3_frame.destroy()
            self.create_widgets()
            self.word_list.append(self.word)
            while self.word in self.word_list:
                self.word = self.choose_random_word()
            self.progress = '_'*len(self.word)
            self.print_progress(self.progress)
            self.wrong_letters = 0
        else:
            self.main_window.destroy()

play = Game()
