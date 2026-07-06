import pygame
import sys

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()

# Game Objects Layout
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15

player_paddle = pygame.Rect(50, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH//2 - BALL_SIZE//2, SCREEN_HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Speeds
paddle_speed = 6
ball_speed_x = 5
ball_speed_y = 5

# Scores
player_score = 0
opponent_score = 0
game_font = pygame.font.Font(None, 50)

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Input handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[pygame.K_s] and player_paddle.bottom < SCREEN_HEIGHT:
        player_paddle.y += paddle_speed
        
    if keys[pygame.K_UP] and opponent_paddle.top > 0:
        opponent_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and opponent_paddle.bottom < SCREEN_HEIGHT:
        opponent_paddle.y += paddle_speed

    # Ball Logic
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Wall Bounce
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Paddle Bounce
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1

    # Scoring
    if ball.left <= 0:
        opponent_score += 1
        ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        ball_speed_x *= -1
    if ball.right >= SCREEN_WIDTH:
        player_score += 1
        ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        ball_speed_x *= -1

# Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT))

# Score Board 
    player_text = game_font.render(f"{player_score}", True, WHITE)
    opponent_text = game_font.render(f"{opponent_score}", True, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH//4, 20))
    screen.blit(opponent_text, (3 * SCREEN_WIDTH//4, 20))

# Screen Update
    pygame.display.flip()
    clock.tick(FPS)