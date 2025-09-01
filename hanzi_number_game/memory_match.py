# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 18:59:03 2025

@author: Sonia Singh
"""

import tkinter as tk
import random

#Mandarin numbers 1-8 (for a 4x4 grid, 8 pairs)
mandarin_nums = ['一','二','三','四','五','六','七','八','九','零']
arabic_nums = ['1','2','3','4','5','6','7','8','9','0']

#create pairs (mandarin + arabic) to match
pairs = list(zip(mandarin_nums, arabic_nums))

#For memory match, we want 8 pairs, each appears twice:
#We'll have a list with each pair duplicated twice.
cards = mandarin_nums + arabic_nums
cards *= 1 #currently 16 cards total(8 Mandarin, 8 Arabic)
random.shuffle(cards)

root = tk.Tk()
root.title("Memory Match = Mandarin Edition")
root.geometry("450x500")

#variables to track flipped cards
flipped = []
buttons = {}

def flip_back(btn1, val1, btn2, val2):
    btn1.config(text='?', state="normal")
    btn2.config(text='?', state="normal")
    
#Update the check_match function to increase score on match
def check_match():
    global score
    if len(flipped) == 2:
           first_btn, first_val = flipped[0]
           second_btn, second_val = flipped[1]

           if (first_val in mandarin_nums and second_val == arabic_nums[mandarin_nums.index(first_val)]) or \
              (second_val in mandarin_nums and first_val == arabic_nums[mandarin_nums.index(second_val)]):
               first_btn.config(state="disabled", text=first_val)
               second_btn.config(state="disabled", text=second_val)
               update_score()
           else:
               root.after(1000, lambda: flip_back(first_btn, first_val, second_btn, second_val))
           flipped.clear()

def on_click(btn, val):
    global mandarin_nums, arabic_nums
    if len(flipped) < 2 and (btn, val) not in flipped:
        btn.config(text=val, state="disabled")
        flipped.append((btn, val))
        if len(flipped) == 2:
            root.after(500, check_match)
            
#Create buttons for cards
for index, val in enumerate(cards):
    btn = tk.Button(root, text="?", width=5, height=3,font=("SimSun", 16, "bold"),
                    bg="#acf2bf",            # white background
                    command=lambda b=index: on_click(buttons[b], cards[b]))
    btn.grid(row=index // 5, column=index % 5, padx=8, pady=8)
    buttons[index] = btn
    
score = 0 
matches_needed = len(mandarin_nums) #8 pairs

score_label = tk.Label(root, text=f"Score:{score}")
score_label.grid(row=5, column=0, columnspan=2)

timer_label = tk.Label(root, text="Time: 02:00")
timer_label.grid(row=5, column=2, columnspan=2)

time_left = 120 # seconds

def update_score():
    global score
    score += 1 
    score_label.config(text=f"Score:{score}")
    if score ==matches_needed:
        game_over("You Win!")

def game_over(message):
    global game_running
    game_running = False
    # Disable all buttons
    for btn in buttons.values():
        btn.config(state="disabled")
    # Show message
    global result_label
    result_label = tk.Label(root, text=message, font=("Arial", 14), fg="green")
    result_label.grid(row=6, column=3, sticky="e", padx=5)

global result_label
try:
    result_label.destroy()
except:
    pass
    
def reset_game():
    global flipped, cards, score, time_left

    flipped.clear()
    score = 0
    time_left = 120
    score_label.config(text=f"Score: {score}")
    timer_label.config(text="Time: 02:00")

    # Shuffle cards again
    random.shuffle(cards)

    # Reset all buttons with new values
    for index, btn in buttons.items():
        btn.config(text="?", state="normal")
    
    countdown()
    
game_running = True

def countdown():
    global time_left
    if time_left > 0 and game_running:
        mins, secs = divmod(time_left, 60)
        timer_label.config(text=f"Time: {mins:02d}:{secs:02d}")
        time_left -= 1
        root.after(1000, countdown)
    else:
        game_over("Time's up!")
        
        # Start the timer when the game starts
countdown()

replay_btn = tk.Button(root, text="🔁 Play Again", command=reset_game, font=("Arial", 14), bg="lightblue")
replay_btn.grid(row=7, column=1, columnspan=2, pady=10)
    
root.mainloop()
