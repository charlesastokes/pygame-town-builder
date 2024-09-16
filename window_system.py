# window_system.py

import pygame

class PaletteWindow:
    def __init__(self, colors, screen_width, screen_height, width=200, height=100):
        self.colors = colors
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = self.screen_width - self.width - 10  # Start near the bottom-right corner
        self.y = self.screen_height - self.height - 10
        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.minimized = False
        self.minimized_height = 30  # Height when minimized

    def handle_event(self, event, selected_color):
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
                    # Check if click is on a color box when not minimized
                    if not self.minimized:
                        palette_margin = 10
                        color_box_size = (self.width - 2 * palette_margin) // len(self.colors)
                        for idx, color in enumerate(self.colors):
                            rect = pygame.Rect(
                                self.x + palette_margin + idx * color_box_size,
                                self.y + self.minimized_height + 10,
                                color_box_size - 5,
                                color_box_size - 5
                            )
                            if rect.collidepoint(mouse_x, mouse_y):
                                selected_color = color
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
                self.x = max(0, min(self.x, self.screen_width - self.width))
                self.y = max(0, min(self.y, self.screen_height - self.height))
        return selected_color

    def update(self):
        pass  # Add any updates if necessary

    def draw(self, surface, selected_color):
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
