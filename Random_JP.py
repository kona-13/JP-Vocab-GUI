# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 19:14:16 2024

@author: Steven
"""

import tkinter as tk
import random
import csv

def import_JP_Vocab(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [row for row in reader] 

JP = import_JP_Vocab('vocab.csv')

yespoints = 0
nopoints = 0
totalpoints = 0
first_press = True

def change_text(event=None):
    global points, first_press
    random_JP = random.choice(JP)
    stripped_random_JP_1 = random_JP[1].replace("(", "").replace(")", "")  # Remove brackets
    if random_JP[0] == stripped_random_JP_1:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"{random_JP[0]}")
        text_widget.tag_configure("center", justify="center")
        text_widget.tag_add("center", "1.0", "end")
        text_widget.config(state=tk.DISABLED)
    else:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"{random_JP[0]}\n{random_JP[1]}")
        text_widget.tag_configure("center", justify="center")
        text_widget.tag_add("center", "1.0", "end")
        text_widget.config(state=tk.DISABLED)
        
    if first_press:
        first_press = False
        reveal_button.config(state=tk.NORMAL)
        button.grid_forget()
    
    reveal_button.config(state=tk.NORMAL)
    update_points_label()

def reveal_meaning():
    global points, first_press
    if first_press:
        first_press = False
    button.grid_forget()  # Hide the button after the first press
        
    selected_entry = text_widget.get("1.0", "1.0 lineend").strip()  # Get the first line (random_JP[0])
    #total_entries = len(JP)

    for index, random_JP in enumerate(JP, start=1):
        stripped_random_JP_1 = random_JP[1].replace("(", "").replace(")", "")  # Remove brackets
        entry_text = random_JP[0]
        if entry_text == selected_entry or stripped_random_JP_1 == selected_entry:
            meaning = random_JP[2]  # Depends on which CSV
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, f"{random_JP[0]}\n{random_JP[1]}\nMeaning: {meaning}")
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
    
def helpwindow():
    popup = tk.Toplevel(root)
    popup.title("Help")
    popup.geometry("150x300")
    popup.configure(bg='#5D5F5E')
    popup.resizable(False, False)
    
    
    label = tk.Label(popup, text="Controls:\n\nYes: y or z\nNo: n or x\nReveal: r or c\nCopy: ctrl + c\n", fg='white', bg='#5D5F5E', font=('Noto Sans CJK JP', 11, 'bold'))
    label.pack(padx=10, pady=10)
   # label2 = tk.Label(popup, text="Yes: y or z\nNo: n or x\nReveal: r or c\nCopy: ctrl + c\n", fg='white', bg='#5D5F5E', font=('Noto Sans CJK JP', 10))
   # label2.pack(padx=10, pady=10)
    
    
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)

root = tk.Tk()
root.title("Random Japanese Word Generator-inator!")
canvas = tk.Canvas(root, width=600, height=450, bg='#5D5F5E')
canvas.grid(columnspan=5, rowspan=7)
root.eval('tk::PlaceWindow . center')
root.resizable(False, False)

text_widget = tk.Text(root, wrap=tk.WORD, font=('Noto Sans CJK JP', 24), height=4, width=30, bg='#5D5F5E', fg='white')
text_widget.tag_configure("center", justify="center")
text_widget.tag_add("center", "1.0", "end")
text_widget.config(state=tk.DISABLED)
text_widget.place(relx=0.5, rely=0.3, anchor='center')

button = tk.Button(root, text="Start", command=change_text)
button.grid(row=1, column=2)

reveal_button = tk.Button(root, text="Reveal Meaning", command=reveal_meaning, state=tk.DISABLED)
reveal_button.grid(row=5, column=2, columnspan=1, sticky="nsew")

no_button = tk.Button(root, text="No", command=click_no)
no_button.grid(row=5, column=1, sticky="nsew")

yes_button = tk.Button(root, text="Yes", command=click_yes)
yes_button.grid(row=5, column=3, sticky="nsew")

points_label = tk.Label(root, text="Total: 0\n Correct: 0\n Incorrect: 0", font=('Noto Sans CJK JP', 15), bg='#5D5F5E', fg='white')
points_label.grid(row=6, column=2, pady=(10, 0)) 

help_btn = tk.Button(root, text="Help", command=helpwindow)
help_btn.grid(row=6, column=4, pady=(10, 0))

version = tk.Label(root, text="\n\nVersion 1.0", bg='#5D5F5E', fg='white' )
version.grid(row=6, column=0)

root.bind('r', lambda event: reveal_meaning())
root.bind('c', lambda event: reveal_meaning())
root.bind('z', lambda event: click_yes())
root.bind('x', lambda event: click_no())

# Binding for text widget copying
text_widget.bind("<Control-a>", lambda e: text_widget.tag_add(tk.SEL, "1.0", "end"))
text_widget.bind("<Control-c>", lambda e: root.clipboard_clear() or root.clipboard_append(text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)) or root.update())

root.mainloop()
