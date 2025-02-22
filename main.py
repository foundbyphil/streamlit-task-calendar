import streamlit as st
import json
import os
import datetime
from streamlit_sortables import sort_items  # ✅ Corrected import for drag-and-drop

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
st.title("📅 Weekly Task Planner with Drag & Drop & Recurring Tasks")

# Sidebar for recurring tasks
with st.sidebar:
    st.header("🔁 Recurring Task")
    recurring_task = st.text_input("Task Name")
    recurring_days = st.multiselect("Repeat on:", DAYS_OF_WEEK)

    if st.button("➕ Add Recurring Task"):
        if recurring_task and recurring_days:
            for day in recurring_days:
                tasks[day]["tasks"].append({"text": recurring_task, "done": False})
            save_tasks(tasks)
            st.rerun()  # Refresh the page

# Displaying tasks for each day
cols = st.columns(7)

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
                st.rerun()  # Refresh the page

        # Drag-and-Drop Task List
        if day in tasks:
            task_list = [{"text": task["text"], "done": task["done"]} for task in tasks[day]["tasks"]]
            reordered_tasks = sort_items(task_list, direction="vertical", key=f"sortable_{day}")

            # Save reordered tasks
            tasks[day]["tasks"] = reordered_tasks
            save_tasks(tasks)

# Button to reset all tasks
if st.button("🔄 Reset Weekly Tasks"):
    tasks = DEFAULT_TASKS
    save_tasks(tasks)
    st.rerun()

