import pygame
import sys

# Initialize PyGame
pygame.init()

# Set up display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PALETTE_HEIGHT = 50  # Height of the color palette area
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + PALETTE_HEIGHT))
pygame.display.set_caption("Isometric World Building Game with Color Palette")

# Define grid dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Define tile dimensions
TILE_WIDTH = 64
TILE_HEIGHT = 32

# Define colors
colors = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (255, 192, 203) # Pink
]
selected_color = colors[0]

# Create a 2D grid to represent the world, storing the color of each tile
world = [[None for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

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
                if mouse_y >= SCREEN_HEIGHT:
                    # Clicked on the palette
                    palette_x = mouse_x // (SCREEN_WIDTH // len(colors))
                    if 0 <= palette_x < len(colors):
                        selected_color = colors[palette_x]
                else:
                    # Convert screen coordinates to grid coordinates
                    grid_x, grid_y = iso_to_grid(mouse_x, mouse_y)
                    # Check if grid coordinates are within bounds
                    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                        if world[grid_y][grid_x] == selected_color:
                            world[grid_y][grid_x] = None  # Remove color
                        else:
                            world[grid_y][grid_x] = selected_color  # Set selected color

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
            if world[y][x]:
                # Filled tile with the assigned color
                pygame.draw.polygon(screen, world[y][x], tile_points)
            else:
                # Empty tile
                pygame.draw.polygon(screen, (255, 255, 255), tile_points, 1)

    # Draw the color palette
    palette_width = SCREEN_WIDTH // len(colors)
    for idx, color in enumerate(colors):
        rect = pygame.Rect(idx * palette_width, SCREEN_HEIGHT, palette_width, PALETTE_HEIGHT)
        pygame.draw.rect(screen, color, rect)
        if color == selected_color:
            # Highlight the selected color
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit PyGame
pygame.quit()
sys.exit()
