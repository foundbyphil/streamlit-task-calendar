import streamlit as st
import pandas as pd
import json
import datetime

# Load tasks from JSON file
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {day: {"tasks": [], "notes": ""} for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

# Save tasks to JSON file
def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

# Initialize session state for first-time run
if "tasks" not in st.session_state:
    st.session_state["tasks"] = load_tasks()

tasks = st.session_state["tasks"]

# Layout setup
st.title("🗓 Weekly Task Calendar")
st.write("Manage your weekly tasks and move them between days.")

# Grid layout for the weekly planner
cols = st.columns(7)
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
current_date = datetime.date.today()
week_dates = [(current_date + datetime.timedelta(days=i - current_date.weekday())).strftime("%b %d") for i in range(7)]

for i, col in enumerate(cols):
    with col:
        st.subheader(f"{days_of_week[i]}  [{week_dates[i]}]")
        new_task = st.text_input(f"Add task for {days_of_week[i]}", key=f"input_{i}")
        if st.button(f"➕ Add", key=f"add_{i}") and new_task:
            tasks[days_of_week[i]]["tasks"].append(new_task)
            save_tasks(tasks)
            st.rerun()
        
        # Display existing tasks with checkboxes
        updated_tasks = []
        for task in tasks[days_of_week[i]]["tasks"]:
            if not st.checkbox(task, key=f"{task}_{i}"):
                updated_tasks.append(task)
        tasks[days_of_week[i]]["tasks"] = updated_tasks
        save_tasks(tasks)

# Sidebar for moving tasks
st.sidebar.header("Move Tasks")
for day in days_of_week:
    st.sidebar.subheader(day)
    if tasks[day]["tasks"]:
        move_task = st.selectbox(f"Select a task from {day}", ["None"] + tasks[day]["tasks"], key=f"move_{day}")
        target_day = st.selectbox(f"Move to", days_of_week, key=f"target_{day}")
        if st.button(f"Move {day}", key=f"btn_{day}") and move_task != "None":
            tasks[day]["tasks"].remove(move_task)
            tasks[target_day]["tasks"].append(move_task)
            save_tasks(tasks)
            st.rerun()

# Sidebar for recurring tasks
st.sidebar.header("Recurring Tasks")
recurring_task = st.text_input("Task Name", key="recurring_task")
recurring_days = st.multiselect("Repeat on Days", days_of_week, key="recurring_days")
if st.button("Add Recurring Task") and recurring_task:
    for day in recurring_days:
        if recurring_task not in tasks[day]["tasks"]:
            tasks[day]["tasks"].append(recurring_task)
    save_tasks(tasks)
    st.rerun()

st.success("✅ Tasks saved automatically. Refresh the page if changes don't appear.")