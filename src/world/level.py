import pygame
import random
from src.utils.constants import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface((width, PLATFORM_HEIGHT))
        self.image.fill(GRASS_GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Level:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.camera_x = 0
        self.generate_level()

    def generate_level(self):
        # Create ground platform
        ground = Platform(0, WINDOW_HEIGHT - PLATFORM_HEIGHT, WORLD_WIDTH)
        self.platforms.add(ground)
        self.all_sprites.add(ground)

        # Generate floating platforms
        for x in range(PLATFORM_SPACING, WORLD_WIDTH - PLATFORM_WIDTH, PLATFORM_SPACING):
            y = random.randint(WINDOW_HEIGHT - 300, WINDOW_HEIGHT - 100)
            platform = Platform(x, y, PLATFORM_WIDTH)
            self.platforms.add(platform)
            self.all_sprites.add(platform)

    def update(self, player):
        # Update camera position based on player
        self.camera_x = max(0, min(player.rect.centerx - WINDOW_WIDTH // 2,
                                 WORLD_WIDTH - WINDOW_WIDTH))

    def draw(self, screen):
        # Draw sky background
        screen.fill(SKY_BLUE)
        
        # Draw all sprites with camera offset
        for sprite in self.all_sprites:
            screen.blit(sprite.image, 
                       (sprite.rect.x - self.camera_x, sprite.rect.y)) 