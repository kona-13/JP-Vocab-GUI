# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 13:57:30 2024

@author: Steven
"""

import tkinter as tk
import csv
import random

#Pulls from .csv
def import_JP_Vocab(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [row for row in reader]

class VocabGenerator:
    def __init__(self, vocab_list, random_order=False):
        self.vocab_list = vocab_list
        self.original_order = vocab_list.copy()
        self.index = 0
        self.random_order = random_order

        if self.random_order:
            random.shuffle(self.vocab_list)

    def get_next_word(self):
        if self.index < len(self.vocab_list):
            word = self.vocab_list[self.index]
            self.index += 1
            return word
        else:
            return None

    def reset_index(self):
        if self.random_order:
            random.shuffle(self.vocab_list)
        else:
            self.vocab_list = self.original_order
        self.index = 0

JP = import_JP_Vocab('vocab.csv')
vocab_generator = VocabGenerator(JP)

yespoints = 0
nopoints = 0
totalpoints = 0
first_press = True

#Updates the text in box
def change_text(event=None):
    global points, first_press
    random_JP = vocab_generator.get_next_word()
    stripped_random_JP_1 = random_JP[1].replace("(", "").replace(")", "")  # Remove brackets

    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)

    if random_JP[0] == stripped_random_JP_1:
        text_widget.insert(tk.END, f"{random_JP[0]}", "kanji")
    else:
        text_widget.insert(tk.END, f"{random_JP[0]}\n", "kanji")
        text_widget.insert(tk.END, f"{random_JP[1]}", "kana")

    text_widget.tag_configure("center", justify="center")
    text_widget.tag_add("center", "1.0", "end")
    text_widget.config(state=tk.DISABLED)

    if first_press:
        first_press = False
        reveal_button.config(state=tk.NORMAL)
        button.grid_forget()

    reveal_button.config(state=tk.NORMAL)
    update_points_label()



#Shows meaning + disables reveal button
def reveal_meaning():
    global points, first_press
    if first_press:
        first_press = False
    button.grid_forget()  # Hide the button after the first press

    selected_entry = text_widget.get("1.0", "1.0 lineend").strip()  # Get the first line (random_JP[0])

    for index, random_JP in enumerate(JP, start=1):
        stripped_random_JP_1 = random_JP[1].replace("(", "").replace(")", "")  # Remove brackets
        entry_text = random_JP[0]
        if entry_text == selected_entry or stripped_random_JP_1 == selected_entry:
            meaning = random_JP[2]  # Depends on which CSV

            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)

            text_widget.insert(tk.END, f"{random_JP[0]}", "kanji")
            text_widget.insert(tk.END, f"\n{random_JP[1]}", "kana")
            text_widget.insert(tk.END, f"\nMeaning: {meaning}")

            text_widget.tag_configure("center", justify="center")
            text_widget.tag_add("center", "1.0", "end")
            text_widget.config(state=tk.DISABLED)

            reveal_button.config(state=tk.DISABLED)
            break
    else:
        print("No match found.")

def click_no():
    global nopoints, totalpoints
    nopoints +=1
    totalpoints +=1
    change_text()

def click_yes():
    global yespoints, totalpoints
    totalpoints+=1
    yespoints += 1
    change_text()

def update_points_label():
    points_label.config(text=f"Total: {totalpoints}\n Correct: {yespoints}\n Incorrect: {nopoints}")
    
def reset_quiz():
    global yespoints, nopoints, totalpoints, first_press, vocab_generator, JP
    yespoints = 0
    nopoints = 0
    totalpoints = 0
    first_press = True

    # Re-import the CSV to ensure a fresh start
    JP = import_JP_Vocab('vocab.csv')

    # Create a new VocabGenerator instance
    vocab_generator = VocabGenerator(JP, random_order=vocab_generator.random_order)

    # Reset the VocabGenerator index to 0 considering the order mode
    vocab_generator.reset_index()
    change_text()
    
    
#Help window stuff   
def helpwindow():
    popup = tk.Toplevel(root)
    popup.title("Help")
    popup.geometry("150x300")
    popup.configure(bg='#5D5F5E')
    popup.resizable(False, False)
    
    
    label = tk.Label(popup, text="Controls:\n\nYes: y or z\nNo: n or x\nReveal: r or space\nReset: 1\nCopy: ctrl + c\n", fg='white', bg='#5D5F5E', font=('Noto Sans CJK JP', 11, 'bold'))
    label.pack(padx=10, pady=10)   
  
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)
    
def open_order_mode_window():
    global order_mode_var  # Add this line to make order_mode_var global
    order_mode_window = tk.Toplevel(root)
    order_mode_window.title("Order Mode")
    order_mode_window.geometry("200x100")
    order_mode_window.configure(bg='#5D5F5E')
    order_mode_window.resizable(False, False)

    # Radio buttons for selecting order mode
    order_mode_var = tk.IntVar()
    order_mode_var.set(0)  # Default to in order

    in_order_radio = tk.Radiobutton(order_mode_window, text="In Order", variable=order_mode_var, value=0)
    in_order_radio.grid(row=0, column=0, pady=5)

    random_order_radio = tk.Radiobutton(order_mode_window, text="Random", variable=order_mode_var, value=1)
    random_order_radio.grid(row=1, column=0, pady=5)
    
    def update_order_mode():
        global vocab_generator
        vocab_generator = VocabGenerator(JP, random_order=(order_mode_var.get() == 1))
        reset_quiz()

    # Bind the function to the radio buttons
    in_order_radio.config(command=update_order_mode)
    random_order_radio.config(command=update_order_mode)


#Tkinter stuff
root = tk.Tk()
root.title("Japanese Vocab")
canvas = tk.Canvas(root, width=700, height=550, bg='#5D5F5E')
canvas.grid(columnspan=5, rowspan=7)
root.eval('tk::PlaceWindow . center')
root.resizable(False, False)

text_widget = tk.Text(root, wrap=tk.WORD, font=('Noto Sans CJK JP', 25), height=5, width=30, bg='#5D5F5E', fg='white')
text_widget.tag_configure("center", justify="center")
text_widget.tag_add("center", "1.0", "end")
text_widget.config(state=tk.DISABLED)
text_widget.place(relx=0.5, rely=0.3, anchor='center')
text_widget.tag_configure("kanji", font=('Noto Sans CJK JP', 40))
text_widget.tag_configure("kana", font=('Noto Sans CJK JP', 20))

button = tk.Button(root, text="Start", command=change_text)
button.grid(row=0, column=2)

reveal_button = tk.Button(root, text="Reveal Meaning", command=reveal_meaning, state=tk.DISABLED)
reveal_button.grid(row=5, column=2, columnspan=1, sticky="nsew")

no_button = tk.Button(root, text="No", command=click_no)
no_button.grid(row=5, column=1, sticky="nsew")

yes_button = tk.Button(root, text="Yes", command=click_yes)
yes_button.grid(row=5, column=3, sticky="nsew")

points_label = tk.Label(root, text="Total: 0\n Correct: 0\n Incorrect: 0", font=('Noto Sans CJK JP', 15), bg='#5D5F5E', fg='white')
points_label.grid(row=6, column=2, pady=(10, 0)) 

help_btn = tk.Button(root, text="Help", command=helpwindow)
help_btn.grid(row=6, column=4)

version = tk.Label(root, text="\n\nVersion 1.05", bg='#5D5F5E', fg='white' )
version.grid(row=6, column=0)

reset_btn = tk.Button(root, text="Reset", command=reset_quiz)
reset_btn.grid(row=0, column=0)

order_mode_button = tk.Button(root, text="Order", command=open_order_mode_window)
order_mode_button.grid(row=6, column=3)

#Bindings
root.bind('r', lambda event: reveal_meaning())
root.bind('z', lambda event: click_yes())
root.bind('x', lambda event: click_no())
root.bind('y', lambda event: click_yes())
root.bind('n', lambda event: click_no())
root.bind('<space>', lambda event: reveal_meaning())
root.bind('1', lambda event: reset_quiz())

# Select all and copy pasta
text_widget.bind("<Control-a>", lambda e: text_widget.tag_add(tk.SEL, "1.0", "end"))
text_widget.bind("<Control-c>", lambda e: root.clipboard_clear() or root.clipboard_append(text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)) or root.update())

root.mainloop()

