# main.py

import pygame
import sys
from window_system import PaletteWindow

# Initialize PyGame
pygame.init()

# Set up display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isometric World Building Game with Tile Images")

# Define grid dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Define initial tile dimensions
BASE_TILE_WIDTH = 64
BASE_TILE_HEIGHT = 32
zoom_factor = 1.0  # Initial zoom factor

# Compute grid vertical offset to center it
def calculate_grid_offset():
    global GRID_PIXEL_HEIGHT, GRID_OFFSET_Y
    GRID_PIXEL_HEIGHT = (GRID_WIDTH + GRID_HEIGHT) * (TILE_HEIGHT // 2)
    GRID_OFFSET_Y = (SCREEN_HEIGHT - GRID_PIXEL_HEIGHT) // 2

# Load tile images
tile_image_files = [
    "grass_texture.png",
    "water_texture.png",
    #"sand_tile.png",
    #"stone_tile.png"
]
tile_images = []
for filename in tile_image_files:
    image = pygame.image.load(filename).convert_alpha()
    tile_images.append(image)
selected_tile = tile_images[0]

# Create a 2D grid to represent the world, storing the tile image index
world = [[None for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

# Instantiate the palette window
palette_window = PaletteWindow(tile_images, SCREEN_WIDTH, SCREEN_HEIGHT, use_images=True)

# Update tile dimensions based on zoom factor
def update_tile_dimensions():
    global TILE_WIDTH, TILE_HEIGHT
    TILE_WIDTH = int(BASE_TILE_WIDTH * zoom_factor)
    TILE_HEIGHT = int(BASE_TILE_HEIGHT * zoom_factor)
    if TILE_WIDTH < 8 or TILE_HEIGHT < 4:
        TILE_WIDTH = 8
        TILE_HEIGHT = 4
    calculate_grid_offset()
    # Resize tile images based on zoom
    global resized_tile_images
    resized_tile_images = [pygame.transform.smoothscale(img, (TILE_WIDTH, TILE_HEIGHT)) for img in tile_images]

update_tile_dimensions()

# Function to convert grid coordinates to isometric screen coordinates
def grid_to_iso(x, y):
    screen_x = (x - y) * (TILE_WIDTH // 2) + SCREEN_WIDTH // 2
    screen_y = (x + y) * (TILE_HEIGHT // 2) + GRID_OFFSET_Y
    return screen_x, screen_y

# Function to convert screen coordinates to grid coordinates
def iso_to_grid(screen_x, screen_y):
    dx = screen_x - SCREEN_WIDTH // 2
    dy = screen_y - GRID_OFFSET_Y
    a = dx / (TILE_WIDTH / 2)
    b = dy / (TILE_HEIGHT / 2)
    x = (a + b) / 2
    y = (b - a) / 2
    return int(round(x)), int(round(y))

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse wheel for zooming
            if event.button == 4:  # Mouse wheel up
                zoom_factor += 0.1
                update_tile_dimensions()
            elif event.button == 5:  # Mouse wheel down
                zoom_factor -= 0.1
                if zoom_factor < 0.2:
                    zoom_factor = 0.2
                update_tile_dimensions()
            else:
                # Handle left click
                selected_tile = palette_window.handle_event(event, selected_tile)
                mouse_x, mouse_y = event.pos
                # Check if click is outside the palette window
                if not palette_window.rect.collidepoint(mouse_x, mouse_y):
                    # Convert screen coordinates to grid coordinates
                    grid_x, grid_y = iso_to_grid(mouse_x, mouse_y)
                    # Check if grid coordinates are within bounds
                    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                        if world[grid_y][grid_x] == selected_tile:
                            world[grid_y][grid_x] = None  # Remove tile
                        else:
                            world[grid_y][grid_x] = selected_tile  # Place selected tile
        else:
            selected_tile = palette_window.handle_event(event, selected_tile)

    # Update
    palette_window.update()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the world
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            iso_x, iso_y = grid_to_iso(x, y)
            if world[y][x]:
                # Draw the tile image
                tile_image = resized_tile_images[tile_images.index(world[y][x])]
                tile_rect = tile_image.get_rect(center=(iso_x, iso_y))
                screen.blit(tile_image, tile_rect)
            else:
                # Draw empty tile outline
                tile_points = [
                    (iso_x, iso_y - TILE_HEIGHT // 2),
                    (iso_x + TILE_WIDTH // 2, iso_y),
                    (iso_x, iso_y + TILE_HEIGHT // 2),
                    (iso_x - TILE_WIDTH // 2, iso_y)
                ]
                pygame.draw.polygon(screen, (255, 255, 255), tile_points, 1)

    # Draw the palette window
    palette_window.draw(screen, selected_tile, zoom_factor)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit PyGame
pygame.quit()
sys.exit()
