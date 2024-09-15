import pygame
import sys

# Initialize PyGame
pygame.init()

# Set up display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isometric World Building Game")

# Define grid dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Define tile dimensions
TILE_WIDTH = 64
TILE_HEIGHT = 32

# Create a 2D grid to represent the world
world = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

# Function to convert grid coordinates to isometric screen coordinates
def grid_to_iso(x, y):
    screen_x = (x - y) * (TILE_WIDTH // 2) + SCREEN_WIDTH // 2
    screen_y = (x + y) * (TILE_HEIGHT // 2)
    return screen_x, screen_y

# Function to convert screen coordinates to grid coordinates
def iso_to_grid(screen_x, screen_y):
    dx = screen_x - SCREEN_WIDTH // 2
    dy = screen_y
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
        # Handle mouse click events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Convert screen coordinates to grid coordinates
                grid_x, grid_y = iso_to_grid(mouse_x, mouse_y)
                # Check if grid coordinates are within bounds
                if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                    world[grid_y][grid_x] = 1 - world[grid_y][grid_x]  # Toggle tile

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the world
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            iso_x, iso_y = grid_to_iso(x, y)
            # Draw tile outline
            tile_points = [
                (iso_x, iso_y - TILE_HEIGHT // 2),
                (iso_x + TILE_WIDTH // 2, iso_y),
                (iso_x, iso_y + TILE_HEIGHT // 2),
                (iso_x - TILE_WIDTH // 2, iso_y)
            ]
            if world[y][x] == 1:
                # Filled tile
                pygame.draw.polygon(screen, (0, 255, 0), tile_points)
            else:
                # Empty tile
                pygame.draw.polygon(screen, (255, 255, 255), tile_points, 1)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit PyGame
pygame.quit()
sys.exit()
