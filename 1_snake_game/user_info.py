import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Connect to database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mca2025",
        database="snake_game"
    )

# Read username from session
def get_logged_in_username():
    try:
        with open("session.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

# Fetch user details
def fetch_user_info(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, surname, dob, username, email, city, state, mobile FROM registration WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# Display user info in table format
def display_user_info():
    username = get_logged_in_username()
    if not username:
        messagebox.showwarning("Not Logged In", "No user is currently logged in.")
        return

    user_info = fetch_user_info(username)
    if not user_info:
        messagebox.showerror("Error", "User not found in database.")
        return

    root = tk.Tk()
    root.title("Logged-in User Info")
    root.geometry("600x300")
    root.configure(bg="white")

    fields = ["First Name", "Surname", "Date of Birth", "Username", "Email", "City", "State", "Mobile"]
    
    tree = ttk.Treeview(root, columns=fields, show="headings", height=1)
    for field in fields:
        tree.heading(field, text=field)
        tree.column(field, width=120, anchor="center")
    
    tree.insert("", "end", values=user_info)
    tree.pack(pady=30)

    root.mainloop()

# Run the function
if __name__ == "__main__":
    display_user_info()
