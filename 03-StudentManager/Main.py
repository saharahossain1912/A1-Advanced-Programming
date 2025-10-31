from tkinter import *
from tkinter import messagebox

FILENAME = "03-StudentManager/studentMarks.txt"
BG = "#E6E6FA"         
BUTTON = "#9B59B6"   
TITLE = "#4B0082"  

def load_students(filename=FILENAME): #loads student records from the file.
    students = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return students 
    
    #checking the content of the file
    if not lines:
        return students 
    
    count = int(lines[0])
    data_lines = lines[1:]
    
    for line in data_lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 6: #if there are less than 6 parts in the list, then the line is invalid and skips.
            continue
        code = parts[0] 
        name = parts[1]
        c1, c2, c3, exam = int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5])
        students.append({"code": code, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": exam})
    return students 

def save_students(students, filename=FILENAME): 
    with open(filename, "w", encoding="utf-8") as file: 
        file.write(str(len(students)) + "\n")

        for s in students: #s is each student dictionary in the students list
            line = f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n" 
            file.write(line)

def coursework_total(s):
    return s['c1'] + s['c2'] + s['c3']

def overall_percentage(s):
    total = coursework_total(s) + s['exam'] #here total marks is the sum of coursework total and exam mark
    percentage = (total / 160.0) * 100 
    return percentage

def student_grade(percentage):
    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"

def student_summary_string(s):
    ct = coursework_total(s)
    percentage = overall_percentage(s)
    grade = student_grade(percentage)
    return (f"Name: {s['name']}\n"
            f"Student Number: {s['code']}\n"
            f"Total Coursework: {ct}/60\n"
            f"Exam Mark: {s['exam']}/100\n"
            f"Overall Percentage: {percentage:.2f}%\n"
            f"Grade: {grade}\n")

def refresh_student_menu():
    global student_var, student_menu 
    menu = student_menu["menu"]
    menu.delete(0, "end")
    names = [f"{s['name']} ({s['code']})" for s in students]

    if not names: 
        student_var.set("")
    else:
        student_var.set(names[0]) 
    for name in names:
        menu.add_command(label=name, command=lambda v=name: student_var.set(v))

def clear_text(): #clearing the result text area in the UI
    result_text.config(state=NORMAL)
    result_text.delete(1.0, END)
    result_text.config(state=DISABLED)

#to add text to the result text area in the UI
def append_text(txt):
    result_text.config(state=NORMAL)
    result_text.insert(END, txt + "\n")
    result_text.config(state=DISABLED)

#Fuction when user clicks "View All Student Records" button
def show_all_records():
    clear_text()
    if not students: 
        append_text("No student records found.") 
        return 
    total_pct = 0.0 #to calculate the average percentage of all students
    for s in students:
        append_text(student_summary_string(s))  
        append_text("-" * 40)
        total_pct += overall_percentage(s)
    avg = total_pct / len(students)
    append_text(f"Number of students: {len(students)}")
    append_text(f"Average percentage: {avg:.2f}%")

def show_individual_record():
    sel = student_var.get()
    if not sel:
        messagebox.showinfo("Select student", "No student selected.")
        return
    if "(" in sel and sel.endswith(")"): 
        code = sel.split("(")[-1].strip(")") 
    else:
        code = sel

    s = next((x for x in students if x['code'] == code), None) #searches for the student with the matching code in the students list
    clear_text()
    if not s:
        append_text("Student not found.")
        return
    append_text(student_summary_string(s))

def show_highest():
    clear_text()
    if not students:
        append_text("No student records found.")
        return
    best = max(students, key=lambda x: coursework_total(x) + x['exam'])
    append_text("Student with highest total score:")
    append_text(student_summary_string(best))

def show_lowest():
    clear_text()
    if not students:
        append_text("No student records found.")
        return
    worst = min(students, key=lambda x: coursework_total(x) + x['exam'])
    append_text("Student with lowest total score:")
    append_text(student_summary_string(worst))

#Extension Task
def sort_records():
    def do_sort():
        order = var.get()
        if order == "Ascending":
            students.sort(key=lambda x: coursework_total(x) + x['exam'])
        else:
            students.sort(key=lambda x: coursework_total(x) + x['exam'], reverse=True)
        refresh_student_menu() 
        save_students(students) 
        top.destroy() 
        show_all_records()

    top = Toplevel(root) #pop up window which will appear when user clicks "Sort Records" button.
    top.title("Sort Records")
    top.config(bg=BG) 
    Label(top, text="Sort by overall score:", bg=BG, fg=TITLE, font=("Arial", 12, "bold")).pack(padx=10, pady=8)
    var = StringVar(value="Descending")
    Radiobutton(top, text="Ascending", variable=var, value="Ascending", bg=BG).pack(anchor="w", padx=12)
    Radiobutton(top, text="Descending", variable=var, value="Descending", bg=BG).pack(anchor="w", padx=12)
    Button(top, text="Sort", command=do_sort, bg=BUTTON, fg="white").pack(pady=10)

def add_record():
    def do_add():
        code = ent_code.get().strip()
        name = ent_name.get().strip()
        try:
            c1 = int(ent_c1.get()); c2 = int(ent_c2.get()); c3 = int(ent_c3.get()); exam = int(ent_exam.get())
        except ValueError:
            messagebox.showerror("Invalid", "Please enter integer marks.")
            return
        if int(code) < 1000 or int(code) > 9999:
            messagebox.showerror("Invalid", "Student code must be between 1000 and 9999.")
            return
        if any(s['code'] == code for s in students):
            messagebox.showerror("Duplicate", "Student code already exists.")
            return
        students.append({"code": code, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": exam})
        save_students(students)
        refresh_student_menu()
        top.destroy() 
        show_all_records()
    
    top = Toplevel(root) #popup window for adding a new student
    top.title("Add Student")
    top.config(bg=BG)
    Label(top, text="Add New Student", bg=BG, fg=TITLE, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=8)
    Label(top, text="Code:", bg=BG).grid(row=1, column=0, sticky="e", padx=5, pady=2)
    ent_code = Entry(top); ent_code.grid(row=1, column=1, padx=5, pady=2)
    Label(top, text="Name:", bg=BG).grid(row=2, column=0, sticky="e", padx=5, pady=2)
    ent_name = Entry(top); ent_name.grid(row=2, column=1, padx=5, pady=2)
    Label(top, text="Course 1 (0-20):", bg=BG).grid(row=3, column=0, sticky="e", padx=5, pady=2)
    ent_c1 = Entry(top); ent_c1.grid(row=3, column=1, padx=5, pady=2)
    Label(top, text="Course 2 (0-20):", bg=BG).grid(row=4, column=0, sticky="e", padx=5, pady=2)
    ent_c2 = Entry(top); ent_c2.grid(row=4, column=1, padx=5, pady=2)
    Label(top, text="Course 3 (0-20):", bg=BG).grid(row=5, column=0, sticky="e", padx=5, pady=2)
    ent_c3 = Entry(top); ent_c3.grid(row=5, column=1, padx=5, pady=2)
    Label(top, text="Exam (0-100):", bg=BG).grid(row=6, column=0, sticky="e", padx=5, pady=2)
    ent_exam = Entry(top); ent_exam.grid(row=6, column=1, padx=5, pady=2)
    Button(top, text="Add Student", command=do_add, bg=BUTTON, fg="white").grid(row=7, column=0, columnspan=2, pady=10)

def delete_record():
    sel = student_var.get()
    if not sel:
        messagebox.showinfo("Select", "No student selected.")
        return
    code = sel.split("(")[-1].strip(")")
    s = next((x for x in students if x['code'] == code), None)
    if not s:
        messagebox.showinfo("Not found", "Student not found.")
        return
    #to prevent accidental deletions.
    if not messagebox.askyesno("Confirm", f"Delete {s['name']} ({s['code']})?"):
        return
    students.remove(s)
    save_students(students)
    refresh_student_menu()
    show_all_records()

def update_record():
    sel = student_var.get()
    if not sel:
        messagebox.showinfo("Select", "No student selected.")
        return
    code = sel.split("(")[-1].strip(")")
    s = next((x for x in students if x['code'] == code), None)
    if not s:
        messagebox.showinfo("Not found", "Student not found.")
        return
    # popup to update fields
    top = Toplevel(root)
    top.title("Update Student")
    top.config(bg=BG)
    Label(top, text="Update Student", bg=BG, fg=TITLE, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=8)
    Label(top, text="Name:", bg=BG).grid(row=1, column=0, sticky="e", padx=5, pady=2)
    ent_name = Entry(top); ent_name.grid(row=1, column=1, padx=5, pady=2); ent_name.insert(0, s['name'])
    Label(top, text="Course 1:", bg=BG).grid(row=2, column=0, sticky="e", padx=5, pady=2)
    ent_c1 = Entry(top); ent_c1.grid(row=2, column=1, padx=5, pady=2); ent_c1.insert(0, str(s['c1']))
    Label(top, text="Course 2:", bg=BG).grid(row=3, column=0, sticky="e", padx=5, pady=2)
    ent_c2 = Entry(top); ent_c2.grid(row=3, column=1, padx=5, pady=2); ent_c2.insert(0, str(s['c2']))
    Label(top, text="Course 3:", bg=BG).grid(row=4, column=0, sticky="e", padx=5, pady=2)
    ent_c3 = Entry(top); ent_c3.grid(row=4, column=1, padx=5, pady=2); ent_c3.insert(0, str(s['c3']))
    Label(top, text="Exam:", bg=BG).grid(row=5, column=0, sticky="e", padx=5, pady=2)
    ent_exam = Entry(top); ent_exam.grid(row=5, column=1, padx=5, pady=2); ent_exam.insert(0, str(s['exam']))
    def do_update():
        try:
            s['name'] = ent_name.get().strip()
            s['c1'] = int(ent_c1.get()); s['c2'] = int(ent_c2.get()); s['c3'] = int(ent_c3.get()); s['exam'] = int(ent_exam.get())
        except ValueError:
            messagebox.showerror("Invalid", "Please enter integer marks.")
            return
        save_students(students)
        refresh_student_menu()
        top.destroy()
        show_individual_record()
    Button(top, text="Update", command=do_update, bg=BUTTON, fg="white").grid(row=6, column=0, columnspan=2, pady=10)

#creating the main UI window
root = Tk()
root.title("Student Manager")
root.geometry("820x560")
root.config(bg=BG)
root.resizable(0,0)

Label(root, text="Student Manager", bg=BG, fg=TITLE, font=("Arial", 22, "bold")).pack(pady=12)

top_frame = Frame(root, bg=BG)
top_frame.pack(pady=6)

Button(top_frame, text="View All Student Records", command=show_all_records,
       bg=BUTTON, fg="white", width=22, height=2).grid(row=0, column=0, padx=8, pady=6)
Button(top_frame, text="Show Highest Score", command=show_highest,
       bg=BUTTON, fg="white", width=18, height=2).grid(row=0, column=1, padx=8, pady=6)
Button(top_frame, text="Show Lowest Score", command=show_lowest,
       bg=BUTTON, fg="white", width=18, height=2).grid(row=0, column=2, padx=8, pady=6)

mid_frame = Frame(root, bg=BG)
mid_frame.pack(pady=6)

Label(mid_frame, text="View Individual Student Record:", bg=BG, fg=TITLE).grid(row=0, column=0, padx=6)
student_var = StringVar()
student_menu = OptionMenu(mid_frame, student_var, "") 
student_menu.config(width=30)
student_menu.grid(row=0, column=1, padx=6)
Button(mid_frame, text="View Record", command=show_individual_record,
       bg=BUTTON, fg="white", width=12).grid(row=0, column=2, padx=8)

# Extension buttons 
Button(mid_frame, text="Sort Records", command=sort_records,
       bg=BUTTON, fg="white", width=12).grid(row=1, column=0, padx=8, pady=8)
Button(mid_frame, text="Add Student", command=add_record,
       bg=BUTTON, fg="white", width=12).grid(row=1, column=1, padx=8, pady=8)
Button(mid_frame, text="Delete Student", command=delete_record,
       bg=BUTTON, fg="white", width=12).grid(row=1, column=2, padx=8, pady=8)
Button(mid_frame, text="Update Student", command=update_record,
       bg=BUTTON, fg="white", width=12).grid(row=1, column=3, padx=8, pady=8)

result_frame = Frame(root, bg="white", bd=2, relief="sunken") #container for the result text area
result_frame.pack(padx=20, pady=12, fill="both", expand=True)

# Creating scrollbar
scrollbar = Scrollbar(result_frame)
scrollbar.pack(side=RIGHT, fill=Y)

result_text = Text(result_frame, wrap="word", bg="white", fg="black", font=("Arial", 11), yscrollcommand=scrollbar.set)
result_text.pack(fill="both", expand=True, padx=6, pady=6)
scrollbar.config(command=result_text.yview)
result_text.config(state=DISABLED)

students = load_students() #this will load initial student records when program starts
refresh_student_menu()
clear_text()
append_text("Yay! Student records loaded successfully!\nUse the buttons above to:")
append_text("  • View all students or individual records\n  • Find highest/lowest scores\n  • Add, update, or delete students")

root.mainloop()

# ---------- REFERENCES ----------
# File parsing and writing adapted from standard Python file I/O examples.
# UI layout and Tkinter usage adapted from official Tkinter docs and tutorials.
# Python File Handling:
# https://www.w3schools.com/python/python_file_handling.asp
# Tkinter GUI Tutorial:
# https://www.w3schools.com/python/python_tkinter.asp