import streamlit as st
import json
import os
import pandas as pd

# File to store tasks locally
TASKS_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return {day: {"tasks": [], "notes": ""} for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

# Save tasks to file
def save_tasks(data):
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load existing tasks
tasks = load_tasks()

# Sidebar menu
st.sidebar.title("Task Calendar")
st.sidebar.write("Manage tasks with drag-and-drop and recurring options.")

st.title("📅 Weekly Task Calendar")

# Days of the week
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Display tasks in a table format with drag-and-drop
task_data = []
for day in days:
    for task in tasks[day]["tasks"]:
        task_data.append({"Day": day, "Task": task["text"], "Done": task["done"]})

# Convert tasks to DataFrame
df = pd.DataFrame(task_data)

# Allow user to edit, reorder, and move tasks
df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# Save updated task list back to tasks.json
new_tasks = {day: {"tasks": [], "notes": tasks[day]["notes"]} for day in days}
for _, row in df.iterrows():
    new_tasks[row["Day"]]["tasks"].append({"text": row["Task"], "done": row["Done"]})

tasks.update(new_tasks)

# Add new task input fields
for day in days:
    new_task = st.text_input(f"Add task for {day}", key=f"new-task-{day}")
    if new_task:
        tasks[day]["tasks"].append({"text": new_task, "done": False})

    # Recurring tasks
    if st.checkbox(f"Repeat task for {day}", key=f"repeat-{day}"):
        if new_task:
            tasks["Recurring"] = tasks.get("Recurring", []) + [{"text": new_task, "day": day}]

    # Notes section
    note = st.text_area(f"Notes for {day}", value=tasks[day]["notes"], key=f"notes-{day}")
    tasks[day]["notes"] = note

# Save changes
save_tasks(tasks)

st.success("Tasks and notes have been saved!")
