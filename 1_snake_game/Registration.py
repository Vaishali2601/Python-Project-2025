import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  # For background images
import bcrypt  # For password hashing

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Change this to your MySQL username
        password="mca2025",  # Change this to your MySQL password
        database="snake_game"
    )

# Function to register user
def register():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Hash the password before storing
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                       (username, hashed_password.decode("utf-8")))  # Decode bytes before storing
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        register_window.destroy()  # Close the registration window after success
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    finally:
        cursor.close()
        conn.close()

# Create Registration Window
register_window = tk.Tk()
register_window.title("Register - Snake Game")
register_window.geometry("400x500")
register_window.resizable(False, False)

# Load and Set Background Image
try:
    bg_image = Image.open("background.jpg")  # Replace with your image file
    bg_image = bg_image.resize((400, 500), Image.LANCZOS)  # Resize to fit window
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(register_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Cover entire window
except Exception:
    register_window.configure(bg="lightgray")  # Use a solid color if image fails

# Create a Frame for the Form
form_frame = tk.Frame(register_window, bg="white", padx=20, pady=20, bd=5, relief="ridge")
form_frame.place(relx=0.5, rely=0.5, anchor="center")

# Title Label
title_label = tk.Label(form_frame, text="Register", font=("Arial", 18, "bold"), fg="#333", bg="white")
title_label.pack(pady=10)

# Username Entry
tk.Label(form_frame, text="Username:", font=("Arial", 12), bg="white").pack(anchor="w")
entry_username = ttk.Entry(form_frame, font=("Arial", 12), width=25)
entry_username.pack(pady=5)

# Password Entry
tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="white").pack(anchor="w")
entry_password = ttk.Entry(form_frame, show="*", font=("Arial", 12), width=25)
entry_password.pack(pady=5)

# Register Button
register_button = tk.Button(
    form_frame, text="Register", command=register, 
    font=("Arial", 12, "bold"), bg="#008CBA", fg="white", 
    padx=20, pady=5, bd=3, relief="raised"
)
register_button.pack(pady=15)

register_window.mainloop()
