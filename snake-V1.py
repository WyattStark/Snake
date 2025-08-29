import asyncio
import pygame
import random
import platform

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 600
HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("arial", 36)
title_font = pygame.font.SysFont("arial", 72)

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1

    def get_head(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head()
        x, y = self.direction
        new = (cur[0] + x, cur[1] + y)
        # Check wall collision
        if new[0] < 0 or new[0] >= GRID_WIDTH or new[1] < 0 or new[1] >= GRID_HEIGHT:
            return False
        # Check self collision
        if new in self.positions[2:]:
            return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, GREEN, (p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def render(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, text_color=WHITE):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def setup():
    global snake, food, game_state, buttons
    snake = Snake()
    food = Food()
    game_state = "menu"
    buttons = {
        "menu": [
            Button("Play", WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 50, GRAY, WHITE),
            Button("Exit", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, GRAY, WHITE)
        ],
        "game_over": [
            Button("Retry", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, GRAY, WHITE)
        ]
    }

def handle_input():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if game_state == "menu":
            for button in buttons["menu"]:
                if button.is_clicked(event):
                    if button.text == "Play":
                        game_state = "playing"
                        snake.reset()
                    elif button.text == "Exit":
                        return False
        elif game_state == "game_over":
            for button in buttons["game_over"]:
                if button.is_clicked(event):
                    if button.text == "Retry":
                        game_state = "playing"
                        snake.reset()
                        food.randomize_position()
        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
    return True

def update_loop():
    global game_state
    screen.fill(BLACK)
    if game_state == "menu":
        title = title_font.render("Snake", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title, title_rect)
        for button in buttons["menu"]:
            button.draw(screen)
    elif game_state == "playing":
        if not snake.update():
            game_state = "game_over"
        if snake.get_head() == food.position:
            snake.length += 1
            food.randomize_position()
        snake.render(screen)
        food.render(screen)
    elif game_state == "game_over":
        game_over_text = title_font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(game_over_text, game_over_rect)
        for button in buttons["game_over"]:
            button.draw(screen)
    pygame.display.flip()

async def main():
    setup()
    while True:
        if not handle_input():
            break
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
