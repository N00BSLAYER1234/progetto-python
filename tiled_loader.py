"""
Tiled map loader for loading TMX files
"""
import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from entities import Platform, Enemy, Coin, Boss
from config import *


class TiledMapLoader:
    def __init__(self, tmx_file):
        """Load a TMX file from Tiled"""
        self.tmx_data = load_pygame(tmx_file)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

    def load_level_data(self):
        """Extract level data from the TMX file"""
        platforms = []
        enemies = pygame.sprite.Group()
        coins = pygame.sprite.Group()
        boss = None
        player_spawn = None

        # Load tile layers (platforms, background, etc)
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                # Check if this is a platform layer
                if 'platform' in layer.name.lower() or 'collision' in layer.name.lower():
                    platforms.extend(self.load_platforms_from_layer(layer))

        # Load object layers (enemies, coins, player spawn, boss)
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    obj_type = obj.properties.get('type', '').lower()

                    if obj_type == 'player':
                        player_spawn = (obj.x, obj.y)

                    elif obj_type == 'enemy':
                        movement_range = obj.properties.get('movement_range', 100)
                        enemy = Enemy(obj.x, obj.y, movement_range)
                        enemies.add(enemy)

                    elif obj_type == 'coin':
                        coin = Coin(obj.x, obj.y)
                        coins.add(coin)

                    elif obj_type == 'boss':
                        boss = Boss(obj.x, obj.y)

        return {
            'platforms': platforms,
            'enemies': enemies,
            'coins': coins,
            'boss': boss,
            'player_spawn': player_spawn
        }

    def load_platforms_from_layer(self, layer):
        """Convert tile layer to platform objects"""
        platforms = []

        # Group consecutive tiles into platforms
        for y in range(self.tmx_data.height):
            platform_start = None
            platform_width = 0

            for x in range(self.tmx_data.width):
                tile = self.tmx_data.get_tile_image(x, y, layer)

                if tile:  # There's a tile here
                    if platform_start is None:
                        platform_start = x
                    platform_width += 1
                else:  # No tile, end of platform
                    if platform_start is not None:
                        # Create platform
                        px = platform_start * self.tmx_data.tilewidth
                        py = y * self.tmx_data.tileheight
                        width = platform_width * self.tmx_data.tilewidth
                        platform = Platform(px, py, width)
                        platforms.append(platform)
                        platform_start = None
                        platform_width = 0

            # Handle platform at end of row
            if platform_start is not None:
                px = platform_start * self.tmx_data.tilewidth
                py = y * self.tmx_data.tileheight
                width = platform_width * self.tmx_data.tilewidth
                platform = Platform(px, py, width)
                platforms.append(platform)

        return platforms

    def render_background_layers(self, surface):
        """Render non-collision tile layers as background"""
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                # Skip platform/collision layers
                if 'platform' in layer.name.lower() or 'collision' in layer.name.lower():
                    continue

                # Render background tiles
                for x, y, image in layer.tiles():
                    if image:
                        surface.blit(image, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))


def load_level_from_tiled(level_number):
    """Load a level from a Tiled TMX file"""
    import os

    tmx_file = os.path.join(os.path.dirname(__file__), 'assets', 'levels', f'level{level_number}.tmx')

    if not os.path.exists(tmx_file):
        return None

    try:
        loader = TiledMapLoader(tmx_file)
        level_data = loader.load_level_data()
        level_data['loader'] = loader  # Keep loader for background rendering
        return level_data
    except Exception as e:
        print(f"Error loading Tiled map: {e}")
        return None