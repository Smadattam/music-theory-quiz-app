from MusicScale import *
import random
import tkinter as tk
import re

# Define color strings
bg_color_str = "#3B6267"
label_color_str = "#092A2F"
text_color_str = "#587A7F"
win_height = 200
win_width = 200
win_xy_str = "{}x{}".format(win_width, win_height)
global_padding = 10
global question_stack
question_stack = []
scale_widget_list = []
valid_scale_entry_regex = re.compile('^[a-gA-G]$|^[a-gA-G][sfSF]$|^$')


# functions for creating randomized questions
def generate_random_root_note():
    return random.randrange(0, 12, 1)


def generate_random_interval():
    return random.randrange(1, 8, 1)


def find_note_given_key_sig_and_mode():
    key_sig_scale = MusicScale(generate_random_root_note(), 1)
    mode_info = key_sig_scale.get_note_text_from_interval(generate_random_interval())

    key_sig = key_sig_scale.get_note_text_from_interval(1)[0]
    message = "What is the {} ({}) mode of {}?".format(mode_info[1], mode_info[2], key_sig)


def ask_a_question():
    key_sig_scale = MusicScale(generate_random_root_note(), 1)
    mode_info = key_sig_scale.get_note_text_from_interval(generate_random_interval())
    answer = mode_info[0]

    key_sig = key_sig_scale.get_note_text_from_interval(1)[0]
    question = "What is the {} ({}) mode of {}?".format(mode_info[1], mode_info[2], key_sig)

    return question, answer, key_sig_scale


# callback functions for the TKinter QUI window
def clear_all_entries():
    answer_entry.delete(0, 'end')
    for widget_group in scale_widget_list:
        widget_group[2].delete(0, 'end')


def submit_answer():
    global question_stack
    answer = question_stack[0][1]
    if answer_entry.get().lower() == answer.lower():
        message_label.config(text="Correct! Press Next Question to move on")
        next_question_button.config(state=tk.NORMAL)
        answer_button.config(state=tk.DISABLED)
    else:
        message_label.config(text="Incorrect")


def next_question():
    global question_stack
    question_stack.insert(0, ask_a_question())
    question_label.config(text=question_stack[0][0])
    message_label.config(text="")
    next_question_button.config(state=tk.DISABLED)
    answer_button.config(state=tk.NORMAL)
    clear_all_entries()


# function for later development, which will check the users input in the practice window below
def check_scale_entry():
    return -1


# Begin TKinter window
gui = tk.Tk()
gui.title("Music Theory Quiz App")
gui.configure(bg=label_color_str)
gui.minsize(win_width, win_height)

question_frame = tk.Frame(gui, bg=label_color_str)
question_label = tk.Label(question_frame, bg=label_color_str, fg=text_color_str, width=100, text="Press 'Next Question' to proceed")
answer_entry = tk.Entry(question_frame, text="")
message_label = tk.Label(question_frame, bg=label_color_str, fg=text_color_str, text="")
answer_button = tk.Button(question_frame, text="Submit Answer", command=submit_answer)
next_question_button = tk.Button(question_frame, text=">> Next Question >>", command=next_question)

# Frame for the scale entry and label widgets
scale_frame = tk.Frame(gui, bg=label_color_str)
# ToDo: Create a space for the user to enter scale intervals for checking purposes
# labels for scale entry forms below
# for num in range(7):
#    frame = tk.Frame(scale_frame, bg=label_color_str)
#    scale_label = tk.Label(frame, text=MusicScale.num_to_roman(num+1), width=5, fg=text_color_str, bg=label_color_str)
#    scale_entry = tk.Entry(frame, text='', width=5)
#    scale_widget_list.append([frame, scale_label, scale_entry])

question_frame.grid(row=0, column=0, padx=global_padding, pady=global_padding, sticky="ew")
scale_frame.grid(row=1, column=0, padx=global_padding, pady=global_padding)
# ToDo: Create a space for the user to enter scale intervals for checking purposes
# for num in range(7):
#    scale_widget_list[num][0].grid(row=0, column=num)
#    scale_widget_list[num][1].grid(row=0, column=0)
#    scale_widget_list[num][2].grid(row=1, column=0)

question_label.grid(row=0, sticky="e")
message_label.grid(row=1, padx=global_padding, pady=global_padding)
answer_entry.grid(row=2, padx=global_padding, pady=global_padding)
answer_button.grid(row=3, padx=global_padding, pady=global_padding)
next_question_button.grid(row=4, padx=global_padding, pady=global_padding)

gui.mainloop()

