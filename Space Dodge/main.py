#Needed modules for the project
import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1300, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodger")

BG = pygame.transform.scale(pygame.image.load("Stars.jpeg"), (WIDTH, HEIGHT))

PLAYER_wIDTH = 40
PLAYER_HEIGHT =60
STAR_WIDTH = 10
STAR_HEIGHT = 20

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time, )}s", 1, (255, 255, 255))
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, (0, 255, 0), player)

    for star in stars:
        pygame.draw.rect(WIN, (255, 255, 0), star)

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_wIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
#keeping track of time to make sure the game runs at a consistent speed
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:


        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count >= star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment += max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - 5 > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.x + 5 + player.width < WIDTH:
            player.x += 5

        for star in stars[:]:
            star.y += 5
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lose_text = FONT.render(f"You lost! Time survived: {round(elapsed_time, 2)}s", 1, (255, 0, 0))
            WIN.blit(lose_text, (WIDTH/2 - lose_text.get_width()/2, HEIGHT/2 - lose_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break



        draw(player, elapsed_time, stars)

    pygame.quit()        

if __name__ == "__main__":
    main()