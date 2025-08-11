import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle properties
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 7

# Ball properties
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Fonts
FONT = pygame.font.Font(None, 74)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, up=True):
        if up:
            self.rect.y -= PADDLE_SPEED
        else:
            self.rect.y += PADDLE_SPEED
        self.rect.y = max(self.rect.y, 0)
        self.rect.y = min(self.rect.y, HEIGHT - PADDLE_HEIGHT)

    def draw(self):
        pygame.draw.rect(SCREEN, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X * (-1 if pygame.time.get_ticks() % 2 == 0 else 1)
        self.speed_y = BALL_SPEED_Y * (-1 if pygame.time.get_ticks() % 2 == 0 else 1)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.ellipse(SCREEN, WHITE, self.rect)

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x *= -1
        self.speed_y *= -1

ball = Ball()
left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
right_paddle = Paddle(WIDTH - PADDLE_WIDTH - 10, HEIGHT // 2 - PADDLE_HEIGHT // 2)

left_score = 0
right_score = 0

clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_paddle.move(up=True)
    if keys[pygame.K_s]:
        left_paddle.move(up=False)
    if keys[pygame.K_UP]:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN]:
        right_paddle.move(up=False)

    ball.move()

    if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
        ball.speed_x *= -1

    if ball.rect.left <= 0:
        right_score += 1
        ball.reset()

    if ball.rect.right >= WIDTH:
        left_score += 1
        ball.reset()

    SCREEN.fill(BLACK)
    left_paddle.draw()
    right_paddle.draw()
    ball.draw()

    left_text = FONT.render(str(left_score), True, WHITE)
    right_text = FONT.render(str(right_score), True, WHITE)
    SCREEN.blit(left_text, (WIDTH // 4 - left_text.get_width() // 2, 20))
    SCREEN.blit(right_text, (WIDTH * 3 // 4 - right_text.get_width() // 2, 20))

    pygame.display.flip()
    clock.tick(60)
