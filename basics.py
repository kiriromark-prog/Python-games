#These are basics i used to learn Pygame.

# Dependencies
import pygame

# This initializes all the modules required for Pygame to work
pygame.init()

# Set up the game window    

# This is the width and height of the window
WIDTH, HEIGHT = 800, 600

# This creates the caption for the window
pygame.display.set_caption("Space Dodge")

#This is the main game loop that keeps the game running until the user quits
def main():

    # This creates the game window with the specified width and height
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    # This controls the main loop and keeps the game running until the user quits
    run = True

    while run:

        # This checks for events in the game window, such as quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

# This ensures the program is executed only when the script is run directly. 
if __name__=="__main__":
    main()



