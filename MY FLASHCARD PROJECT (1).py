#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[16]:


#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import sqlite3
import random
import speech_recognition as sr

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Flashcard App F088")

        # Show homepage
        self.show_homepage()

    def show_homepage(self):
        # Clear any existing widgets from the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add some introductory text
        intro_label = tk.Label(self.root, text="Welcome to My Flashcard App!", font=('Arial', 20, 'bold'))
        intro_label.configure(bg='yellow',fg='black')
        intro_label.pack(pady=20)
        
        intro_text = tk.Label(self.root, text="A Learning Tool that will help you to remember your studies.", font=('Arial', 14))
        intro_text.configure(bg='yellow',fg='black')
        intro_text.pack(pady=10)
        
        # Add a button to start the app
        start_button = tk.Button(self.root, text="Get Started!", font=('Arial', 16), command=self.start_app)
        start_button.configure(bg='yellow',fg='black')
        start_button.pack(pady=20)

    def start_app(self):
        # Clear any existing widgets from the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Connect to flashcards SQLite database
        self.conn_flashcards = sqlite3.connect("flashcards.db")
        self.cursor_flashcards = self.conn_flashcards.cursor()

        # Create flashcards table if not exists
        self.cursor_flashcards.execute("""CREATE TABLE IF NOT EXISTS flashcards (
                            id INTEGER PRIMARY KEY,
                            question TEXT NOT NULL,
                            answer TEXT NOT NULL
                            )""")
        self.conn_flashcards.commit()

        # Connect to students SQLite database
        self.conn_students = sqlite3.connect("students.db")
        self.cursor_students = self.conn_students.cursor()

        # Create students table if not exists
        self.cursor_students.execute("""CREATE TABLE IF NOT EXISTS students (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            roll_no TEXT NOT NULL,
                            class TEXT NOT NULL
                            )""")
        self.conn_students.commit()

        # Create GUI components for flashcard app
        self.create_app_widgets()

    def create_app_widgets(self):
        # Add the flashcard app widgets here
        self.question_label = tk.Label(self.root, text="Question:", font=('Futura', 16))
        self.question_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.question_entry = tk.Entry(self.root, width=50)
        self.question_entry.grid(row=0, column=1, padx=10, pady=5)

        self.answer_label = tk.Label(self.root, text="Answer:", font=('Arial', 16))
        self.answer_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.answer_entry = tk.Entry(self.root, width=50)
        self.answer_entry.grid(row=1, column=1, padx=10, pady=5)

        self.add_button = tk.Button(self.root, text="Add Flashcard", font=('Arial', 16), command=self.add_flashcard)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.random_question_button = tk.Button(self.root, text="Show Random Question", font=('Arial', 16), command=self.show_random_question)
        self.random_question_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.answer_button = tk.Button(self.root, text="Show Answer", font=('Arial', 16), command=self.show_answer, state=tk.DISABLED)
        self.answer_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.voice_to_text_question_button = tk.Button(self.root, text="Voice to Text (Question)", font=('Arial', 16), command=self.voice_to_text_question)
        self.voice_to_text_question_button.grid(row=5, column=0, padx=10, pady=5, sticky="we")

        self.voice_to_text_answer_button = tk.Button(self.root, text="Voice to Text (Answer)", font=('Arial', 16), command=self.voice_to_text_answer)
        self.voice_to_text_answer_button.grid(row=5, column=1, padx=10, pady=5, sticky="we")

        self.test_button = tk.Button(self.root, text="TEST", font=('Arial', 16), command=self.start_test)
        self.test_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.show_reports_button = tk.Button(self.root, text="Show All Reports", font=('Arial', 16), command=self.show_all_reports)
        self.show_reports_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.color_button = tk.Button(self.root, text="Select Background Color", font=('Arial', 16), command=self.select_background_color)
        self.color_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.current_question = ""
        self.set_random_background()

        # Centering the GUI widgets
        for i in range(9):
            self.root.rowconfigure(i, weight=1)
        for i in range(2):
            self.root.columnconfigure(i, weight=1)

    # Remaining methods remain the same...

        for i in range(2):
            self.root.columnconfigure(i, weight=1)

    def select_background_color(self):
        color = colorchooser.askcolor()[1]  # askcolor returns a tuple, we're interested in the second element
        if color:
            self.root.config(bg=color)

    def add_flashcard(self):
        try:
            question = self.question_entry.get().strip()
            answer = self.answer_entry.get().strip()

            if not question or not answer:
                messagebox.showerror("Error", "Please enter both question and answer.")
                return

            # Insert flashcard into flashcards database
            self.cursor_flashcards.execute("INSERT INTO flashcards (question, answer) VALUES (?, ?)", (question, answer))
            self.conn_flashcards.commit()
            messagebox.showinfo("Success", "Flashcard added successfully.")
            self.question_entry.delete(0, tk.END)
            self.answer_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_random_question(self):
        # Fetch all flashcards from flashcards database
        self.cursor_flashcards.execute("SELECT question FROM flashcards")
        questions = self.cursor_flashcards.fetchall()

        if not questions:
            messagebox.showinfo("No Flashcards", "No flashcards found.")
            return

        # Select a random question
        self.current_question = random.choice(questions)[0]
        messagebox.showinfo("Random Question", self.current_question)
        self.answer_button.config(state=tk.NORMAL)  # Enable answer button

    def show_answer(self):
        try:
            # Fetch answer corresponding to the current question
            self.cursor_flashcards.execute("SELECT answer FROM flashcards WHERE question=?", (self.current_question,))
            answer = self.cursor_flashcards.fetchone()[0]
            messagebox.showinfo("Answer", answer)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def set_random_background(self):
        # Generate random RGB values
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        # Convert RGB values to hexadecimal format
        bg_color = "#{:02x}{:02x}{:02x}".format(r, g, b)

        # Set background color for the root window
        self.root.config(bg=bg_color)

    def voice_to_text_answer(self):
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.root.title("Listening...")
                audio = recognizer.listen(source)
                self.root.title("Flashcard App")

            text = recognizer.recognize_google(audio)
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.insert(0, text)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio.")
        except sr.RequestError:
            messagebox.showerror("Error", "Could not request results; check your internet connection.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def voice_to_text_question(self):
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.root.title("Listening...")
                audio = recognizer.listen(source)
                self.root.title("Flashcard App")

            text = recognizer.recognize_google(audio)
            self.question_entry.delete(0, tk.END)
            self.question_entry.insert(0, text)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio.")
        except sr.RequestError:
            messagebox.showerror("Error", "Could not request results; check your internet connection.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def start_test(self):
        try:
            # Prompt for student information
            name = simpledialog.askstring("Student Information", "Enter Your Name:")
            if not name:
                return

            roll_no = simpledialog.askstring("Student Information", "Enter Your Roll Number:")
            if not roll_no:
                return

            class_ = simpledialog.askstring("Student Information", "Enter Your Class:")
            if not class_:
                return

            # Insert student information into students database
            self.cursor_students.execute("INSERT INTO students (name, roll_no, class) VALUES (?, ?, ?)", (name, roll_no, class_))
            self.conn_students.commit()

            # Fetch all flashcards from flashcards database
            self.cursor_flashcards.execute("SELECT question, answer FROM flashcards")
            flashcards = self.cursor_flashcards.fetchall()

            # Create a new window for the test
            test_window = tk.Toplevel(self.root)
            test_window.title("Test")

            # Initialize variables to store the student's answers
            student_answers = {}
            for question, _ in flashcards:
                student_answers[question] = tk.StringVar()

            # Create GUI components for the test
            row = 0
            for question, _ in flashcards:
                tk.Label(test_window, text=question).grid(row=row, column=0, padx=10, pady=5)
                tk.Entry(test_window, textvariable=student_answers[question], width=50).grid(row=row, column=1, padx=10, pady=5)
                row += 1

            # Submit button to calculate and display report card
            submit_button = tk.Button(test_window, text="Submit", command=lambda: self.generate_report_card(test_window, flashcards, student_answers, name, roll_no, class_))
            submit_button.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="WE")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def generate_report_card(self, test_window, flashcards, student_answers, name, roll_no, class_):
        try:
            # Calculate right and wrong answers
            correct_answers = 0
            wrong_answers = 0
            report = ""

            for question, answer in flashcards:
                student_answer = student_answers[question].get().strip()
                if student_answer.lower() == answer.lower():
                    correct_answers += 1
                else:
                    wrong_answers += 1
                    report += f"\nQuestion: {question}\nYour Answer: {student_answer}\nCorrect Answer: {answer}\n"

            # Display report card
            report_card = f"Name: {name}\nRoll Number: {roll_no}\nClass: {class_}\n\nTotal Questions: {len(flashcards)}\nCorrect Answers: {correct_answers}\nWrong Answers: {wrong_answers}\n\n{report}"
            messagebox.showinfo("Report Card", report_card)
            test_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_all_reports(self):
        # Fetch all student information and report cards from students database
        self.cursor_students.execute("SELECT name, roll_no, class FROM students")
        students = self.cursor_students.fetchall()

        if not students:
            messagebox.showinfo("No Reports", "No reports found.")
            return

        # Initialize variable to store all report cards
        all_reports = ""

        # Loop through each student to fetch and append their report card
        for student in students:
            name, roll_no, class_ = student
            report = self.fetch_student_report(name, roll_no, class_)
            all_reports += report + "\n" + "-"*50 + "\n"

        # Display all report cards in a message box
        messagebox.showinfo("All Reports", all_reports)

    def fetch_student_report(self, name, roll_no, class_):
        # Fetch all flashcards from flashcards database
        self.cursor_flashcards.execute("SELECT question, answer FROM flashcards")
        flashcards = self.cursor_flashcards.fetchall()

        # Fetch student's answers from the student's table
        self.cursor_students.execute("SELECT * FROM students WHERE name=? AND roll_no=? AND class=?", (name, roll_no, class_))
        student_info = self.cursor_students.fetchone()

        # If student not found, return error message
        if not student_info:
            return f"No report found for {name} (Roll No: {roll_no}, Class: {class_})"

        # Extract student's answers from the student's record
        student_answers = student_info[3:]  # Assuming answers start from the 4th column
        total_questions = len(flashcards)
        correct_answers = 0
        wrong_answers = 0
        report = ""

        # Compare student's answers with correct answers
        for i, (question, answer) in enumerate(flashcards):
            if i < len(student_answers):
                student_answer = student_answers[i]
                if student_answer.lower() == answer.lower():
                    correct_answers += 1
                else:
                    wrong_answers += 1
                    report += f"\nQuestion: {question}\nYour Answer: {student_answer}\nCorrect Answer: {answer}\n"
            else:
                wrong_answers += 1
                report += f"\nQuestion: {question}\nYour Answer: Not answered\nCorrect Answer: {answer}\n"

        # Calculate score
        score = (correct_answers / total_questions) * 100

        # Construct report string with scores
        report_card = f"Name: {name}\nRoll Number: {roll_no}\nClass: {class_}\n\nTotal Questions: {total_questions}\nCorrect Answers: {correct_answers}\nWrong Answers: {wrong_answers}\nScore: {score:.2f}%\n\n{report}"
        return report_card


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()


# In[ ]:




