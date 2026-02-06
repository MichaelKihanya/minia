import pygame
import math
import random
from src.utils.constants import *

def create_taco_sprite():
    sprite = pygame.Surface((24, 24), pygame.SRCALPHA)
    
    # Draw taco shell (yellow/gold)
    shell_color = (220, 170, 90)
    pygame.draw.polygon(sprite, shell_color, [(3, 12), (12, 5), (21, 12), (12, 19)])
    
    # Draw lettuce (green)
    lettuce_color = (140, 160, 100)
    pygame.draw.polygon(sprite, lettuce_color, [(5, 12), (12, 8), (19, 12), (12, 16)])
    
    # Draw cheese (orange)
    cheese_color = (255, 160, 80)
    pygame.draw.circle(sprite, cheese_color, (10, 12), 2)
    pygame.draw.circle(sprite, cheese_color, (14, 12), 2)
    
    return sprite

class MusicalNote(pygame.sprite.Sprite):
    """Taco collectible - renamed from MusicalNote for Tania"""
    def __init__(self, x, y):
        super().__init__()
        self.image = create_taco_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.float_offset = random.randint(0, 360)
        self.float_speed = 0.05

    def update(self):
        # Make the note float up and down
        self.rect.y += math.sin(pygame.time.get_ticks() * self.float_speed + self.float_offset) * 0.5 