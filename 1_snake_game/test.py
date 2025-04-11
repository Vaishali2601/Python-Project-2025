import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'
        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self): self.direction = 'left'
    def move_right(self): self.direction = 'right'
    def move_up(self): self.direction = 'up'
    def move_down(self): self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left': self.x[0] -= SIZE
        if self.direction == 'right': self.x[0] += SIZE
        if self.direction == 'up': self.y[0] -= SIZE
        if self.direction == 'down': self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self, speed, apples_per_level):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.level = 1
        self.speed = speed
        self.apples_per_level = apples_per_level

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        sound = pygame.mixer.Sound(f"resources/{sound_name}.mp3")
        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.level = 1

    def is_collision(self, x1, y1, x2, y2):
        return x1 >= x2 and x1 < x2 + SIZE and y1 >= y2 and y1 < y2 + SIZE

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        bg = pygame.transform.scale(bg, (1000, 800))
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()

                # Updated: level-up logic based on difficulty
                if (self.snake.length - 1) % self.apples_per_level == 0:
                    self.level += 1
                    self.speed = max(0.1, self.speed - 0.02)

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"

        if not (0 <= self.snake.x[0] < 1000 and 0 <= self.snake.y[0] < 800):
            self.play_sound('crash')
            raise "Hit the boundary error"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}  Level: {self.level}", True, (200, 200, 200))
        self.surface.blit(score, (700, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game over! Your score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Press Enter to play again or Escape to exit", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_LEFT: self.snake.move_left()
                        if event.key == K_RIGHT: self.snake.move_right()
                        if event.key == K_UP: self.snake.move_up()
                        if event.key == K_DOWN: self.snake.move_down()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(self.speed)

def show_difficulty_menu():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Choose Difficulty")
    clock = pygame.time.Clock()

    try:
        bg_image = pygame.image.load("resources/background.jpg")
        bg_image = pygame.transform.scale(bg_image, (1000, 800))
    except pygame.error:
        bg_image = None

    low_btn = pygame.Rect(350, 300, 300, 60)
    med_btn = pygame.Rect(350, 400, 300, 60)
    high_btn = pygame.Rect(350, 500, 300, 60)

    def draw_button(rect, text, color):
        pygame.draw.rect(screen, color, rect)
        font = pygame.font.SysFont('arial', 35)
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    while True:
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((30, 30, 30))

        font = pygame.font.SysFont('arial', 50)
        title = font.render("    Select Difficulty", True, (255, 255, 255))
        screen.blit(title, (320, 180))

        draw_button(low_btn, "Low (Easy)", (0, 200, 0))
        draw_button(med_btn, "Medium", (200, 200, 0))
        draw_button(high_btn, "High (Hard)", (200, 0, 0))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if low_btn.collidepoint(event.pos):
                    return 0.4, 3
                if med_btn.collidepoint(event.pos):
                    return 0.3, 5
                if high_btn.collidepoint(event.pos):
                    return 0.15, 7

        clock.tick(60)

if __name__ == '__main__':
    speed, apples_per_level = show_difficulty_menu()
    game = Game(speed, apples_per_level)
    game.run()
