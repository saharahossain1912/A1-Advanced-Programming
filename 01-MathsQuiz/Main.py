from tkinter import *
from tkinter import messagebox 
import random 

def displayMenu(): #this displays the difficulty selection menu
    def set_level(level): 
        nonlocal selected_level  
        selected_level = level
        menu.destroy()  

    menu = Toplevel(root)  #Created a new pop-up window for difficulty selection
    menu.title("Select Difficulty")
    menu.geometry("320x250")
    menu['bg'] = "#988dad"

    Label(menu, text="DIFFICULTY LEVEL", font=("Arial", 15, "bold"), fg="black", bg="#988dad").pack(pady=15)
    btn_style = {"width": 10, "font": ("Arial", 12, "bold"), "bg": "#D6CA98", "fg": "black", "activebackground": "#D6CA98"}
    
    Button(menu, text="1.  Easy", command=lambda: set_level(1), **btn_style).pack(pady=5)
    Button(menu, text="2.  Moderate", command=lambda: set_level(2), **btn_style).pack(pady=5)
    Button(menu, text="3.  Advanced", command=lambda: set_level(3), **btn_style).pack(pady=5)

    selected_level = None
    menu.grab_set()  
    root.wait_window(menu)
    return selected_level

def randomInt(level):
    if level == 1:
        return random.randint(1, 9)
    elif level == 2:
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)

def decideOperation():
    return random.choice(['+', '-']) 

def displayProblem(level):
    #Generates and returns a random arithmetic problem and its answer.
    n1 = randomInt(level) 
    n2 = randomInt(level)
    op = decideOperation()

    if op == '-' and n2 > n1:  #so that subtraction does not result in negative numbers
        n1, n2 = n2, n1

    question = f"{n1} {op} {n2}"
    correct_answer = eval(question)
    return question, correct_answer

def isCorrect(user_answer, correct_answer):
    try:
        return int(user_answer) == correct_answer
    except ValueError:
        return  False

def displayResults(score):
    if score >= 90:
        rank = "A+"
    elif score >= 80:
        rank = "A "
    elif score >= 70:
        rank = "B"
    elif score >= 60:
        rank = "C"
    else:
        rank = "Try Again"
    
    result = Toplevel(root) #result pop-up window
    result.title("Quiz Results")
    result.geometry("300x150")
    result['bg'] = "#988dad"
    
    Label(result, text=f"Your final score: {score}/100", font=("Arial", 13, "bold"), fg="black", bg="#988dad").pack(pady=10)
    Label(result, text=f"Rank: {rank}", font=("Arial", 12, "bold"), fg="black", bg="#988dad").pack(pady=5)
    Button(result, text="OK", font=("Arial", 11, "bold"), bg="#D6CA98", fg="black",
           activebackground="#D6CA98", command=result.destroy).pack(pady=10)

    result.grab_set()
    root.wait_window(result)

def simple_prompt(prompt_text):
    #Pop-up window to get user's answer for a question.
    prompt = Toplevel(root)
    prompt.title("Answer")
    prompt.geometry("300x150")
    prompt['bg'] = "#988dad"

    Label(prompt, text=prompt_text, font=("Arial", 12, "bold"), fg="black", bg="#988dad").pack(pady=10)
    entry = Entry(prompt, font=("Arial", 12))
    entry.pack(pady=5)
    entry.focus()
    result = {'value': None}

    def submit():
        result['value'] = entry.get()  #Stores user input
        prompt.destroy()

    #editing submit button
    Button(prompt, text="Submit", font=("Arial", 11, "bold"), bg="#D6CA98", fg="black",
           activebackground="#D6CA98", command=submit).pack(pady=10)

    prompt.grab_set() 
    root.wait_window(prompt)
    return result['value']

def startQuiz():
    level = displayMenu()
    if not level:
        return 
    
    score = 0
    for q in range(1, 11): #loop through 10 questions
        question, answer = displayProblem(level)
        user_ans = simple_prompt(f"Q{q}: {question} =")
        
        if isCorrect(user_ans, answer):
            messagebox.showinfo("Result", "✅ Correct! +10 points")
            score += 10
        else:
            user_ans = simple_prompt("❌ Wrong! Try again:")
            if isCorrect(user_ans, answer):
                messagebox.showinfo("Result", "✅ Correct on second try! +5 points")
                score += 5
            else:
                messagebox.showinfo("Result", f"❌ Wrong again! The correct answer was {answer}")

    displayResults(score)
    play_again = messagebox.askyesno("Play Again?", "Would you like to play again?")
    if play_again:
        startQuiz() #Restarts quiz
    else:
        root.destroy() 

root = Tk() 
root.title("Maths Quiz")
root.geometry("400x300")
root['bg'] = "#988dad"
root.resizable(0,0)

Label(root, text="Welcome to the Maths Quiz!", font=("Arial", 17, "bold"), fg="black", bg="#988dad").pack(pady=25)

Button(root, text="Start Quiz", font=("Arial", 13, "bold"), bg="#4E9F3D", fg="white",
       activebackground="#3B7A2A", width=10, command=startQuiz).pack(pady=10)
Button(root, text="Exit", font=("Arial", 13, "bold"), bg="#E84545", fg="white",
       activebackground="#B02A2A", width=10, command=root.destroy).pack(pady=10)

root.mainloop()

"""REFERENCES
1. Code for random arithmetic questions adapted from:
  "Python random integer examples" - https://www.w3schools.com/python/ref_random_randint.asp
2. Python GUI Development- https://www.youtube.com/watch?v=ibf5cx221hk
3. Input in Tkinter using Entry widgets- https://www.youtube.com/watch?v=Y3ce9R46f0o
"""
