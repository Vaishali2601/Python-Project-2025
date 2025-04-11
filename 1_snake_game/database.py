import mysql.connector
import bcrypt

# MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="mca2025",  # Replace with your MySQL password
        database="snake_game"
    )

# Function to register a new user
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # Hash password
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password.decode()))
        conn.commit()
        print("User registered successfully!")
    except mysql.connector.IntegrityError:
        print("Error: Username already exists.")

    cursor.close()
    conn.close()

# Function to verify login
def verify_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result and bcrypt.checkpw(password.encode(), result[0].encode()):
        return True
    return False
