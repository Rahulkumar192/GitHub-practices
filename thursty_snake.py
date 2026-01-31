import pygame
import random
import sys

# ---------- CONFIG ----------
WIDTH, HEIGHT = 900, 600
FPS = 60
BG_COLOR = (18, 18, 18)
SNAKE_RADIUS = 10
INITIAL_LENGTH = 5

# Non-repeating color pool
COLOR_POOL = [
    (231, 76, 60), (46, 204, 113), (52, 152, 219),
    (241, 196, 15), (155, 89, 182), (26, 188, 156),
    (230, 126, 34), (149, 165, 166)
]

FOOD_TYPES = [
    {"color": (255, 0, 0), "score": 10},
    {"color": (0, 255, 0), "score": 20},
    {"color": (0, 200, 255), "score": 30}
]

# ---------- INIT ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Professional Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 22)

# ---------- CLASSES ----------
class Snake:
    def __init__(self):
        self.body = []
        self.colors = []
        self.direction = pygame.Vector2(1, 0)
        self.color_index = 0

        x, y = WIDTH // 2, HEIGHT // 2
        for i in range(INITIAL_LENGTH):
            self.add_segment((x - i * SNAKE_RADIUS * 2, y))

    def add_segment(self, position):
        self.body.append(pygame.Vector2(position))
        self.colors.append(COLOR_POOL[self.color_index])
        self.color_index = (self.color_index + 1) % len(COLOR_POOL)

    def move(self):
        new_head = self.body[0] + self.direction * SNAKE_RADIUS * 2
        self.body.insert(0, new_head)
        self.body.pop()
        self.colors.insert(0, self.colors[0])
        self.colors.pop()

    def grow(self):
        self.add_segment(self.body[-1])

    def draw(self):
        for pos, col in zip(self.body, self.colors):
            pygame.draw.circle(screen, col, pos, SNAKE_RADIUS)

    def collision_self(self):
        return self.body[0] in self.body[1:]

class Food:
    def __init__(self):
        self.type = random.choice(FOOD_TYPES)
        self.position = self.random_position()

    def random_position(self):
        return pygame.Vector2(
            random.randrange(40, WIDTH - 40, 20),
            random.randrange(40, HEIGHT - 40, 20)
        )

    def draw(self):
        pygame.draw.circle(screen, self.type["color"], self.position, 8)

class Stone:
    def __init__(self):
        self.radius = random.randint(15, 40)
        self.position = pygame.Vector2(
            random.randint(60, WIDTH - 60),
            random.randint(60, HEIGHT - 60)
        )

    def draw(self):
        pygame.draw.circle(screen, (120, 120, 120), self.position, self.radius)

# ---------- GAME SETUP ----------
snake = Snake()
food = Food()
stones = [Stone() for _ in range(6)]
score = 0

# ---------- MAIN LOOP ----------
while True:
    clock.tick(FPS)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction.y != 1:
                snake.direction = pygame.Vector2(0, -1)
            if event.key == pygame.K_DOWN and snake.direction.y != -1:
                snake.direction = pygame.Vector2(0, 1)
            if event.key == pygame.K_LEFT and snake.direction.x != 1:
                snake.direction = pygame.Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and snake.direction.x != -1:
                snake.direction = pygame.Vector2(1, 0)

    snake.move()

    # --- FOOD COLLISION ---
    if snake.body[0].distance_to(food.position) < SNAKE_RADIUS + 8:
        score += food.type["score"]
        snake.grow()
        food = Food()

    # --- STONE COLLISION ---
    for stone in stones:
        if snake.body[0].distance_to(stone.position) < SNAKE_RADIUS + stone.radius:
            pygame.quit()
            sys.exit()

    # --- WALL COLLISION ---
    head = snake.body[0]
    if head.x < 0 or head.x > WIDTH or head.y < 0 or head.y > HEIGHT:
        pygame.quit()
        sys.exit()

    # --- SELF COLLISION ---
    if snake.collision_self():
        pygame.quit()
        sys.exit()

    # --- DRAW ---
    food.draw()
    for stone in stones:
        stone.draw()
    snake.draw()

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (15, 15))

    pygame.display.flip()