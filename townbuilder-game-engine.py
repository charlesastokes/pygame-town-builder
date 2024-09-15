import pygame
import sys

# Initialize PyGame
pygame.init()

# Set up display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isometric World Building Game with Movable Palette")

# Define grid dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Define tile dimensions
TILE_WIDTH = 64
TILE_HEIGHT = 32

# Compute grid vertical offset to center it
GRID_PIXEL_HEIGHT = (GRID_WIDTH + GRID_HEIGHT) * (TILE_HEIGHT // 2)
GRID_OFFSET_Y = (SCREEN_HEIGHT - GRID_PIXEL_HEIGHT) // 2

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

# Palette window class
class PaletteWindow:
    def __init__(self, colors, width=200, height=100):
        self.colors = colors
        self.width = width
        self.height = height
        self.x = SCREEN_WIDTH - self.width - 10  # Start near the bottom-right corner
        self.y = SCREEN_HEIGHT - self.height - 10
        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.minimized = False
        self.minimized_height = 30  # Height when minimized

    def handle_event(self, event):
        global selected_color
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Check if click is within the palette window
            if self.rect.collidepoint(mouse_x, mouse_y):
                if event.button == 1:  # Left click
                    # Check for minimize button
                    if self.minimize_rect.collidepoint(mouse_x, mouse_y):
                        self.minimized = not self.minimized
                    else:
                        self.is_dragging = True
                        self.offset_x = self.x - mouse_x
                        self.offset_y = self.y - mouse_y
                elif event.button == 3:  # Right click
                    pass  # You can add more functionality here
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                mouse_x, mouse_y = event.pos
                self.x = mouse_x + self.offset_x
                self.y = mouse_y + self.offset_y
                # Keep the window within the screen bounds
                self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
                self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

    def update(self):
        pass  # Add any updates if necessary

    def draw(self, surface):
        # Draw the window background
        if self.minimized:
            window_height = self.minimized_height
        else:
            window_height = self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, window_height)
        pygame.draw.rect(surface, (50, 50, 50), self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)

        # Draw the minimize button
        self.minimize_rect = pygame.Rect(self.x + self.width - 25, self.y + 5, 20, 20)
        pygame.draw.rect(surface, (200, 200, 200), self.minimize_rect)
        pygame.draw.line(surface, (0, 0, 0), (self.minimize_rect.left + 5, self.minimize_rect.centery),
                         (self.minimize_rect.right - 5, self.minimize_rect.centery), 2)

        if self.minimized:
            return  # Do not draw palette contents when minimized

        # Draw the color palette inside the window
        palette_margin = 10
        color_box_size = (self.width - 2 * palette_margin) // len(self.colors)
        for idx, color in enumerate(self.colors):
            rect = pygame.Rect(
                self.x + palette_margin + idx * color_box_size,
                self.y + self.minimized_height + 10,
                color_box_size - 5,
                color_box_size - 5
            )
            pygame.draw.rect(surface, color, rect)
            if color == selected_color:
                pygame.draw.rect(surface, (255, 255, 255), rect, 3)

# Instantiate the palette window
palette_window = PaletteWindow(colors)

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
        else:
            palette_window.handle_event(event)
            # Handle mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Get mouse position
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Check if click is outside the palette window
                    if not palette_window.rect.collidepoint(mouse_x, mouse_y):
                        # Convert screen coordinates to grid coordinates
                        grid_x, grid_y = iso_to_grid(mouse_x, mouse_y)
                        # Check if grid coordinates are within bounds
                        if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                            if world[grid_y][grid_x] == selected_color:
                                world[grid_y][grid_x] = None  # Remove color
                            else:
                                world[grid_y][grid_x] = selected_color  # Set selected color
                    else:
                        # Check if click is on a color box when not minimized
                        if not palette_window.minimized:
                            palette_margin = 10
                            color_box_size = (palette_window.width - 2 * palette_margin) // len(colors)
                            for idx, color in enumerate(colors):
                                rect = pygame.Rect(
                                    palette_window.x + palette_margin + idx * color_box_size,
                                    palette_window.y + palette_window.minimized_height + 10,
                                    color_box_size - 5,
                                    color_box_size - 5
                                )
                                if rect.collidepoint(mouse_x, mouse_y):
                                    selected_color = color

    # Update
    palette_window.update()

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

    # Draw the palette window
    palette_window.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit PyGame
pygame.quit()
sys.exit()
