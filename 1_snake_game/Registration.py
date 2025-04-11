import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import bcrypt
import datetime
from tkcalendar import DateEntry
import re
import json

# Load state and district data from JSON
with open("india_states_districts_full.json", "r", encoding="utf-8") as f:
    states_cities = json.load(f)

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mca2025",
        database="snake_game"
    )

# Function to register user
def register():
    data = {
        "name": entry_name.get(),
        "surname": entry_surname.get(),
        "dob": entry_dob.get(),
        "username": entry_username.get(),
        "password": entry_password.get(),
        "email": entry_email.get(),
        "city": entry_city.get(),
        "state": entry_state.get(),
        "mobile": entry_mobile.get()
    }

    if any(not value for value in data.values()):
        messagebox.showerror("Error", "All fields are required!")
        return

    # Username validation: 5 to 10 characters
    if len(data["username"]) < 5 or len(data["username"]) > 10:
        messagebox.showerror("Invalid Username", "Username must be between 5 and 10 characters.")
        return

    # Password validation: 4 to 8 characters
    if len(data["password"]) < 4 or len(data["password"]) > 8:
        messagebox.showerror("Invalid Password", "Password must be between 4 and 8 characters.")
        return

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
    if not re.match(email_pattern, data["email"]):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    if not data["mobile"].isdigit() or len(data["mobile"]) != 10:
        messagebox.showerror("Invalid Mobile Number", "Mobile number must be exactly 10 digits.")
        return

    hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO registration (name, surname, dob, username, password, email, city, state, mobile)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["name"], data["surname"], data["dob"], data["username"],
            hashed_password.decode("utf-8"), data["email"], data["city"],
            data["state"], data["mobile"]
        ))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")

        # Auto-clear
        entry_name.delete(0, tk.END)
        entry_surname.delete(0, tk.END)
        entry_dob.set_date(datetime.date.today())
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_city.set('')
        entry_city.config(state="disabled")
        entry_state.set('')
        entry_mobile.delete(0, tk.END)

    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    finally:
        cursor.close()
        conn.close()

# GUI
register_window = tk.Tk()
register_window.title("Register - Snake Game")
register_window.geometry("500x720")
register_window.resizable(False, False)

# Background
try:
    bg_image = Image.open("background.jpg")
    bg_image = bg_image.resize((500, 720), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(register_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except Exception:
    register_window.configure(bg="lightgray")

form_frame = tk.Frame(register_window, bg="white", padx=20, pady=20, bd=5, relief="ridge")
form_frame.place(relx=0.5, rely=0.5, anchor="center")

def create_labeled_entry(parent, label):
    tk.Label(parent, text=label, font=("Arial", 12), bg="white").pack(anchor="w")
    entry = ttk.Entry(parent, font=("Arial", 12), width=30)
    entry.pack(pady=5)
    return entry

tk.Label(form_frame, text="Register", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

entry_name = create_labeled_entry(form_frame, "First Name:")
entry_surname = create_labeled_entry(form_frame, "Surname:")

tk.Label(form_frame, text="Date of Birth:", font=("Arial", 12), bg="white").pack(anchor="w")
entry_dob = DateEntry(
    form_frame,
    font=("Arial", 12),
    width=28,
    background='darkblue',
    foreground='white',
    date_pattern='yyyy-mm-dd',
    maxdate=datetime.date.today()
)
entry_dob.pack(pady=5)

entry_username = create_labeled_entry(form_frame, "Username:")

tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="white").pack(anchor="w")
entry_password = ttk.Entry(form_frame, show="*", font=("Arial", 12), width=30)
entry_password.pack(pady=5)

entry_email = create_labeled_entry(form_frame, "Email ID:")

# --- State and City dropdowns ---
tk.Label(form_frame, text="State:", font=("Arial", 12), bg="white").pack(anchor="w")
state_var = tk.StringVar()
entry_state = ttk.Combobox(form_frame, textvariable=state_var, font=("Arial", 12), width=28, state="readonly")
entry_state["values"] = list(states_cities.keys())
entry_state.pack(pady=5)

tk.Label(form_frame, text="City:", font=("Arial", 12), bg="white").pack(anchor="w")
city_var = tk.StringVar()
entry_city = ttk.Combobox(form_frame, textvariable=city_var, font=("Arial", 12), width=28, state="disabled")
entry_city.pack(pady=5)

def update_cities(event):
    selected_state = state_var.get()
    if selected_state in states_cities:
        entry_city["values"] = states_cities[selected_state]
        entry_city.config(state="readonly")
        city_var.set("")

entry_state.bind("<<ComboboxSelected>>", update_cities)

# Mobile field
entry_mobile = create_labeled_entry(form_frame, "Mobile No:")

# Register button
tk.Button(
    form_frame, text="Register", command=register,
    font=("Arial", 12, "bold"), bg="#008CBA", fg="white",
    padx=20, pady=5, bd=3, relief="raised"
).pack(pady=15)

register_window.mainloop()
