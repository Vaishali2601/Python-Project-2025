import mysql.connector
import bcrypt

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mca2025",  # Add your MySQL password
    database="snake_game"
)
cursor = conn.cursor()

# Function to check password
def verify_password(username, input_password):
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    
    if result:
        stored_hashed_password = result[0].encode('utf-8')
        if bcrypt.checkpw(input_password.encode('utf-8'), stored_hashed_password):
            print("✅ Password is correct!")
        else:
            print("❌ Incorrect password!")
    else:
        print("❌ Username not found!")

# Ask for username and password to verify
user = input("Enter username: ")
password = input("Enter password: ")

verify_password(user, password)

# Close connection
cursor.close()
conn.close()
