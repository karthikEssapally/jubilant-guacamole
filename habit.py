import tkinter as tk
from tkinter import messagebox
import sqlite3

# Initialize Database
conn = sqlite3.connect('habit_tracker.db')
cursor = conn.cursor()

# Create Table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    days_completed INTEGER DEFAULT 0
)
''')
conn.commit()

# Function to Add a Habit
def add_habit():
    habit_name = habit_entry.get()
    if habit_name:
        cursor.execute("INSERT INTO habits (name, days_completed) VALUES (?, ?)", (habit_name, 0))
        conn.commit()
        habit_entry.delete(0, tk.END)
        load_habits()
        messagebox.showinfo("Success", "Habit added successfully!")
    else:
        messagebox.showwarning("Input Error", "Please enter a habit name.")

# Function to Mark Habit as Completed
def complete_habit(habit_id):
    cursor.execute("UPDATE habits SET days_completed = days_completed + 1 WHERE id = ?", (habit_id,))
    conn.commit()
    load_habits()

# Function to Load and Display Habits
def load_habits():
    # Clear the List
    for widget in habit_list_frame.winfo_children():
        widget.destroy()

    cursor.execute("SELECT * FROM habits")
    habits = cursor.fetchall()
    for habit in habits:
        habit_id, name, days_completed = habit

        # Display Habit
        habit_label = tk.Label(habit_list_frame, text=f"{name} - Days Completed: {days_completed}")
        habit_label.pack(anchor='w', pady=2)

        # Button to mark as completed
        complete_button = tk.Button(habit_list_frame, text="Complete", command=lambda habit_id=habit_id: complete_habit(habit_id))
        complete_button.pack(anchor='e')

# GUI Setup
root = tk.Tk()
root.title("Habit Tracker")

habit_entry = tk.Entry(root, width=30)
habit_entry.pack(pady=10)
add_button = tk.Button(root, text="Add Habit", command=add_habit)
add_button.pack(pady=5)

habit_list_frame = tk.Frame(root)
habit_list_frame.pack(pady=20)

load_habits()  # Load existing habits

root.mainloop()

# Close the Database Connection
conn.close()
