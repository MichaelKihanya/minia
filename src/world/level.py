import pygame
from src.utils.constants import *

class Level:
    """Grid-based world with multiple zones for exploration"""
    
    TILE_SIZE = 32
    
    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0
        self.platforms = []  # Keep for compatibility
        
    def update(self, player):
        """Update camera to follow player"""
        # Center camera on player
        self.camera_x = player.rect.centerx - WINDOW_WIDTH // 3
        self.camera_y = player.rect.centery - WINDOW_HEIGHT // 2
        
        # Clamp camera to world bounds (20x30 tiles)
        max_x = 20 * self.TILE_SIZE - WINDOW_WIDTH
        max_y = 30 * self.TILE_SIZE - WINDOW_HEIGHT
        self.camera_x = max(0, min(self.camera_x, max_x))
        self.camera_y = max(0, min(self.camera_y, max_y))

    def draw(self, surface):
        """Draw the world with distinct terrain zones"""
        # Define terrain colors for each zone type
        COLORS = {
            'grass': (140, 160, 100),      # Muted sage green
            'sand': (220, 200, 150),        # Beach sand
            'water': (100, 150, 200),       # Water/ocean
            'dirt': (160, 140, 100),        # Dirt path
        }
        
        # Draw base background
        surface.fill((200, 190, 180))
        
        TILE_SIZE = self.TILE_SIZE
        
        # Draw terrain tiles based on position
        for x in range(-1, (WINDOW_WIDTH // TILE_SIZE) + 2):
            for y in range(-1, (WINDOW_HEIGHT // TILE_SIZE) + 2):
                # Convert to world coordinates
                world_x = x + (self.camera_x // TILE_SIZE)
                world_y = y + (self.camera_y // TILE_SIZE)
                
                # Determine terrain type based on zone
                terrain_color = COLORS['grass']  # Default
                
                # Town area (0-10, 0-10) - dirt
                if 0 <= world_x < 10 and 0 <= world_y < 10:
                    terrain_color = COLORS['dirt']
                # Beach area (10-20, 0-10) - sand and water
                elif 10 <= world_x < 20:
                    if 0 <= world_y < 10:
                        terrain_color = COLORS['sand']
                    elif 10 <= world_y < 12:  # Water at bottom of beach
                        terrain_color = COLORS['water']
                # Yoga garden (0-10, 10-20) - grass
                elif 0 <= world_x < 10 and 10 <= world_y < 20:
                    terrain_color = COLORS['grass']
                # Taco market (10-20, 10-20) - mixed
                elif 10 <= world_x < 20 and 10 <= world_y < 20:
                    if world_x % 2 == 0:
                        terrain_color = COLORS['sand']
                    else:
                        terrain_color = COLORS['dirt']
                # Nature area (0-20, 20-30) - grass
                elif 0 <= world_y < 30:
                    terrain_color = COLORS['grass']
                
                # Draw tile
                screen_x = x * TILE_SIZE
                screen_y = y * TILE_SIZE
                pygame.draw.rect(surface, terrain_color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
                
                # Draw subtle grid lines
                pygame.draw.rect(surface, (180, 170, 160), (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 1)
        
        # Draw decorative elements
        self._draw_decorations(surface)
        self._draw_zone_labels(surface)
    
    def _draw_decorations(self, surface):
        """Draw decorative elements like trees and water details"""
        TILE_SIZE = self.TILE_SIZE
        
        # Draw simple tree decorations in nature and yoga areas
        tree_positions = [
            (15, 24), (16, 25), (17, 26),  # Nature area trees
            (3, 15), (8, 18),  # Yoga garden trees
        ]
        
        for world_x, world_y in tree_positions:
            screen_x = world_x * TILE_SIZE - (self.camera_x % TILE_SIZE) - (self.camera_x // TILE_SIZE) * TILE_SIZE
            screen_y = world_y * TILE_SIZE - (self.camera_y % TILE_SIZE) - (self.camera_y // TILE_SIZE) * TILE_SIZE
            
            if -TILE_SIZE < screen_x < WINDOW_WIDTH and -TILE_SIZE < screen_y < WINDOW_HEIGHT:
                # Draw simple tree (trunk and foliage)
                pygame.draw.rect(surface, (100, 60, 40), (screen_x + 10, screen_y + 16, 12, 16))
                pygame.draw.rect(surface, (80, 120, 60), (screen_x + 4, screen_y + 4, 24, 16))
    
    def _draw_zone_labels(self, surface):
        """Draw zone labels on the map"""
        font = pygame.font.Font(None, 24)
        zones_info = [
            ((50, 50), "Town"),
            ((WINDOW_WIDTH - 150, 50), "Beach 🌊"),
            ((50, WINDOW_HEIGHT - 100), "Yoga Garden 🧘"),
            ((WINDOW_WIDTH - 150, WINDOW_HEIGHT - 100), "Taco Market 🌮"),
            ((WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - 50), "Nature 🌿"),
        ]
        
        for pos, label in zones_info:
            text = font.render(label, True, (100, 80, 70))
            text.set_alpha(80)
            surface.blit(text, pos)
    
    def grid_to_pixel(self, grid_x, grid_y):
        """Convert grid coordinates to pixel coordinates"""
        return grid_x * self.TILE_SIZE, grid_y * self.TILE_SIZE
    
    def pixel_to_grid(self, pixel_x, pixel_y):
        """Convert pixel coordinates to grid coordinates"""
        return pixel_x // self.TILE_SIZE, pixel_y // self.TILE_SIZE 