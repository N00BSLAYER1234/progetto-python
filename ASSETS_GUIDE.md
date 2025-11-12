# How to Add Sprites and Backgrounds

The game now supports custom images for sprites and backgrounds!

## Folder Structure

```
progetto python/
├── assets/
│   ├── sprites/      # Character and object images
│   └── backgrounds/  # Level background images
```

## Adding Sprites

Place your sprite images in `assets/sprites/` with these exact names:

### Required Sprite Files:

1. **player.png** - The player character
   - Recommended size: 40x60 pixels
   - Format: PNG with transparency

2. **enemy.png** - Enemy characters
   - Recommended size: 40x40 pixels
   - Format: PNG with transparency

3. **coin.png** - Collectible coins
   - Recommended size: 20x20 pixels
   - Format: PNG with transparency

4. **platform.png** - Platform tiles
   - Size: Any width x 20 pixels height
   - Format: PNG (will be tiled horizontally)

5. **boss.png** - Boss character
   - Recommended size: 80x100 pixels
   - Format: PNG with transparency

## Adding Backgrounds

Place your background images in `assets/backgrounds/` with these exact names:

### Required Background Files:

1. **level1.png** - Level 1 background
   - Size: 800x600 pixels (or any size, will be scaled)
   - Format: PNG or JPG

2. **level2.png** - Level 2 background
   - Size: 800x600 pixels (or any size, will be scaled)
   - Format: PNG or JPG

3. **level3.png** - Level 3 background (Boss level)
   - Size: 800x600 pixels (or any size, will be scaled)
   - Format: PNG or JPG

## What If I Don't Add Images?

Don't worry! The game will work fine without custom images. It will use:
- **Colored rectangles** for sprites (blue player, red enemies, yellow coins, etc.)
- **Solid colored backgrounds** for levels (different shades of blue)

## Where to Find Free Sprites

You can find free game sprites at:
- **OpenGameArt.org** - Free game assets
- **Itch.io** - Many free sprite packs
- **Kenney.nl** - Excellent free game assets
- **Pixabay** - Free images and sprites

## Tips

- Keep file sizes reasonable (< 1MB per image)
- PNG format is best for sprites (supports transparency)
- JPG is fine for backgrounds
- Make sure filenames are exactly as listed above (case-sensitive!)
- The game will automatically scale images to fit

## Example: Adding a Player Sprite

1. Download or create a player character image
2. Save it as `player.png`
3. Place it in `assets/sprites/player.png`
4. Run the game - your character will now appear!

Enjoy customizing your game!
