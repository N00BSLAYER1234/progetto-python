# Tiled Map Editor Setup Guide

## What is Tiled?
Tiled is a free, visual level editor that lets you design game levels by clicking and placing tiles - just like building levels in Mario Maker or using Godot's tilemap editor!

## Installation

### Download Tiled
1. Go to https://www.mapeditor.org/
2. Download Tiled for macOS
3. Install it on your computer

## How to Create Levels

### Step 1: Create a New Map
1. Open Tiled
2. File → New → New Map
3. Set these properties:
   - **Orientation**: Orthogonal
   - **Tile layer format**: CSV
   - **Tile size**: 20x20 pixels (for platforms)
   - **Map size**: 40x30 tiles (800x600 screen)

### Step 2: Import Your Tileset
1. Map → New Tileset
2. Browse to: `assets/backgrounds/Mossy Tileset/Mossy - TileSet.png`
3. Set tile width/height to match your tileset

### Step 3: Create Layers
Create these layers (Layer → New Layer):
1. **Background** - for background tiles
2. **Platforms** - for solid platforms
3. **Objects** - for enemies, coins, player spawn

### Step 4: Add Objects
1. Switch to the Objects layer
2. Use Insert Rectangle tool to place:
   - **Player** - Add custom property `type = "player"`
   - **Enemy** - Add properties `type = "enemy"`, `range = 100`
   - **Coin** - Add property `type = "coin"`
   - **Boss** - Add property `type = "boss"`

### Step 5: Save Your Level
1. File → Save As
2. Save to: `assets/levels/level1.tmx`
3. Repeat for level2.tmx and level3.tmx

## Tips

- Use the stamp brush to quickly paint platforms
- Use object layers for entities (enemies, coins, player start)
- You can test your level by loading it in the game
- Press Tab to switch between layers
- Use Grid → Show Grid to help align objects

## Custom Properties for Objects

When you add an object, set these properties:

### Player Spawn
- `type`: "player"

### Enemy
- `type`: "enemy"
- `movement_range`: 100 (how far it moves)

### Coin
- `type`: "coin"

### Boss
- `type`: "boss"

## Next Steps

After creating your TMX files, the game will automatically load them instead of using the hardcoded level layouts!
