"""Direct test for level 2 - starts at level 2 immediately"""
import pygame
import sys
from config import *
from game import Game

# Initialize pygame
pygame.init()

# Create game instance
game = Game()

# Override to start at level 2
game.current_level = 2
from level import Level
game.level = Level(2)
game.player.reset_position(100, 300)

print("🎮 Starting at Level 2!")
print(f"Diamonds to collect: {len(game.level.coins)}")
print(f"Enemies: {len(game.level.enemies)}")
print(f"Chest: {'Yes' if game.level.chest else 'No'}")

# Run game
game.run()

pygame.quit()
sys.exit()
