# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 16:47:11 2024

@author: Steven
"""
import tkinter as tk
import random
import csv



def import_JP_Vocab(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [row for row in reader]


#JP = import_JP_Vocab('JLPT4_Vocab_v0.1.csv')
JP = import_JP_Vocab('JP_Vocab_v1.csv')


#Pulls Random Word from the Array
def change_text(event=None):
    random_JP = random.choice(JP)
    stripped_random_JP_1 = random_JP[1].replace("(", "").replace(")", "")  # Remove brackets
    if random_JP[0] == stripped_random_JP_1:
        label.config(text=f"{random_JP[0]}")
    else:
        label.config(text=f"{random_JP[0]}\n{random_JP[1]}")
    
    reveal_button.config(state=tk.NORMAL)

def reveal_meaning():
    selected_entry = label.cget("text").split("\n")[0].strip()  # Get the first line (random_JP[0]) and remove leading/trailing whitespaces
    total_entries = len(JP)

    for index, random_JP in enumerate(JP, start=1):
        stripped_random_JP_1 = random_JP[1].replace("(", "").replace(")", "")  # Remove brackets
        entry_text = random_JP[0]
        print(f"Checking Entry #{index}/{total_entries} - Entry Text: '{entry_text}', Selected Entry: '{selected_entry}'")
        if entry_text == selected_entry or stripped_random_JP_1 == selected_entry:
            print("Match Found!")
            #meaning = random_JP[3]
            meaning = random_JP[2] # Depends on which CSV
            label.config(text=f"{random_JP[0]}\n{random_JP[1]}\nMeaning: {meaning}")
            reveal_button.config(state=tk.DISABLED)
            break
    else:
        print("No match found.")




#Misc Program Stuff - self explanitory    
root = tk.Tk()
root.title("Random Japanese Word Generator-inator!")
canvas = tk.Canvas(root, width=600, height=450, bg='#5D5F5E')
canvas.grid (columnspan=5, rowspan=7)
root.resizable(False, False)



label = tk.Label(root, text="Click the button, or press space for new word", font=('Noto Sans CJK JP', 25), wraplength=300, bg='#5D5F5E', fg='white')
label.place(relx=0.5, rely=0.3, anchor='center')

button = tk.Button(root, text="New Word", command=change_text)
button.grid(row=4, column=2)

reveal_button = tk.Button(root, text="Reveal Meaning", command=reveal_meaning, state=tk.DISABLED)
reveal_button.grid(row=5, column=2)

root.bind('<space>', change_text)
root.bind('n', change_text)
root.bind('r', lambda event: reveal_meaning())

root.mainloop()