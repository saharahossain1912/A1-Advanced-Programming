from tkinter import *
import random

root = Tk()
root.title("Alexa - Tell Me a Joke")
root.geometry("500x300")
root.config(bg="#603866")

display = Label(root, text="Say: Alexa tell me a joke", fg="white", bg="#230e26", wraplength=400, font=("Arial", 14))
display.pack(pady=40)

with open("02-Alexa-tell-me-a-joke\RandomJokes.txt", "r", encoding="utf-8") as file:
    jokes = [line.strip() for line in file if line.strip()]

joke_pairs = [] #Splitting each joke into setup and punchline
for joke in jokes:
    if "?" in joke:
        parts = joke.split("?", 1)
        setup = parts[0].strip() + "?"
        punchline = parts[1].strip()
        joke_pairs.append((setup, punchline))

current_joke = None  #To keep track of current joke

#to show a random joke setup
def tell_joke():
    global current_joke
    current_joke = random.choice(joke_pairs)
    display.config(text=current_joke[0])

#Function to show the punchline
def show_punchline():
    if current_joke:
        display.config(text=current_joke[1])

#Function to quit the program
def quit_app():
    root.destroy()

btn_frame = Frame(root, bg="#230e26")
btn_frame.pack(pady=20)

Button(btn_frame, text="Alexa tell me a joke", command=tell_joke,
       font=("Arial", 12), bg="#4CAF50", fg="white", width=20).grid(row=0, column=0, padx=5, pady=5)

Button(btn_frame, text="Show punchline", command=show_punchline,
       font=("Arial", 12), bg="#2196F3", fg="white", width=20).grid(row=0, column=1, padx=5, pady=5)

Button(btn_frame, text="Next joke", command=tell_joke,
       font=("Arial", 12), bg="#FF9800", fg="white", width=20).grid(row=1, column=0, padx=5, pady=5)

Button(btn_frame, text="Quit", command=quit_app,
       font=("Arial", 12), bg="#f44336", fg="white", width=20).grid(row=1, column=1, padx=5, pady=5)

root.mainloop()