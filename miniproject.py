# this is my mini project . i am choosing the topic of task management system. here i am using two tabels ,
# one for user credential  table and one for storing datas of users task management.


import sqlite3

conn = sqlite3.connect('task_system.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks(
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER, 
    title TEXT,
    description TEXT,
    status TEXT DEFAULT 'Pending',
    due_date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
''')
conn.commit()


def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        cursor.execute("INSERT INTO users (username,password) VALUES (?,?)", (username, password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already taken.")


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    cursor.execute("SELECT user_id FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    if result:
        print("Login successful!")
        return result[0]
    else:
        print("Invalid credentials.")
        return None


def add_task(uid):
    title = input("Enter task title: ")
    desc = input("Enter task description: ")
    due = input("Enter due date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO tasks (user_id,title,description,due_date) VALUES (?,?,?,?)", (uid, title, desc, due))
    conn.commit()
    print("Task added successfully")


def view_tasks(uid):
    cursor.execute("SELECT * FROM tasks WHERE user_id=?", (uid,))
    data = cursor.fetchall()
    if data:
        for d in data:
            print(f"\nID: {d[0]}, Title: {d[2]}, Description: {d[3]}, Status: {d[4]}, Due: {d[5]}")
    else:
        print("No tasks found.")


def update_task(uid):
    tid = input("Enter task ID: ")
    new_status = input("Enter new status (Pending/In Progress/Completed): ")
    cursor.execute("UPDATE tasks SET status=? WHERE task_id=? AND user_id=?", (new_status, tid, uid))
    conn.commit()
    if cursor.rowcount > 0:
        print("Task updated.")
    else:
        print("Task not found.")


def delete_task(uid):

    cursor.execute("SELECT task_id, title FROM tasks WHERE user_id=?", (uid,))
    tasks = cursor.fetchall()
    if not tasks:
        print("No tasks to delete.")
        return

    print("\nYour Tasks:")
    for t in tasks:
        print(f"ID: {t[0]} | Title: {t[1]}")


    tid = input("Enter task ID to delete: ")
    cursor.execute("DELETE FROM tasks WHERE task_id=? AND user_id=?", (tid, uid))
    conn.commit()
    if cursor.rowcount > 0:
        print("Task deleted.")
    else:
        print("Task not found or unauthorized.")

# Main program here is the cli begins
print("Welcome to Task Management System")

while True:
    print("\n1. Register\n2. Login\n3. Exit")
    ch = input("Choose: ")

    if ch == '1':
        register_user()
    elif ch == '2':
        user_id = login()
        if user_id:
            while True:
                print("\n1. Add Task\n2. View Tasks\n3. Update Task\n4. Delete Task\n5. Logout")
                op = input("Choose option: ")
                if op == '1':
                    add_task(user_id)
                elif op == '2':
                    view_tasks(user_id)
                elif op == '3':
                    update_task(user_id)
                elif op == '4':
                    delete_task(user_id)
                elif op == '5':
                    break
                else:
                    print("Invalid choice.")
    elif ch == '3':
        print("see you later ")
        break
    else:
        print("Invalid choice.")

conn.close()





