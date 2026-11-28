import tkinter as tk
from tkinter import messagebox

# Score variables
c_ans = 0
w_ans = 0
question_no = 0

# Questions and answers
questions = [
    ("What is the capital of India?", "delhi"),
    ("What is the capital of Andhra Pradesh?", "amaravati")
]

def check_answer():
    global c_ans, w_ans, question_no

    answer = entry.get().lower().strip()

    if answer == "":
        messagebox.showwarning("Warning", "Please enter your answer!")
        return

    correct_answer = questions[question_no][1]

    if answer == correct_answer:
        c_ans += 1
        result_label.config(text="Correct Answer!", fg="green")
    else:
        w_ans += 1
        result_label.config(
            text="Wrong Answer! Correct answer: " + correct_answer,
            fg="red"
        )

    question_no += 1
    entry.delete(0, tk.END)

    if question_no < len(questions):
        root.after(1000, next_question)
    else:
        root.after(1000, show_result)


def next_question():
    question_label.config(text=questions[question_no][0])
    result_label.config(text="")
    submit_button.config(state="normal")


def show_result():
    question_label.config(text="Quiz Completed!")
    entry.pack_forget()
    submit_button.pack_forget()

    result_label.config(
        text=f"Correct Answers: {c_ans}\n"
             f"Wrong Answers: {w_ans}\n"
             f"Total Questions: {len(questions)}",
        fg="blue"
    )


# Main window
root = tk.Tk()
root.title("Python Quiz Application")
root.geometry("500x350")
root.config(bg="#eaf2f8")

# Heading
heading = tk.Label(
    root,
    text="Python Quiz",
    font=("Arial", 24, "bold"),
    bg="#eaf2f8",
    fg="#154360"
)
heading.pack(pady=20)

# Question
question_label = tk.Label(
    root,
    text=questions[0][0],
    font=("Arial", 16),
    bg="#eaf2f8"
)
question_label.pack(pady=15)

# Answer input
entry = tk.Entry(
    root,
    font=("Arial", 16),
    justify="center"
)
entry.pack(pady=10)

# Submit button
submit_button = tk.Button(
    root,
    text="Submit Answer",
    font=("Arial", 13, "bold"),
    bg="#2874a6",
    fg="white",
    command=check_answer
)
submit_button.pack(pady=15)

# Result label
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 13, "bold"),
    bg="#eaf2f8"
)
result_label.pack(pady=10)

root.mainloop()