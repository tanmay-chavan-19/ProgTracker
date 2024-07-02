import streamlit as st
import sqlite3
import base64

# Setup the SQLite database
def setup_database():
    conn = sqlite3.connect('progress_tracker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, description TEXT, deadline TEXT, status TEXT)''')
    conn.commit()
    conn.close()

# Add a new task
def add_task(description, deadline):
    conn = sqlite3.connect('progress_tracker.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (description, deadline, status) VALUES (?, ?, ?)", (description, deadline, 'Pending'))
    conn.commit()
    conn.close()

# List all tasks
def list_tasks():
    conn = sqlite3.connect('progress_tracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

# Update a task
def update_task(task_id, description=None, deadline=None, status=None):
    conn = sqlite3.connect('progress_tracker.db')
    c = conn.cursor()
    if description:
        c.execute("UPDATE tasks SET description = ? WHERE id = ?", (description, task_id))
    if deadline:
        c.execute("UPDATE tasks SET deadline = ? WHERE id = ?", (deadline, task_id))
    if status:
        c.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()

# Delete a task
def delete_task(task_id):
    conn = sqlite3.connect('progress_tracker.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Function to load the HTML file and return its content
def load_html(file_name):
    with open(file_name, 'r') as file:
        html_content = file.read()
    return html_content

# Function to render the HTML in Streamlit
def render_html(html_content):
    b64_html = base64.b64encode(html_content.encode()).decode()
    st.markdown(f'<iframe src="data:text/html;base64,{b64_html}" width="100%" height="500px"></iframe>', unsafe_allow_html=True)

def main():
    setup_database()

    st.title("Progress Tracker")
    st.write("Track your progress on a road with a car animation.")

    menu = ["Add Task", "View Tasks", "Update Task", "Delete Task", "View Progress"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Task":
        st.subheader("Add a new task")
        description = st.text_input("Task Description")
        deadline = st.date_input("Task Deadline")
        if st.button("Add Task"):
            add_task(description, str(deadline))
            st.success(f"Task '{description}' added successfully!")

    elif choice == "View Tasks":
        st.subheader("View all tasks")
        tasks = list_tasks()
        for task in tasks:
            st.write(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2]}, Status: {task[3]}")

    elif choice == "Update Task":
        st.subheader("Update an existing task")
        task_id = st.number_input("Task ID", min_value=1)
        description = st.text_input("New Description (leave blank to keep current)")
        deadline = st.date_input("New Deadline (leave blank to keep current)")
        status = st.selectbox("Status", ["Pending", "Completed"])
        if st.button("Update Task"):
            update_task(task_id, description or None, str(deadline) or None, status)
            st.success(f"Task ID {task_id} updated successfully!")

    elif choice == "Delete Task":
        st.subheader("Delete a task")
        task_id = st.number_input("Task ID to delete", min_value=1)
        if st.button("Delete Task"):
            delete_task(task_id)
            st.success(f"Task ID {task_id} deleted successfully!")

    elif choice == "View Progress":
        st.subheader("View your progress")
        html_content = load_html('road.html')
        render_html(html_content)

if __name__ == "__main__":
    main()
