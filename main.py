import streamlit as st
import json
import os
import datetime

# File path for saving tasks
TASKS_FILE = "tasks.json"

# Default structure for tasks
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

DEFAULT_TASKS = {day: {"tasks": [], "notes": ""} for day in DAYS_OF_WEEK}

# Load tasks from JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return DEFAULT_TASKS

# Save tasks to JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Load tasks on startup
tasks = load_tasks()

# Get the current date and calculate the week's dates
today = datetime.date.today()
start_of_week = today - datetime.timedelta(days=today.weekday())
week_dates = {day: (start_of_week + datetime.timedelta(days=i)).strftime("%m/%d") for i, day in enumerate(DAYS_OF_WEEK)}

# Streamlit UI Layout
st.title("📅 Weekly Task Planner")

# Grid layout for days
cols = st.columns(7)

# Input boxes for adding tasks
for i, day in enumerate(DAYS_OF_WEEK):
    with cols[i]:
        st.subheader(f"{day} [{week_dates[day]}]")

        # Task input box
        new_task = st.text_input(f"Add Task for {day}", key=f"input_{day}")

        # Button to add new task
        if st.button(f"➕ Add to {day}", key=f"btn_{day}"):
            if new_task:
                tasks[day]["tasks"].append({"text": new_task, "done": False})
                save_tasks(tasks)
                st.rerun()  # ✅ FIX: Updated from experimental_rerun() to rerun()

        # Display existing tasks with checkboxes
        updated_tasks = []
        for idx, task in enumerate(tasks[day]["tasks"]):
            if not st.checkbox(task["text"], key=f"{day}_{idx}"):
                updated_tasks.append(task)

        # Update the task list for the day
        tasks[day]["tasks"] = updated_tasks
        save_tasks(tasks)

# Drag-and-drop functionality (Mock-up)
st.write("🖱 Drag-and-Drop Feature Coming Soon!")

# Button to reset all tasks
if st.button("🔄 Reset Weekly Tasks"):
    tasks = DEFAULT_TASKS
    save_tasks(tasks)
    st.rerun()  # ✅ FIX: Updated from experimental_rerun() to rerun()
