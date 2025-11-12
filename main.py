"""
Main entry point for the platform game
"""
import pygame
import sys
from config import *
from login import LoginScreen
from game import Game
from assets import init_assets


def main():
    """Main function to run the game"""
    # Initialize pygame
    pygame.init()

    # Create the screen FIRST (required before loading images)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platform Adventure")

    # Initialize assets AFTER creating the screen
    init_assets()
    
    # Main loop
    running = True
    
    while running:
        # Show login screen
        login_screen = LoginScreen(screen)
        user_id, username = login_screen.run()
        
        if user_id is None:
            # User quit from login screen
            running = False
            break
        
        # Start the game
        game = Game(screen, user_id, username)
        game.run()
        
        # After game ends, return to login screen
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()