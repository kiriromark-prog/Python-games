import pygame
import random
import sys

pygame.init()
pygame.font.init()

CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = 30, 20
SCREEN_WIDTH, SCREEN_HEIGHT = CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Snake")
clock = pygame.time.Clock()

# Fonts
FONT_SCORE = pygame.font.SysFont("arial", 18, bold=True)
FONT_GAMEOVER = pygame.font.SysFont("arial", 36, bold=True)
FONT_SUB = pygame.font.SysFont("arial", 20)

# Global High Score
high_score = 0

def reset_game():
    """Resets all active game variables to starting state."""
    global min_x, max_x, min_y, max_y, snake, direction, next_direction
    global obstacles, food, powerup, score, base_speed, game_state

    min_x, max_x = 0, GRID_WIDTH
    min_y, max_y = 0, GRID_HEIGHT
    
    snake = [pygame.Vector2(15, 10), pygame.Vector2(14, 10), pygame.Vector2(13, 10)]
    direction = next_direction = pygame.Vector2(1, 0)
    
    obstacles = [pygame.Vector2(random.randint(5, 24), random.randint(5, 14)) for _ in range(6)]
    
    food = get_valid_pos()
    powerup = None
    score = 0
    base_speed = 120
    game_state = "PLAYING"
    
    pygame.time.set_timer(MOVE_EVENT, base_speed)
    pygame.time.set_timer(SHRINK_EVENT, 10000)

def get_valid_pos():
    while True:
        pos = pygame.Vector2(random.randint(min_x, max_x - 1), random.randint(min_y, max_y - 1))
        if pos not in snake and pos not in obstacles:
            return pos

# Custom Events
MOVE_EVENT = pygame.USEREVENT + 1
SHRINK_EVENT = pygame.USEREVENT + 2

# Start Initial Game
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == "PLAYING":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction.y == 0: next_direction = pygame.Vector2(0, -1)
                elif event.key == pygame.K_DOWN and direction.y == 0: next_direction = pygame.Vector2(0, 1)
                elif event.key == pygame.K_LEFT and direction.x == 0: next_direction = pygame.Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT and direction.x == 0: next_direction = pygame.Vector2(1, 0)

            elif event.type == SHRINK_EVENT:
                if (max_x - min_x) > 10 and (max_y - min_y) > 10:
                    min_x += 1; max_x -= 1
                    min_y += 1; max_y -= 1

            elif event.type == MOVE_EVENT:
                direction = next_direction
                new_head = snake[0] + direction

                out_of_bounds = not (min_x <= new_head.x < max_x and min_y <= new_head.y < max_y)
                if out_of_bounds or new_head in snake or new_head in obstacles:
                    game_state = "GAME_OVER"
                    if score > high_score:
                        high_score = score

                if game_state == "PLAYING":
                    snake.insert(0, new_head)

                    if new_head == food:
                        score += 10
                        food = get_valid_pos()
                        if not powerup and random.random() < 0.3:
                            powerup = get_valid_pos()
                    else:
                        snake.pop()

                    if powerup and new_head == powerup:
                        score += 25
                        powerup = None
                        pygame.time.set_timer(MOVE_EVENT, base_speed + 60)

        elif game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()

# --- RENDERING ---
    screen.fill((20, 20, 20))

# 1. Draw Out-of-Bounds Hazard Zone
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if not (min_x <= x < max_x and min_y <= y < max_y):
                pygame.draw.rect(screen, (80, 20, 20), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# 2. Draw Game Objects
    for obs in obstacles:
        pygame.draw.rect(screen, (100, 100, 100), (obs.x * CELL_SIZE, obs.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, (220, 50, 50), (food.x * CELL_SIZE, food.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if powerup:
        pygame.draw.rect(screen, (50, 150, 250), (powerup.x * CELL_SIZE, powerup.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for segment in snake:
        pygame.draw.rect(screen, (50, 220, 100), (segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# 3. Draw On-Screen HUD (Score Display)
    score_surface = FONT_SCORE.render(f"SCORE: {score}  |  HIGH SCORE: {high_score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 8))

# 4. Draw Game Over Overlay
    if game_state == "GAME_OVER":
        # Dark translucent overlay surface
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

# Game Over Text
        title_surf = FONT_GAMEOVER.render("GAME OVER", True, (230, 50, 50))
        score_surf = FONT_SUB.render(f"Final Score: {score}", True, (255, 255, 255))
        restart_surf = FONT_SUB.render("Press 'R' to Restart", True, (180, 180, 180))

        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
        screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)))
        screen.blit(restart_surf, restart_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 45)))

    pygame.display.flip()
    clock.tick(60)