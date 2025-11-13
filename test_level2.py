"""Test script to directly load and display level 2"""
import pygame
import sys
from config import *
from level import Level
from assets import init_assets, get_assets
from player import Player

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Level 2 Test")
clock = pygame.time.Clock()

# Initialize assets
init_assets()
assets = get_assets()

# Load level 2
print("Loading level 2...")
level = Level(2)
print(f"Level 2 loaded! Platforms: {len(level.platforms)}")

# Create player
player = Player(100, 300)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Update
    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    player.update(level.platforms)

    # Draw
    screen.fill((135, 206, 235))  # Sky blue background

    # Draw background if available
    bg = assets.get_background('level2')
    if bg:
        screen.blit(bg, (0, 0))

    # Draw platforms (debug - red boxes)
    for platform in level.platforms:
        pygame.draw.rect(screen, (255, 0, 0), platform.rect, 2)

    # Draw player
    all_sprites.draw(screen)

    # Draw info
    font = pygame.font.Font(None, 36)
    info = font.render(f"Platforms: {len(level.platforms)} | Player: ({int(player.rect.x)}, {int(player.rect.y)})", True, (0, 0, 0))
    screen.blit(info, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
