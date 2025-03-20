import pygame
import sys
import subprocess
import psutil
import tkinter as tk  # Import tkinter

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 150, 250)
BUTTON_HOVER = (30, 100, 200)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Load background image
try:
    background = pygame.image.load("fancy_background.jpg")
except pygame.error:
    print("Error: Could not load background image. Make sure 'fancy_background.jpg' exists.")
    background = None

# Font
font = pygame.font.Font(None, 40)

# Button function
def draw_button(text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = BUTTON_HOVER if x < mouse[0] < x + w and y < mouse[1] < y + h else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h))

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surface, text_rect)

    if click[0] == 1 and action:
        pygame.time.delay(1)  # Prevent multiple fast clicks
        action()

# Check if a process is running
def is_process_running(script_name):
    for process in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        cmdline = process.info.get("cmdline", [])
        if cmdline and script_name in cmdline:
            return True  # Process is already running
    return False

# Function to start the game
def start_game():
    if not is_process_running("test.py"):
        subprocess.Popen(["python", "test.py"])

# Function to open registration window
def register():
    if not is_process_running("Registration.py"):
        subprocess.Popen(["python", "Registration.py"])

# Quit Game Function
def quit_game():
    pygame.quit()
    sys.exit()

# Main Menu
def main_menu():
    running = True
    while running:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)  # Use black background if image fails to load

        draw_button("Start Game", WIDTH // 3, HEIGHT // 3, 200, 50, start_game)
        draw_button("Quit", WIDTH // 3, HEIGHT // 3 + 140, 200, 50, quit_game)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

# Function to open Login window
def open_login():
    subprocess.Popen(["python", "Login.py"])

# Create Main Window
main_window = tk.Tk()
main_window.title("Snake Game - Authentication")
main_window.geometry("300x200")

tk.Label(main_window, text="Welcome to Snake Game!", font=("Arial", 14)).pack(pady=20)
tk.Button(main_window, text="Register", command=register, bg="blue", fg="white").pack(pady=5)
tk.Button(main_window, text="Login", command=open_login, bg="green", fg="white").pack(pady=5)
tk.Button(main_window, text="Quit", command=main_window.quit, bg="red", fg="white").pack(pady=5)

main_window.mainloop()

# Run the main menu
main_menu()
