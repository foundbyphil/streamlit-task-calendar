import streamlit as st
import pandas as pd
import json
import datetime

# Define the tasks.json file
TASKS_FILE = "tasks.json"

# Load tasks from JSON file
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {day: {"tasks": [], "notes": ""} for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

# Save tasks back to JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Load tasks
tasks = load_tasks()

# Streamlit page config
st.set_page_config(page_title="Task Calendar", layout="wide")

# Create a grid layout that matches the reference image
st.title("📅 Weekly Task Planner")

# Get current date
current_date = datetime.date.today()
week_dates = {day: (current_date + datetime.timedelta(days=i - current_date.weekday())).strftime("%Y-%m-%d") for i, day in enumerate(tasks.keys())}

# Initialize column layout
cols = st.columns(7)  # 7 columns for each day of the week

# Map days of the week
days_of_week = list(tasks.keys())

# Drag-and-drop session state
if "dragging_task" not in st.session_state:
    st.session_state.dragging_task = None

# Display each day with its tasks
for i, day in enumerate(days_of_week):
    with cols[i]:
        st.subheader(f"{day} [{week_dates[day]}]")

        # Input box to add new tasks
        new_task = st.text_input(f"Add Task ({day})", key=f"input_{day}")
        if st.button(f"➕ Add to {day}", key=f"add_{day}"):
            if new_task:
                tasks[day]["tasks"].append({"text": new_task, "done": False})
                save_tasks(tasks)
                st.experimental_rerun()

        # Display existing tasks with checkboxes
        updated_tasks = []
        for task in tasks[day]["tasks"]:
            for idx, task in enumerate(tasks[day]["tasks"]):  # Add an index
    if not st.checkbox(task["text"], key=f"{day}_{idx}"):  # Use index for uniqueness
        updated_tasks.append(task)
                updated_tasks.append(task)

        # Update tasks
        tasks[day]["tasks"] = updated_tasks
        save_tasks(tasks)

        # Drag-and-drop functionality
        st.markdown("---")
        move_task = st.selectbox(f"Move task from {day}", [None] + [t["text"] for t in tasks[day]["tasks"]], key=f"move_{day}")
        move_to_day = st.selectbox(f"Move to", [None] + days_of_week, key=f"moveto_{day}")

        if st.button(f"Move Task ({day})", key=f"move_btn_{day}"):
            if move_task and move_to_day and move_to_day != day:
                task_obj = next((t for t in tasks[day]["tasks"] if t["text"] == move_task), None)
                if task_obj:
                    tasks[day]["tasks"].remove(task_obj)
                    tasks[move_to_day]["tasks"].append(task_obj)
                    save_tasks(tasks)
                    st.experimental_rerun()

        # Notes section
        st.text_area(f"Notes ({day})", value=tasks[day]["notes"], key=f"notes_{day}", height=100)

# Recurring tasks feature
st.sidebar.header("🔁 Recurring Tasks")
recurring_task = st.sidebar.text_input("Recurring Task Name")
recurring_days = st.sidebar.multiselect("Repeat on:", days_of_week)
if st.sidebar.button("➕ Add Recurring Task"):
    if recurring_task and recurring_days:
        for day in recurring_days:
            tasks[day]["tasks"].append({"text": recurring_task, "done": False})
        save_tasks(tasks)
        st.experimental_rerun()

# Save updated tasks
save_tasks(tasks)

