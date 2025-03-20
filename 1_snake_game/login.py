import mysql.connector
import tkinter as tk
from tkinter import messagebox
import bcrypt  
import subprocess  # To open the main menu

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mca2025",
        database="snake_game"
    )

# Function to verify user login
def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        stored_hashed_password = result[0]  

        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):  
            messagebox.showinfo("Success", f"Welcome, {username}!")
            login_window.destroy()  # Close login window
            
            # 🔥 Open the Main Menu (`main.py`)
            subprocess.Popen(["python", "main.py"])  
        else:
            messagebox.showerror("Error", "Incorrect password!")
    else:
        messagebox.showerror("Error", "Username not found!")

    cursor.close()
    conn.close()

# Create Login Window
login_window = tk.Tk()
login_window.title("Login - Snake Game")
login_window.geometry("300x250")
login_window.resizable(False, False)

tk.Label(login_window, text="Username:", font=("Arial", 12)).pack(pady=5)
entry_username = tk.Entry(login_window, font=("Arial", 12))
entry_username.pack()

tk.Label(login_window, text="Password:", font=("Arial", 12)).pack(pady=5)
entry_password = tk.Entry(login_window, show="*", font=("Arial", 12))
entry_password.pack()

tk.Button(login_window, text="Login", command=login, bg="green", fg="white", font=("Arial", 12, "bold"), padx=20, pady=5).pack(pady=10)

login_window.mainloop()
def login_success(username):
    with open("session.txt", "w") as file:
        file.write(username)  # Save logged-in username
    print("Login successful. You can now start the game.")
