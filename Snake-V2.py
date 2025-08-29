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
MAX_APPLES = 5  # Maximum apples in Extra Apples mode

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("arial", 36)
title_font = pygame.font.SysFont("arial", 72)
score_font = pygame.font.SysFont("arial", 24)

class Snake:
    def __init__(self, color, start_pos, start_direction):
        self.color = color
        self.start_pos = start_pos
        self.start_direction = start_direction
        self.reset()

    def reset(self):
        self.positions = [self.start_pos]
        self.direction = self.start_direction
        self.length = 1
        self.score = 0

    def get_head(self):
        return self.positions[0]

    def update(self, other_snake_positions, infinite_mode=False):
        cur = self.get_head()
        x, y = self.direction
        new = (cur[0] + x, cur[1] + y)
        if infinite_mode:
            # Wrap around screen edges
            new = (new[0] % GRID_WIDTH, new[1] % GRID_HEIGHT)
        else:
            # Check wall collision
            if new[0] < 0 or new[0] >= GRID_WIDTH or new[1] < 0 or new[1] >= GRID_HEIGHT:
                return False
            # Check collision with self or other snake
            if new in self.positions[2:] or new in other_snake_positions:
                return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.positions = []
        self.randomize_position()

    def randomize_position(self):
        # Add a new apple at a random position not occupied by existing apples or snakes
        available_positions = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)
                              if (x, y) not in self.positions and (x, y) not in snake1.positions
                              and (x, y) not in snake2.positions]
        if available_positions:
            self.positions.append(random.choice(available_positions))

    def render(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, RED, (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

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
    global snake1, snake2, food, game_state, buttons, game_mode
    snake1 = Snake(GREEN, (GRID_WIDTH // 4, GRID_HEIGHT // 2), (1, 0))
    snake2 = Snake(BLUE, (3 * GRID_WIDTH // 4, GRID_HEIGHT // 2), (-1, 0))
    food = Food()
    game_state = "menu"
    game_mode = None  # None, "single", "two_player", "infinite", or "extra_apples"
    pygame.display.set_caption("Snake Game")
    buttons = {
        "menu": [
            Button("1 Player", WIDTH // 2 - 100, HEIGHT // 2 - 70, 200, 50, GRAY, WHITE),
            Button("2 Player", WIDTH // 2 - 100, HEIGHT // 2 - 10, 200, 50, GRAY, WHITE),
            Button("Game Modes", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, GRAY, WHITE),
            Button("Exit", WIDTH // 2 - 100, HEIGHT // 2 + 110, 200, 50, GRAY, WHITE)
        ],
        "game_modes": [
            Button("Infinite", WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, GRAY, WHITE),
            Button("Extra Apples", WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 50, GRAY, WHITE),
            Button("Back", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, GRAY, WHITE)
        ],
        "game_over": [
            Button("Retry", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, GRAY, WHITE)
        ]
    }

def handle_input():
    global game_state, game_mode
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if game_state == "menu":
            for button in buttons["menu"]:
                if button.is_clicked(event):
                    if button.text == "1 Player":
                        game_state = "playing"
                        game_mode = "single"
                        snake1.reset()
                        snake2.reset()
                        food.positions = []
                        food.randomize_position()
                        pygame.display.set_caption("Snake Game - 1 Player")
                    elif button.text == "2 Player":
                        game_state = "playing"
                        game_mode = "two_player"
                        snake1.reset()
                        snake2.reset()
                        food.positions = []
                        food.randomize_position()
                        pygame.display.set_caption("Snake Game - 2 Player")
                    elif button.text == "Game Modes":
                        game_state = "game_modes"
                        pygame.display.set_caption("Snake Game")
                    elif button.text == "Exit":
                        return False
        elif game_state == "game_modes":
            for button in buttons["game_modes"]:
                if button.is_clicked(event):
                    if button.text == "Infinite":
                        game_state = "playing"
                        game_mode = "infinite"
                        snake1.reset()
                        snake2.reset()
                        food.positions = []
                        food.randomize_position()
                        pygame.display.set_caption("Snake Game - Infinite")
                    elif button.text == "Extra Apples":
                        game_state = "playing"
                        game_mode = "extra_apples"
                        snake1.reset()
                        snake2.reset()
                        food.positions = []
                        for _ in range(MAX_APPLES):
                            food.randomize_position()
                        pygame.display.set_caption("Snake Game - Extra Apples")
                    elif button.text == "Back":
                        game_state = "menu"
                        pygame.display.set_caption("Snake Game")
        elif game_state == "game_over":
            for button in buttons["game_over"]:
                if button.is_clicked(event):
                    if button.text == "Retry":
                        game_state = "playing"
                        snake1.reset()
                        snake2.reset()
                        food.positions = []
                        if game_mode == "extra_apples":
                            for _ in range(MAX_APPLES):
                                food.randomize_position()
                        else:
                            food.randomize_position()
                        pygame.display.set_caption(f"Snake Game - {game_mode.replace('single', '1 Player').replace('two_player', '2 Player').replace('infinite', 'Infinite').replace('extra_apples', 'Extra Apples')}")
        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                # Snake 1 (WASD)
                if event.key == pygame.K_w and snake1.direction != (0, 1):
                    snake1.direction = (0, -1)
                elif event.key == pygame.K_s and snake1.direction != (0, -1):
                    snake1.direction = (0, 1)
                elif event.key == pygame.K_a and snake1.direction != (1, 0):
                    snake1.direction = (-1, 0)
                elif event.key == pygame.K_d and snake1.direction != (-1, 0):
                    snake1.direction = (1, 0)
                # Snake 2 (Arrow keys, only if 2-player mode)
                if game_mode == "two_player":
                    if event.key == pygame.K_UP and snake2.direction != (0, 1):
                        snake2.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and event.key == pygame.K_DOWN and snake2.direction != (0, -1):
                        snake2.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake2.direction != (1, 0):
                        snake2.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake2.direction != (-1, 0):
                        snake2.direction = (1, 0)
    return True

def update_loop():
    global game_state
    screen.fill(BLACK)
    if game_state == "menu":
        title = title_font.render("Snake", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        screen.blit(title, title_rect)
        for button in buttons["menu"]:
            button.draw(screen)
    elif game_state == "game_modes":
        title = title_font.render("Game Modes", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title, title_rect)
        for button in buttons["game_modes"]:
            button.draw(screen)
    elif game_state == "playing":
        # Update snakes
        snake2_positions = snake2.positions if game_mode == "two_player" else []
        if not snake1.update(snake2_positions, infinite_mode=game_mode == "infinite"):
            if game_mode != "infinite":
                game_state = "game_over"
        if game_mode == "two_player":
            snake1_positions = snake1.positions
            if not snake2.update(snake1_positions, infinite_mode=False):
                game_state = "game_over"
        # Check for food collision
        head = snake1.get_head()
        if head in food.positions:
            snake1.length += 1
            snake1.score += 1
            food.positions.remove(head)
            if game_mode == "extra_apples" and len(food.positions) < MAX_APPLES:
                food.randomize_position()
            elif game_mode != "extra_apples":
                food.randomize_position()
        if game_mode == "two_player" and snake2.get_head() in food.positions:
            snake2.length += 1
            snake2.score += 1
            food.positions.remove(snake2.get_head())
            food.randomize_position()
        # Render
        snake1.render(screen)
        if game_mode == "two_player":
            snake2.render(screen)
        food.render(screen)
        # Draw score
        if game_mode in ["single", "infinite", "extra_apples"]:
            score_text = score_font.render(f"Score: {snake1.score}", True, WHITE)
            screen.blit(score_text, (10, 10))
        else:
            score1_text = score_font.render(f"P1 Score: {snake1.score}", True, WHITE)
            score2_text = score_font.render(f"P2 Score: {snake2.score}", True, WHITE)
            screen.blit(score1_text, (10, 10))
            screen.blit(score2_text, (10, 40))
    elif game_state == "game_over":
        game_over_text = title_font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(game_over_text, game_over_rect)
        if game_mode in ["single", "extra_apples"]:
            score_text = score_font.render(f"Score: {snake1.score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - 50, HEIGHT // 2 - 40))
        else:
            score1_text = score_font.render(f"P1 Score: {snake1.score}", True, WHITE)
            score2_text = score_font.render(f"P2 Score: {snake2.score}", True, WHITE)
            screen.blit(score1_text, (WIDTH // 2 - 50, HEIGHT // 2 - 40))
            screen.blit(score2_text, (WIDTH // 2 - 50, HEIGHT // 2 - 10))
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
