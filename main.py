from tkinter import *
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    french_words_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    french_words_data = pandas.read_csv("data/french_words.csv")
finally:
    french_words_dict = french_words_data.to_dict(orient="records")
current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(french_words_dict)
    canvas.itemconfigure(card_title, text="French", fill="black")
    canvas.itemconfigure(card_text, text=f"{current_card['French']}", fill="black")
    canvas.itemconfigure(canvas_image, image=card_front)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfigure(canvas_image, image=card_back)
    canvas.itemconfigure(card_title, text="English", fill="white")
    canvas.itemconfigure(card_text, text=f"{current_card['English']}", fill="white")


def remove_card():
    global french_words_data, french_words_dict
    if len(french_words_dict) <= 0:
        messagebox.showinfo(title="Congratulations!!", message="You've mastered all the words.\nNow restarting from the beginning.\n"
                                                               "Add new words if you would like.")
        french_words_data = pandas.read_csv("data/french_words.csv")
        french_words_dict = french_words_data.to_dict(orient="records")
    else:
        french_words_dict.remove(current_card)
        pandas.DataFrame(french_words_dict).to_csv("data/words_to_learn.csv", index=False)
        next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
card_text = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))

check_mark_image = PhotoImage(file="images/right.png")
known_btn = Button(image=check_mark_image, bg=BACKGROUND_COLOR, highlightthickness=0, borderwidth=0,
                   command=remove_card)
wrong_image = PhotoImage(file="images/wrong.png")
unknown_btn = Button(image=wrong_image, bg=BACKGROUND_COLOR, highlightthickness=0, borderwidth=0, command=next_card)

canvas.grid(row=0, column=0, columnspan=2)
unknown_btn.grid(row=1, column=0)
known_btn.grid(row=1, column=1)
next_card()

window.mainloop()
